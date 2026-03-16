# Deep Flo Documentation

> **Plan Visually, Execute Deeply**
>
> Deep Flo bridges Langflow (visual planning) and LangChain Deep Agents (execution)
> across the Python dependency boundary that prevents them sharing an environment.

---

## Start Here

| Document | What it covers |
|---|---|
| [QUICKSTART.md](QUICKSTART.md) | Get running in under 10 minutes — Docker or manual |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Why Deep Flo exists and how the pieces fit together |
| [API-REFERENCE.md](API-REFERENCE.md) | Runtime HTTP API endpoints, request/response schemas |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | Development setup, dual-venv workflow, PR process |

---

## The Core Problem

Langflow 1.8.x is pinned to **LangChain 0.3.x**.
Deep Agents requires **LangChain 1.2.x**.

These are incompatible — shared package names, different APIs, different class hierarchies.
No import tricks can bridge them in one Python process.

Deep Flo solves this by running each tool in its own environment and connecting them over HTTP.

---

## Component Map

```
deep-flo/
├── src/deep_flo_runtime/     # FastAPI bridge server (Deep Agents environment)
├── langflow_components/      # Custom Langflow nodes (Langflow environment)
├── deploy/                   # Docker Compose and Dockerfiles
├── examples/langflow/        # Example Langflow flow JSON files
├── tests/                    # Test suite (runtime + component tests, separate venvs)
└── docs/                     # This directory
```

---

## Key Decisions

- **Two venvs, always.** Runtime (`.[runtime]`) and Langflow (`.[langflow-dev]`) must never share a Python environment.
- **HTTP is the boundary.** The only way data crosses from Langflow to Deep Agents is through the runtime's REST API.
- **Apache 2.0.** This is an [Optimal Living Systems](https://github.com/Optimal-Living-Systems) nonprofit project. Free to use, fork, and build on.

---

```text
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   Built on Deep Agents · LangGraph · LangSmith · LangChain      ║
║                                                                  ║
║                  ★   LANGCHAIN RULES   ★                         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

*Built with [Claude Sonnet 4.6](https://www.anthropic.com) and Codex 5.4. All agent capabilities powered by [LangChain](https://github.com/langchain-ai).*
