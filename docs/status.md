# Status

## Built

- isolated Deep Flo Python project
- Deep Flo runtime API
- Deep Flo CLI
- Deep Flo ACP entrypoint
- Deep Flo MCP server
- Langflow custom component
- Langflow example bridge flows
- portable launch scripts for ACP, MCP, and Langflow
- PostgreSQL bootstrap and local Langflow startup scripts
- Docker deployment files for Postgres and full stack
- editor integration docs, Zed ACP config example, and VS Code MCP workspace config
- memory and skill files
- startup scripts
- project tests
- upstream `deepagents-cli` installed and aligned to local `deepagents 0.4.11`
- provider wiring for OpenRouter and DeepSeek

## Verified

- `uv sync --extra dev`
- `uv run pytest`
- `uv run deep-flo --help`
- `uv run deep-flo doctor`
- import of the Langflow custom component from the Langflow environment
- runtime `/health` over a real localhost port
- live Anthropic Deep Flo run
- live OpenAI Deep Flo run
- live OpenRouter Deep Flo run
- live DeepSeek Deep Flo run
- live LangSmith project access and run visibility
- live Langflow component call into the Deep Flo runtime over HTTP
- live Langflow MCP utility discovery and invocation against Deep Flo
- ACP server boot
- live MCP server discovery and tool invocation over streamable HTTP
- Docker Compose parsing for Postgres-only and full-stack deployment files
- dynamic Deep Flo home/env path resolution
- live local Langflow database initialization against PostgreSQL
- live full Docker stack startup
- live containerized Langflow HTTP response

## Publish Ready

Deep Flo is ready to publish as a repository and ready to use locally.

The validated paths are:

- CLI via `deep-flo`
- IDE via VS Code MCP
- Langflow via the native Deep Flo runtime component
- Langflow via MCP-compatible tooling
- PostgreSQL-backed Langflow
- Dockerized stack deployment

## Optional Follow-On Work

- richer Langflow orchestration flows beyond the bridge examples
- a real ACP editor session from an ACP-native client such as Zed
- additional operator flow gallery examples

## Current blockers

- the supplied Google project is quota-blocked for `gemini-2.5-pro`


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
