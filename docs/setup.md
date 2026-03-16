# Setup

## Prerequisites

- Python `3.11+`
- `uv`
- one model provider:
  - `ANTHROPIC_API_KEY`
  - `OPENAI_API_KEY`
  - `GOOGLE_API_KEY`
  - `OPENROUTER_API_KEY`
  - `DEEPSEEK_API_KEY`
  - or a reachable Ollama server with `DEEPFLOW_MODEL=ollama:<model-name>`

Optional:
- `TAVILY_API_KEY`
- `LANGSMITH_API_KEY`

## Fresh install

```bash
cd /path/to/deepflow
uv sync --extra dev
```

If `.env` does not exist yet:

```bash
cp .env.example .env
```

Then edit `.env` and add your provider keys.

The project default model is:

```env
DEEPFLOW_MODEL=anthropic:claude-sonnet-4-6
```

Override it per command if needed:

```bash
DEEPFLOW_MODEL='openrouter:anthropic/claude-sonnet-4.5' uv run deepflow run "Hello"
```

## Core commands

```bash
cd /path/to/deepflow
uv run deepflow doctor
uv run deepflow serve
uv run deepflow run "Research LangGraph and summarize the latest changes."
uv run deepflow chat
uv run deepflow acp
uv run deepflow mcp --transport stdio
```

## Langflow integration

Start Langflow with the DeepFlow component path:

```bash
./scripts/start_langflow.sh
```

This sets:

- `LANGFLOW_COMPONENTS_PATH=<deepflow-root>/langflow_components`
- `DEEPFLOW_RUNTIME_URL=http://127.0.0.1:8011`

If Langflow is not checked out as a sibling directory, set:

```bash
export LANGFLOW_ROOT=/absolute/path/to/langflow
```

## Full stack startup

```bash
./scripts/start_stack.sh
```

This starts:
- DeepFlow runtime
- Langflow with the bundled DeepFlow component path

## PostgreSQL-backed local Langflow

Start PostgreSQL:

```bash
./scripts/start_postgres.sh
```

Then run local Langflow from source against Postgres:

```bash
./scripts/start_langflow_postgres.sh
```

If the local Langflow environment is missing a working PostgreSQL client backend, install:

```bash
cd /path/to/langflow
uv pip install 'psycopg[binary]'
```

Default local Postgres URL:

```env
LANGFLOW_DATABASE_URL=postgresql://langflow:langflow@127.0.0.1:55433/langflow
```

Override the published Docker host port if needed:

```bash
export LANGFLOW_POSTGRES_PORT=55433
```

## MCP startup

STDIO transport:

```bash
./scripts/start_mcp_stdio.sh
```

Streamable HTTP transport:

```bash
./scripts/start_mcp_http.sh
```

Optional:

```bash
export DEEPFLOW_MCP_HOST=127.0.0.1
export DEEPFLOW_MCP_PORT=8012
```

## ACP editor setup

Start ACP:

```bash
./scripts/start_acp.sh
```

For editor setup details, see [editor/README.md](../editor/README.md).

For Zed, start from [editor/zed-settings.example.json](../editor/zed-settings.example.json) and replace the placeholder path with your real checkout path.

## VS Code MCP setup

Open the DeepFlow repo in VS Code and use the workspace config at [.vscode/mcp.json](../.vscode/mcp.json).

This starts DeepFlow over MCP `stdio` using:

```bash
./scripts/start_mcp_stdio.sh
```

## Langflow MCP Tools setup

DeepFlow can also be consumed through Langflow's `MCP Tools` path.

Recommended server config:

```json
{
  "mode": "Streamable_HTTP",
  "url": "http://127.0.0.1:8012/mcp",
  "verify_ssl": true
}
```

Start the server first:

```bash
./scripts/start_mcp_http.sh
```

## Dockerized stack

Start the full container stack:

```bash
./scripts/start_compose_stack.sh
```

Stop it:

```bash
./scripts/stop_compose_stack.sh
```

Files:
- [deploy/Dockerfile.deepflow](../deploy/Dockerfile.deepflow)
- [deploy/docker-compose.postgres.yml](../deploy/docker-compose.postgres.yml)
- [deploy/docker-compose.stack.yml](../deploy/docker-compose.stack.yml)
- [deploy/README.md](../deploy/README.md)


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
