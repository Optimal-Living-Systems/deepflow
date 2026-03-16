"""CLI for Deep Flo."""

from __future__ import annotations

import asyncio
import json

import typer
import uvicorn

from deep_flo_runtime.config import get_settings
from deep_flo_runtime.runtime_api import InvokeRequest, RuntimeService, create_app
from deep_flo_runtime.utils.banner import print_banner

app = typer.Typer(no_args_is_help=True, add_completion=False)

def main() -> None:
    """Run the Deep Flo CLI with startup branding."""
    print_banner()
    app()


@app.command()
def doctor() -> None:
    """Print runtime status and missing prerequisites."""
    settings = get_settings()
    payload = {
        "home_dir": str(settings.home_dir),
        "workspace_dir": str(settings.workspace_dir),
        "sqlite_path": str(settings.sqlite_path),
        "provider_status": settings.provider_status(),
        "model": settings.model or "auto",
    }
    typer.echo(json.dumps(payload, indent=2, sort_keys=True))


@app.command()
def serve() -> None:
    """Run the Deep Flo runtime API."""
    settings = get_settings()
    uvicorn.run(
        create_app(settings),
        host=settings.host,
        port=settings.port,
        log_level="info",
    )


@app.command()
def run(prompt: str, thread_id: str = "deep-flo-cli") -> None:
    """Run one prompt against the Deep Flo runtime graph."""
    asyncio.run(_run_once(prompt=prompt, thread_id=thread_id))


@app.command()
def chat(thread_id: str = "deep-flo-chat") -> None:
    """Run an interactive REPL."""
    asyncio.run(_chat_loop(thread_id=thread_id))


@app.command()
def acp() -> None:
    """Run the ACP server for ACP-capable editors."""
    from deep_flo_runtime.acp_server import run_acp_server

    asyncio.run(run_acp_server(get_settings()))


@app.command("mcp")
def mcp_command(
    transport: str = typer.Option("stdio", help="MCP transport: stdio or streamable-http."),
    host: str | None = typer.Option(None, help="Host for streamable-http transport."),
    port: int | None = typer.Option(None, help="Port for streamable-http transport."),
) -> None:
    """Run the Deep Flo MCP server for IDE and Langflow MCP clients."""
    from deep_flo_runtime.mcp_server import run_mcp_server

    settings = get_settings()
    resolved_host = host or settings.host
    resolved_port = port or 8012
    run_mcp_server(transport=transport, host=resolved_host, port=resolved_port)


async def _run_once(*, prompt: str, thread_id: str) -> None:
    settings = get_settings()
    service = RuntimeService(settings)
    await service.start()
    try:
        response = await service.invoke(InvokeRequest(prompt=prompt, thread_id=thread_id))
    finally:
        await service.stop()
    typer.echo(response.output_text)


async def _chat_loop(*, thread_id: str) -> None:
    settings = get_settings()
    service = RuntimeService(settings)
    await service.start()
    typer.echo("Deep Flo chat. Type 'exit' or 'quit' to stop.")
    try:
        while True:
            prompt = typer.prompt("you")
            if prompt.strip().lower() in {"exit", "quit"}:
                break
            response = await service.invoke(InvokeRequest(prompt=prompt, thread_id=thread_id))
            typer.echo(f"deep-flo> {response.output_text}")
    finally:
        await service.stop()
