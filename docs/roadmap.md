# Roadmap

DeepFlow is a stable integration layer. These are the areas where it will grow.

## Near-term

- **Thread management API** — list and delete threads via `GET /threads` and `DELETE /threads/{thread_id}`
- **Langflow operator library** — documented patterns for common orchestration flows (research, summarize, multi-step)
- **VS Code MCP validation** — live-tested VS Code + MCP workflow documentation

## Medium-term

- **Auth modes** — per-thread API keys and optional JWT support for multi-user deployments
- **Postgres checkpointer** — first-class support for `langgraph-checkpoint-postgres` as a drop-in for SQLite
- **Streaming in Langflow component** — SSE passthrough from the custom component to Langflow's UI

## Longer-term

- **DeepFlow Hub** — shareable skills and memory profiles via a simple registry format
- **Observability dashboard** — structured log aggregation and LangSmith trace linking in one view
- **Multi-runtime support** — run multiple named runtimes with different model/tool configurations from one deployment

## Won't do

- Replace Deep Agents — DeepFlow is a packaging and integration layer, not an agent harness
- Monorepo with Langflow — dependency isolation is the whole point


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
