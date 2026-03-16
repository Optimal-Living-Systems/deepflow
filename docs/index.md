```text
╔═════════════════════════════════════════════════════════════════════════╗
║                                                                         ║
║   ██████╗ ███████╗███████╗██████╗ ███████╗██╗      ██████╗ ██╗    ██╗  ║
║   ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██║     ██╔═══██╗██║    ██║  ║
║   ██║  ██║█████╗  █████╗  ██████╔╝█████╗  ██║     ██║   ██║██║ █╗ ██║  ║
║   ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝  ██║     ██║   ██║██║███╗██║  ║
║   ██████╔╝███████╗███████╗██║     ██║     ███████╗╚██████╔╝╚███╔███╔╝  ║
║   ╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝  ║
║                                                                         ║
║                 DeepFlow — Structured Integration Layer                 ║
║                                                                         ║
╚═════════════════════════════════════════════════════════════════════════╝
```

# Docs Index

## What DeepFlow Is

DeepFlow is a structured Deep Agents system for teams that want one runtime reachable from CLI, IDE, Langflow, and Docker.

It is not a new agent framework. It is an operational wrapper around LangChain's Deep Agents.

## Why DeepFlow Exists

This project exists because the current Deep Agents stack and the current Langflow stack do not fit safely into one Python environment.

DeepFlow resolves that by separating concerns:

- Deep Agents run in an isolated runtime
- Langflow talks to that runtime over explicit boundaries
- MCP and HTTP make the same DeepFlow runtime reachable from IDEs and flow tools

## Why Use It Instead Of Standalone Deep Agents

Standalone Deep Agents is the right choice when:

- you only need the upstream SDK or CLI
- you are not integrating with Langflow
- you do not need a shared operator runtime

DeepFlow is the right choice when:

- you need Langflow and Deep Agents in one system
- you want a shared runtime for CLI, IDE, and visual orchestration
- you want deployment scripts, Docker, tracing, and reproducible startup

## Core Positioning

- Deep Agents is the agent harness
- LangGraph is the runtime foundation
- LangSmith is the tracing layer
- DeepFlow is the integration and operations layer

## Credits

DeepFlow builds directly on LangChain projects and gives them full credit.

- Deep Agents overview: <https://docs.langchain.com/oss/python/deepagents/overview>
- LangGraph overview: <https://docs.langchain.com/oss/python/langgraph/overview>
- LangSmith tracing: <https://docs.langchain.com/langsmith/trace-with-langchain>
- Deep Agents source: <https://github.com/langchain-ai/deepagents>

DeepFlow should be read as a project-specific wrapper around those systems, not as a replacement for them.

> **Disclaimer:** DeepFlow is not a LangChain product. It is a community integration layer built entirely on top of LangChain's open-source work. All core agent capabilities — Deep Agents, LangGraph, and LangSmith — belong to the LangChain team. DeepFlow adds packaging, routing, and operations around their work, and nothing more.

## Documentation Map

- [Why DeepFlow](why-deepflow.md)
- [Architecture](architecture.md)
- [Setup](setup.md)
- [Testing](testing.md)
- [Workflows](workflows.md)
- [Status](status.md)
- [Roadmap](roadmap.md)

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
