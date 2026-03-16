```text
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   ██████╗ ███████╗███████╗██████╗ ███████╗██╗        ║
║   ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██║        ║
║   ██║  ██║█████╗  █████╗  ██████╔╝█████╗  ██║        ║
║   ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝  ██║        ║
║   ██████╔╝███████╗███████╗██║     ██║     ███████╗   ║
║   ╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝     ╚══════╝   ║
║                                                      ║
║         DeepFlow — Structured Integration Layer      ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

# DeepFlow

DeepFlow is a structured integration layer around LangChain's Deep Agents.

It exists for teams that want one Deep Agents runtime they can use from:

- a project-specific runtime API
- a project-specific CLI
- ACP-capable editors
- Langflow through a native custom component

DeepFlow does not replace Deep Agents. It packages, routes, and operationalizes them.

## What DeepFlow Is

DeepFlow is for the case where standalone `deepagents` is not enough by itself because you need:

- one shared Deep Agents runtime
- Langflow orchestration
- IDE access through MCP
- stable runtime boundaries between tools that do not belong in one Python environment
- a reproducible local and Docker deployment story

In practice, DeepFlow is a split-stack system:

- LangChain Deep Agents do the actual agent work
- LangGraph provides the runtime, checkpoints, interruptibility, and durable execution model
- LangSmith provides tracing and observability
- DeepFlow adds integration, packaging, deployment, and operator workflows around that stack

## Why DeepFlow Exists

Langflow `1.8.1` is pinned around LangChain `0.3.x`, while current Deep Agents requires LangChain `1.2.x`. Installing both into one environment is not a safe path.

DeepFlow solves that by:

- isolating Deep Agents in their own runtime
- exposing them to Langflow over HTTP and MCP instead of shared imports
- keeping CLI, IDE, and Langflow workflows pointed at the same runtime layer
- making the stack reproducible for local development and Docker deployment

## Why Use DeepFlow Instead Of Standalone Deep Agents

Use standalone Deep Agents when you want:

- a direct SDK workflow
- the upstream CLI only
- a single-purpose research or coding agent
- the fewest possible moving parts

Use DeepFlow when you want:

- Deep Agents plus Langflow in the same overall system
- a reusable runtime that multiple interfaces can share
- Langflow custom components and MCP-based orchestration
- Dockerized deployment
- a consistent project wrapper for memory, skills, MCP, tracing, and operations

The short version:

- `deepagents` is the agent harness
- DeepFlow is the integration and operations layer around that harness

## Primary Use Cases

- Visual orchestration in Langflow while keeping Deep Agents in a modern isolated environment
- One research runtime shared by CLI, IDE, and flow-based operator interfaces
- Team workflows that need reproducible startup, observability, and deployment
- A controlled bridge between long-horizon Deep Agents and UI-first orchestration systems

## Full Credit To LangChain

DeepFlow is built on top of LangChain's work and should be understood that way.

- Deep Agents is a LangChain project: [Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview)
- Deep Agents is implemented as the `deepagents` library from LangChain: [deepagents GitHub](https://github.com/langchain-ai/deepagents)
- LangGraph provides the runtime model Deep Agents uses for durable execution and stateful workflows: [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- LangSmith provides tracing and observability for LangChain and LangGraph applications: [LangSmith tracing](https://docs.langchain.com/langsmith/trace-with-langchain)

DeepFlow does not claim authorship of Deep Agents, LangChain, LangGraph, or LangSmith. Those belong to the LangChain team and community. DeepFlow is a packaging, orchestration, and deployment layer that makes those tools usable together in this project shape.

## What is built

- `DeepFlow Runtime`: FastAPI-based runtime with `/health`, `/invoke`, and `/invoke/stream` (SSE)
- `DeepFlow CLI`: `doctor`, `serve`, `run`, `chat`, `acp`, and `mcp`
- `DeepFlow ACP`: editor-facing ACP entrypoint
- `DeepFlow MCP`: IDE- and Langflow-facing MCP server over `stdio` or streamable HTTP
- `DeepFlow Langflow Bridge`: a Langflow custom component that calls the runtime over HTTP
- `DeepFlow Workspace`: memory, skills, workspace, and LangGraph checkpoint persistence

## Quick start

```bash
git clone https://github.com/Optimal-Living-Systems/deepflow
cd deepflow
make demo
```

`make demo` will copy `.env.example` → `.env` on first run and prompt you to add a provider key. Once `.env` has a key, re-run and the runtime starts at `http://127.0.0.1:8011`.

## Runtime API

```bash
# Blocking response
curl -s -X POST http://127.0.0.1:8011/invoke \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is LangGraph?", "thread_id": "demo"}' | jq .

# Streaming (SSE)
curl -N -X POST http://127.0.0.1:8011/invoke/stream \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is LangGraph?", "thread_id": "demo"}'

# Provider status
curl http://127.0.0.1:8011/health | jq .
```

Set `DEEPFLOW_API_KEY` in `.env` to require `Authorization: Bearer <key>` on `/invoke` and `/invoke/stream`. Leave it unset for local dev.

## Main commands

```bash
uv run deepflow serve
uv run deepflow run "Research the latest LangGraph release notes."
uv run deepflow chat
uv run deepflow acp
uv run deepflow mcp --transport stdio
```

Start Langflow with DeepFlow loaded:

```bash
./scripts/start_langflow.sh
```

Start both together:

```bash
./scripts/start_stack.sh
```

## Documentation

- [docs/index.md](docs/index.md)
- [docs/why-deepflow.md](docs/why-deepflow.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/setup.md](docs/setup.md)
- [docs/testing.md](docs/testing.md)
- [docs/workflows.md](docs/workflows.md)
- [docs/status.md](docs/status.md)
- [docs/roadmap.md](docs/roadmap.md)
- [deploy/README.md](deploy/README.md)
- [editor/README.md](editor/README.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)

## Current state

DeepFlow is publish-ready.

The core split-stack implementation is built, documented, and live-validated across:

- CLI
- IDE via MCP
- Langflow custom component integration
- Langflow MCP compatibility
- PostgreSQL-backed Langflow
- full Docker deployment

ACP support is included as an optional editor-facing path. The primary validated IDE path on this machine is VS Code through MCP.

## Notes

- DeepFlow now has first-class env/config support for Anthropic, OpenAI, Gemini, OpenRouter, DeepSeek, and Ollama.
- The current project default model is `anthropic:claude-sonnet-4-6`.
- LangSmith tracing is wired and verified against the default LangSmith US endpoint.
- Gemini support is wired correctly, but the supplied Google project is quota-blocked for `gemini-2.5-pro`.
- MCP is live-validated over streamable HTTP with `deepflow_status` and `deepflow_research`.
- PostgreSQL-backed local Langflow is live-validated.
- The full Docker stack is live-validated: Postgres, DeepFlow runtime, DeepFlow MCP, and Langflow.
- If `TAVILY_API_KEY` is missing, DeepFlow falls back to DuckDuckGo search via `ddgs`.
- The HTTP runtime is intentionally research-first and does not expose shell execution.
- The ACP profile is where local shell-backed coding workflows belong.
