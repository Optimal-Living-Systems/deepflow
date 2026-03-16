# Status

## Built

- isolated DeepFlow Python project
- DeepFlow runtime API
- DeepFlow CLI
- DeepFlow ACP entrypoint
- DeepFlow MCP server
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
- `uv run deepflow --help`
- `uv run deepflow doctor`
- import of the Langflow custom component from the Langflow environment
- runtime `/health` over a real localhost port
- live Anthropic DeepFlow run
- live OpenAI DeepFlow run
- live OpenRouter DeepFlow run
- live DeepSeek DeepFlow run
- live LangSmith project access and run visibility
- live Langflow component call into the DeepFlow runtime over HTTP
- live Langflow MCP utility discovery and invocation against DeepFlow
- ACP server boot
- live MCP server discovery and tool invocation over streamable HTTP
- Docker Compose parsing for Postgres-only and full-stack deployment files
- dynamic DeepFlow home/env path resolution
- live local Langflow database initialization against PostgreSQL
- live full Docker stack startup
- live containerized Langflow HTTP response

## Publish Ready

DeepFlow is ready to publish as a repository and ready to use locally.

The validated paths are:

- CLI via `deepflow`
- IDE via VS Code MCP
- Langflow via the native DeepFlow runtime component
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
