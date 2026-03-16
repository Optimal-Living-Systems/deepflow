# Changelog

All notable changes to DeepFlow are documented here.

## 0.1.0 (2026-03-16)

Initial public release.

### Added

- **HTTP bridge runtime** — FastAPI server wrapping LangChain Deep Agents SDK in an isolated Python environment
- **REST API** — `/health`, `/ready`, `/run`, `/stream` endpoints with optional Bearer token auth
- **SSE streaming** — `/stream` and `/invoke/stream` return server-sent events as tokens are generated
- **Thread history** — `GET /threads/{thread_id}` returns full conversation history
- **Custom Langflow component** — drop-in node for Langflow visual workflows that calls the runtime over HTTP
- **MCP server** — `deepflow_status` and `deepflow_research` tools over stdio or streamable HTTP
- **ACP editor bridge** — coding-oriented agent profile for ACP-capable editors (Zed, etc.)
- **Docker Compose stack** — one-command setup for runtime + Langflow as sibling containers
- **Multi-provider support** — Anthropic, OpenAI, Google, OpenRouter, DeepSeek, Ollama
- **LangSmith tracing** — wired and verified against the default LangSmith US endpoint
- **GitHub Actions CI** — lint (ruff), test matrix (Python 3.11/3.12/3.13), Docker build verification
- **Documentation** — ARCHITECTURE.md, QUICKSTART.md, API-REFERENCE.md, docs INDEX

### Architecture

DeepFlow solves a hard Python packaging constraint: Deep Agents requires LangChain 1.2.x while Langflow 1.8.x is pinned to LangChain 0.3.x. These cannot coexist in one Python interpreter. DeepFlow runs each in its own environment and connects them over HTTP.

> Built on [Deep Agents](https://github.com/langchain-ai/deepagents) · [LangGraph](https://github.com/langchain-ai/langgraph) · [LangSmith](https://smith.langchain.com) · [LangChain](https://github.com/langchain-ai/langchain)
> **LangChain rules.**
