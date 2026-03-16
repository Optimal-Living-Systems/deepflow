# AGENTS.md — Deep Flo

This file describes the Deep Flo project structure and conventions for AI coding agents (Claude Code, Copilot, Cursor, etc.).

---

## What This Project Is

Deep Flo is an HTTP bridge that lets Langflow (visual workflow builder, LangChain 0.3.x) call Deep Agents (LangChain 1.2.x) without a dependency conflict. The two services run in separate Python environments and communicate over HTTP.

**Two-service architecture:**
- **Deep Flo Runtime** (`src/deep_flo_runtime/`) — FastAPI server wrapping `create_deep_agent()`. Runs with deepagents + LangChain 1.x.
- **Langflow Component** (`langflow_components/`) — Custom Langflow node that calls the runtime over HTTP. Runs inside Langflow's LangChain 0.3.x environment.

These two environments **must never share a Python interpreter or venv.** This is the core constraint of the project.

---

## Repo Layout

```
src/deep_flo_runtime/       Runtime server (FastAPI, CLI, agent, MCP, ACP)
langflow_components/        Custom Langflow node (httpx only, no deepagents)
deploy/                     Docker Compose files and Dockerfiles
  docker-compose.stack.yml  Primary production stack (Postgres + runtime + MCP + Langflow)
  docker-compose.yml        Simpler two-service stack (runtime + Langflow, no Postgres)
  Dockerfile.deep-flo       Image for runtime and MCP services (uses uv, port 8011)
  Dockerfile.runtime        Older image (pip-based, port 8100) — kept for reference
tests/                      Pytest suite (39 tests)
docs/                       Architecture guides, API reference, quickstart
examples/langflow/          Example Langflow flows
memories/AGENTS.md          Runtime agent memory/instructions (read by the agent at startup)
skills/                     Deep Agents skills loaded by the runtime
scripts/                    Shell helpers for local dev
```

---

## Key Source Files

| File | Purpose |
|---|---|
| `src/deep_flo_runtime/runtime_api.py` | FastAPI app factory (`create_app()`), all HTTP endpoints |
| `src/deep_flo_runtime/cli.py` | Typer CLI (`deep-flo serve`, `run`, `chat`, `doctor`, `acp`, `mcp`) |
| `src/deep_flo_runtime/server.py` | Argparse CLI entry point (`deep-flo-runtime`) + uvicorn runner |
| `src/deep_flo_runtime/agent.py` | `build_runtime_agent()` and `build_acp_agent()` |
| `src/deep_flo_runtime/config.py` | `DeepFloSettings` (pydantic-settings, env prefix `DEEP_FLO_`) |
| `langflow_components/deep_flo_runtime_component.py` | The Langflow custom node |

---

## API Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/health` | None | Always public; returns `{"status": "healthy"}` |
| GET | `/ready` | None | 503 until agent graph is compiled |
| POST | `/run` | Bearer | Execute a prompt synchronously (preferred) |
| POST | `/invoke` | Bearer | Alias for `/run` |
| POST | `/stream` | Bearer | SSE streaming response (preferred) |
| POST | `/invoke/stream` | Bearer | Alias for `/stream` |
| GET | `/threads/{id}` | Bearer | Retrieve thread message history |

Auth is only enforced when `DEEP_FLO_API_KEY` is set. When unset, all endpoints are open.

---

## Environment Variables

All settings use the `DEEP_FLO_` prefix (from `config.py`).

| Variable | Default | Description |
|---|---|---|
| `DEEP_FLO_HOST` | `127.0.0.1` | Bind host for the runtime server |
| `DEEP_FLO_PORT` | `8011` | Bind port |
| `DEEP_FLO_MODEL` | auto | Model string (e.g. `anthropic:claude-sonnet-4-6`) |
| `DEEP_FLO_API_KEY` | unset | Bearer token for runtime auth |
| `DEEP_FLO_HOME_DIR` | repo root | Base directory for workspace, data, memories |
| `ANTHROPIC_API_KEY` | — | Required for Anthropic models |
| `OPENAI_API_KEY` | — | Required for OpenAI models |
| `GOOGLE_API_KEY` | — | Required for Google models |

---

## Running Tests

```bash
# Activate the runtime venv
source .venv/bin/activate  # or: uv run pytest

# Run all tests
pytest tests/

# Runtime tests only
pytest tests/test_runtime.py

# Component tests only (no deepagents needed)
pytest tests/test_components.py
```

Tests do **not** require any API keys or running services. Auth tests use in-process ASGI transport.

---

## Development Setup

```bash
# Runtime venv (for server work)
make install-runtime
source .venv-runtime/bin/activate

# Start the runtime locally
deep-flo serve                    # uses DEEP_FLO_PORT from .env, default 8011

# Full stack via Docker
docker compose -f deploy/docker-compose.stack.yml up
```

---

## Critical Constraints

1. **Never import `deepagents` in `langflow_components/`** — the component must only use `httpx`. The test `test_no_deepagents_import_in_components` enforces this.
2. **Never mix langflow and deepagents in the same venv** — they have incompatible LangChain versions.
3. **`langflow_components/` uses `langflow.*` imports** — not `lfx.*` or any other alias.
4. **The `require_api_key` auth dependency is a closure inside `create_app()`** — do not move it to module scope; it must close over the `runtime_settings` instance to work correctly in tests.
5. **`memories/AGENTS.md`** is the runtime agent's memory/instructions file, loaded at startup. It is not this file.

---

## Deep Flo Project Context

**What this project is:** Deep Flo is an HTTP bridge that allows LangChain Deep Agents (LangChain 1.2.x) to run inside Langflow (LangChain 0.3.x) by isolating the dependency conflict between the two versions.

**Architecture:**
- `src/deep_flo_runtime/` — FastAPI server running Deep Agents in an isolated Python environment
- `langflow_components/deep_flo_runtime_component.py` — Custom Langflow component that calls the runtime over HTTP
- `deploy/` — Docker Compose stack for one-command setup

**OLS Mission Context:** This project is built by Optimal Living Systems, a mutual aid nonprofit. It is the execution layer for the OLS Sociology Research System — a 7-stage autonomous research pipeline. All contributions should align with open science, privacy-respecting, and community-owned principles.

**Key commands for this repo:**
- `docker compose -f deploy/docker-compose.stack.yml up` — start the full stack
- `docker compose logs -f deep-flo-runtime` — watch runtime logs
- `python -m py_compile $(find . -name "*.py" -not -path './.venv/*')` — syntax check
- `pytest tests/` — run all 39 tests

**OpenSpec workflow:**
- `/opsx-propose` — propose a new change with full spec artifacts
- `/opsx-apply` — implement tasks from an open change
- `/opsx-explore` — think through ideas before committing to a change
- `/opsx-archive` — archive a completed change

**Current open OpenSpec change:** `deep-flo-sociology-research-system` — see `openspec/changes/deep-flo-sociology-research-system/`
