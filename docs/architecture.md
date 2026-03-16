# Architecture

## Goal

DeepFlow exists because current `deepagents` and current Langflow do not belong in the same Python environment.

- Langflow `1.8.1` is pinned around LangChain `0.3.x`
- DeepFlow uses `deepagents 0.4.11` with LangChain `1.2.x`

The project keeps those worlds separate and connects them over a narrow interface.

## System shape

```text
Langflow UI / flows
        |
        | HTTP or MCP
        v
DeepFlow Runtime / Bridges
        |
        v
Deep Agents / LangGraph graph
        |
        +--> workspace filesystem
        +--> thread checkpoints (SQLite)
        +--> ACP editor bridge
        +--> MCP IDE / Langflow bridge
```

## Components

### DeepFlow Runtime

Files:
- [src/deepflow_runtime/runtime_api.py](../src/deepflow_runtime/runtime_api.py)
- [src/deepflow_runtime/agent.py](../src/deepflow_runtime/agent.py)
- [src/deepflow_runtime/tools.py](../src/deepflow_runtime/tools.py)

Responsibilities:
- exposes `/health`, `/invoke`, `/invoke/stream`, and `/threads/{thread_id}`
- creates the Deep Agents graph
- owns checkpoint persistence
- constrains the HTTP runtime to a bounded workspace

### DeepFlow CLI

File:
- [src/deepflow_runtime/cli.py](../src/deepflow_runtime/cli.py)

Responsibilities:
- `doctor`
- `serve`
- `run`
- `chat`
- `acp`

### ACP bridge

File:
- [src/deepflow_runtime/acp_server.py](../src/deepflow_runtime/acp_server.py)

Responsibilities:
- exposes DeepFlow to ACP-capable editors
- uses a shell-backed local project workflow
- applies human approval modes for risky operations

### Langflow bridge

File:
- [langflow_components/deepflow_runtime_component.py](../langflow_components/deepflow_runtime_component.py)

Responsibilities:
- gives Langflow a native node for DeepFlow
- keeps Langflow out of the Deep Agents dependency graph
- supports tool-oriented usage via `tool_mode`

### MCP bridge

File:
- [src/deepflow_runtime/mcp_server.py](../src/deepflow_runtime/mcp_server.py)

Responsibilities:
- exposes DeepFlow as MCP tools for IDEs and Langflow `MCP Tools`
- supports `stdio` and streamable HTTP transports
- reuses the runtime graph and checkpoint persistence

## Persistence

- LangGraph checkpoints in `data/threads.sqlite` (swappable to Postgres via `deploy/docker-compose.postgres.yml`)
- DeepFlow memory file in `memories/AGENTS.md`
- DeepFlow skill files in `skills/`
- Agent-created artifacts under `workspace/`

## Profiles

### HTTP runtime profile

- research-first
- bounded filesystem
- no shell execution exposed over HTTP

### ACP editor profile

- local shell backend
- user approval modes
- intended for coding/editor workflows


---

```text
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║      Built on Deep Agents · LangGraph · LangSmith · LangChain   ║
║                                                                  ║
║                    ★   LANGCHAIN RULES   ★                       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

*Built with [Claude Sonnet 4.6](https://www.anthropic.com) and Codex 5.4. All agent capabilities powered by [LangChain](https://github.com/langchain-ai).*
