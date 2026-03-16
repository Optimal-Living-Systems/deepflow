# Why DeepFlow

## Summary

DeepFlow exists for one specific problem:

you want to use LangChain Deep Agents in a system that also needs Langflow, IDE access, deployment scripts, and a stable operator runtime.

If you only need Deep Agents by themselves, use standalone `deepagents`.

If you need a shared operational layer around Deep Agents, use DeepFlow.

## DeepFlow vs Standalone Deep Agents

### Use standalone Deep Agents when

- you want the upstream SDK directly
- you want the upstream CLI directly
- you are building one focused agent application
- you do not need Langflow in the same stack
- you want the smallest possible surface area

### Use DeepFlow when

- you want Langflow and Deep Agents in one system
- you need one runtime shared by CLI, IDE, and flow interfaces
- you want MCP access for IDEs and Langflow
- you need Docker and PostgreSQL deployment support
- you want a project wrapper for memory, skills, tracing, and operator workflows

## What DeepFlow Adds

DeepFlow adds:

- an isolated Deep Agents runtime
- a project CLI
- a Langflow custom component
- an MCP server for IDE and Langflow consumption
- startup and deployment scripts
- PostgreSQL-backed Langflow options
- Dockerized stack definitions
- shared docs and examples

It does not replace the LangChain agent runtime. It operationalizes it.

## Architectural Reason

The concrete technical reason this repo exists is dependency separation.

- current Langflow `1.8.1` is pinned around LangChain `0.3.x`
- current Deep Agents requires LangChain `1.2.x`

DeepFlow keeps those stacks out of the same Python environment and connects them over explicit runtime boundaries instead.

## Credits

DeepFlow is built on top of LangChain projects and gives them full credit.

- Deep Agents overview: <https://docs.langchain.com/oss/python/deepagents/overview>
- Deep Agents source: <https://github.com/langchain-ai/deepagents>
- LangGraph overview: <https://docs.langchain.com/oss/python/langgraph/overview>
- LangSmith tracing: <https://docs.langchain.com/langsmith/trace-with-langchain>

DeepFlow should be understood as a project-level wrapper and integration layer around those systems.


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
