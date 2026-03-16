"""Agent builders for the Deep Flo runtime and ACP server."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, FilesystemBackend, LocalShellBackend, StateBackend
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langgraph.types import Checkpointer

from deep_flo_runtime.config import DeepFloSettings
from deep_flo_runtime.prompts import ACP_SYSTEM_PROMPT, MAIN_SYSTEM_PROMPT, RESEARCH_SUBAGENT_PROMPT
from deep_flo_runtime.tools import create_runtime_tools


def resolve_model(settings: DeepFloSettings) -> BaseChatModel:
    """Resolve the first available model configuration."""
    if settings.model:
        return _build_model_from_name(settings.model)

    providers = settings.provider_status()
    if providers["anthropic"]:
        return _build_model_from_name(settings.anthropic_default_model)
    if providers["openai"]:
        return _build_model_from_name(settings.openai_default_model)
    if providers["google"]:
        return _build_model_from_name(settings.google_default_model)
    if providers["openrouter"]:
        return _build_model_from_name(settings.openrouter_default_model)
    if providers["deepseek"]:
        return _build_model_from_name(settings.deepseek_default_model)
    if os.getenv("OLLAMA_HOST") or os.getenv("OLLAMA_BASE_URL"):
        return _build_model_from_name(settings.ollama_default_model)

    msg = (
        "No model provider configured. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY, "
        "OPENROUTER_API_KEY, DEEPSEEK_API_KEY, or DEEP_FLO_MODEL=ollama:<model-name> with a "
        "reachable Ollama server."
    )
    raise RuntimeError(msg)


def _build_model_from_name(model_name: str) -> BaseChatModel:
    """Build a chat model, using provider-specific classes when needed."""
    if model_name.startswith("openrouter:"):
        from langchain_openrouter import ChatOpenRouter

        return ChatOpenRouter(
            model=model_name.split(":", 1)[1],
            temperature=0.0,
            max_retries=2,
        )
    if model_name.startswith("deepseek:"):
        from langchain_deepseek import ChatDeepSeek

        return ChatDeepSeek(
            model=model_name.split(":", 1)[1],
            temperature=0.0,
            max_retries=2,
        )
    return init_chat_model(model_name, temperature=0.0)


def create_runtime_backend(settings: DeepFloSettings) -> CompositeBackend:
    """Create the bounded filesystem backend used by the HTTP runtime."""
    return CompositeBackend(
        default=FilesystemBackend(root_dir=str(settings.workspace_dir), virtual_mode=False),
        routes={
            "/memories/": FilesystemBackend(root_dir=str(settings.memories_dir), virtual_mode=True),
            "/skills/": FilesystemBackend(root_dir=str(settings.skills_dir), virtual_mode=True),
        },
    )


def build_runtime_agent(settings: DeepFloSettings, *, checkpointer: Checkpointer) -> Any:
    """Build the research-oriented runtime agent."""
    model = resolve_model(settings)
    tools = create_runtime_tools(settings)
    subagents = [
        {
            "name": "researcher",
            "description": "Use this subagent for focused web research on a single topic.",
            "system_prompt": RESEARCH_SUBAGENT_PROMPT,
            "tools": tools,
        }
    ]
    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=MAIN_SYSTEM_PROMPT,
        subagents=subagents,
        skills=[str(settings.skills_dir)],
        memory=[str(settings.memory_file)],
        checkpointer=checkpointer,
        backend=create_runtime_backend(settings),
        name="deep-flo-runtime",
    )


def build_acp_agent(
    settings: DeepFloSettings,
    *,
    project_root: Path,
    checkpointer: Checkpointer,
    mode: str,
) -> Any:
    """Build the ACP editor-facing agent."""

    interrupt_on = {
        "edit_file": {"allowed_decisions": ["approve", "reject"]},
        "write_file": {"allowed_decisions": ["approve", "reject"]},
        "write_todos": {"allowed_decisions": ["approve", "reject"]},
        "execute": {"allowed_decisions": ["approve", "reject"]},
    }
    if mode == "accept_edits":
        interrupt_on.pop("edit_file", None)
        interrupt_on.pop("write_file", None)
    elif mode == "accept_everything":
        interrupt_on = {}

    def create_backend(runtime: Any | None = None) -> CompositeBackend:
        ephemeral_backend = StateBackend(runtime) if runtime is not None else None
        shell_backend = LocalShellBackend(
            root_dir=str(project_root),
            inherit_env=True,
            env=os.environ.copy(),
        )
        routes: dict[str, Any] = {}
        if ephemeral_backend is not None:
            routes["/memories/"] = ephemeral_backend
            routes["/conversation_history/"] = ephemeral_backend
        return CompositeBackend(default=shell_backend, routes=routes)

    return create_deep_agent(
        model=resolve_model(settings),
        tools=create_runtime_tools(settings),
        system_prompt=ACP_SYSTEM_PROMPT,
        skills=[str(settings.skills_dir)],
        checkpointer=checkpointer,
        backend=create_backend,
        interrupt_on=interrupt_on,
        name="deep-flo-acp",
    )
