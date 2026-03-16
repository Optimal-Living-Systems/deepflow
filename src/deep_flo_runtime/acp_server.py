"""ACP server entrypoint for Deep Flo."""

from __future__ import annotations

from pathlib import Path

from acp import run_agent as run_acp_agent
from acp.schema import SessionMode, SessionModeState
from deepagents_acp.server import AgentServerACP, AgentSessionContext

from deep_flo_runtime.agent import build_acp_agent
from deep_flo_runtime.config import DeepFloSettings
from deep_flo_runtime.sqlite_compat import open_checkpointer


async def run_acp_server(settings: DeepFloSettings) -> None:
    """Run the ACP server with a shared SQLite checkpointer."""
    with open_checkpointer(str(settings.sqlite_path)) as checkpointer:

        def build_agent(context: AgentSessionContext):
            return build_acp_agent(
                settings,
                project_root=Path(context.cwd),
                checkpointer=checkpointer,
                mode=context.mode,
            )

        modes = SessionModeState(
            current_mode_id="accept_edits",
            available_modes=[
                SessionMode(
                    id="ask_before_edits",
                    name="Ask before edits",
                    description="Ask before edits, plans, and shell execution.",
                ),
                SessionMode(
                    id="accept_edits",
                    name="Accept edits",
                    description="Auto-accept edits but ask before plans and shell execution.",
                ),
                SessionMode(
                    id="accept_everything",
                    name="Accept everything",
                    description="Auto-accept all tool calls.",
                ),
            ],
        )
        await run_acp_agent(AgentServerACP(agent=build_agent, modes=modes))
