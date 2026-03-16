from __future__ import annotations

import pytest

from deep_flo_runtime import mcp_server


def test_research_prompt_includes_topic() -> None:
    prompt = mcp_server.research_prompt("langgraph")
    assert "langgraph" in prompt
    assert "source-aware summary" in prompt


def test_run_mcp_server_rejects_invalid_transport() -> None:
    with pytest.raises(ValueError, match="transport must be 'stdio' or 'streamable-http'"):
        mcp_server.run_mcp_server(transport="invalid", host="127.0.0.1", port=8012)
