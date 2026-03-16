"""FastAPI runtime for DeepFlow."""

from __future__ import annotations

import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from langchain_core.messages import AIMessage, BaseMessage
from pydantic import BaseModel, Field

from deepflow_runtime.agent import build_runtime_agent
from deepflow_runtime.config import DeepFlowSettings, get_settings
from deepflow_runtime.sqlite_compat import AsyncCompatibleSqliteSaver, open_checkpointer

_bearer = HTTPBearer(auto_error=False)


def require_api_key(
    credentials: HTTPAuthorizationCredentials | None = Security(_bearer),
    settings: DeepFlowSettings = Depends(get_settings),
) -> None:
    """Validate Bearer token when DEEPFLOW_API_KEY is set."""
    if settings.api_key is None:
        return
    if credentials is None or credentials.credentials != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


class InvokeRequest(BaseModel):
    """Invocation payload for the DeepFlow runtime."""

    prompt: str = Field(min_length=1)
    thread_id: str = Field(default="deepflow-default")


class InvokeResponse(BaseModel):
    """Response payload for the DeepFlow runtime."""

    thread_id: str
    output_text: str
    message_count: int


@dataclass
class RuntimeService:
    """Manages the lifecycle of the DeepFlow runtime graph."""

    settings: DeepFlowSettings
    checkpointer: AsyncCompatibleSqliteSaver | None = None
    checkpointer_cm: Any | None = None
    agent: Any | None = None
    startup_error: str | None = None

    async def start(self) -> None:
        """Start the runtime and compile the graph."""
        self.settings.ensure_directories()
        self.checkpointer_cm = open_checkpointer(str(self.settings.sqlite_path))
        self.checkpointer = self.checkpointer_cm.__enter__()
        try:
            self.agent = build_runtime_agent(self.settings, checkpointer=self.checkpointer)
            self.startup_error = None
        except RuntimeError as exc:
            self.agent = None
            self.startup_error = str(exc)

    async def stop(self) -> None:
        """Stop the runtime and release the database handle."""
        if self.checkpointer_cm is not None:
            self.checkpointer_cm.__exit__(None, None, None)
        self.checkpointer = None
        self.checkpointer_cm = None
        self.agent = None
        self.startup_error = None

    def _get_agent(self) -> Any:
        """Return the compiled agent, rebuilding if needed."""
        if self.agent is None:
            if self.checkpointer is None:
                raise RuntimeError("RuntimeService.start() must be called before invoke().")
            self.agent = build_runtime_agent(self.settings, checkpointer=self.checkpointer)
            self.startup_error = None
        return self.agent

    async def invoke(self, request: InvokeRequest) -> InvokeResponse:
        """Run the graph for one user request."""
        agent = self._get_agent()
        result = await agent.ainvoke(
            {"messages": [("user", request.prompt)]},
            config={"configurable": {"thread_id": request.thread_id}},
        )
        messages = result.get("messages", [])
        return InvokeResponse(
            thread_id=request.thread_id,
            output_text=extract_text(messages),
            message_count=len(messages),
        )

    async def stream(self, request: InvokeRequest) -> AsyncGenerator[str, None]:
        """Stream token chunks as SSE for one user request."""
        agent = self._get_agent()
        config = {"configurable": {"thread_id": request.thread_id}}
        async for event in agent.astream_events(
            {"messages": [("user", request.prompt)]},
            config=config,
            version="v2",
        ):
            if event["event"] == "on_chat_model_stream":
                chunk = event["data"].get("chunk")
                if chunk is None:
                    continue
                content = chunk.content
                if isinstance(content, str) and content:
                    yield f"data: {json.dumps({'text': content})}\n\n"
                elif isinstance(content, list):
                    for part in content:
                        if isinstance(part, dict) and part.get("type") == "text":
                            text = part.get("text", "")
                            if text:
                                yield f"data: {json.dumps({'text': text})}\n\n"
        yield f"data: {json.dumps({'done': True, 'thread_id': request.thread_id})}\n\n"


def extract_text(messages: list[Any]) -> str:
    """Extract the last assistant text from a LangGraph message list."""
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            return _message_to_text(message)
        if isinstance(message, BaseMessage) and getattr(message, "type", "") == "ai":
            return _message_to_text(message)
    return ""


def _message_to_text(message: BaseMessage) -> str:
    """Convert a message content payload into plain text."""
    content = message.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)
    return str(content)


def create_app(settings: DeepFlowSettings | None = None) -> FastAPI:
    """Create the DeepFlow FastAPI app."""
    runtime_settings = settings or get_settings()
    service = RuntimeService(runtime_settings)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        await service.start()
        try:
            yield
        finally:
            await service.stop()

    app = FastAPI(title="DeepFlow Runtime", version="0.1.0", lifespan=lifespan)
    app.state.service = service

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "provider_status": runtime_settings.provider_status(),
            "workspace_dir": str(runtime_settings.workspace_dir),
            "sqlite_path": str(runtime_settings.sqlite_path),
            "startup_error": service.startup_error,
        }

    @app.post("/invoke", response_model=InvokeResponse, dependencies=[Depends(require_api_key)])
    async def invoke(request: InvokeRequest) -> InvokeResponse:
        try:
            return await service.invoke(request)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.post("/invoke/stream", dependencies=[Depends(require_api_key)])
    async def invoke_stream(request: InvokeRequest) -> StreamingResponse:
        try:
            return StreamingResponse(
                service.stream(request),
                media_type="text/event-stream",
                headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
            )
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    return app
