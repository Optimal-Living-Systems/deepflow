# DeepFlow

[![CI](https://github.com/Optimal-Living-Systems/deepflow/actions/workflows/ci.yml/badge.svg)](https://github.com/Optimal-Living-Systems/deepflow/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**A structured integration layer between Langflow (visual planning) and LangChain Deep Agents (execution)**

Built by [Optimal Living Systems](https://github.com/Optimal-Living-Systems) · Apache 2.0

---

## Why DeepFlow Exists

LangChain's [Deep Agents](https://github.com/langchain-ai/deepagents) framework is a powerful execution engine for complex, multi-step AI tasks — planning, sub-agent delegation, filesystem operations, and long-horizon reasoning. [Langflow](https://github.com/langflow-ai/langflow) is the leading visual workflow builder for LangChain applications.

They cannot run in the same Python environment.

Deep Agents requires **LangChain 1.2.x**. Langflow 1.8.x is pinned to **LangChain 0.3.x** through its `langflow-base` dependency. These are incompatible version trees — they share package names but have different APIs, different class hierarchies, and different runtime expectations. No amount of import tricks or shims can make them coexist in a single Python interpreter. This is a hard constraint of Python's packaging model, not a limitation that can be engineered around.

DeepFlow solves this by using each tool for what it does best.

## Architecture: Plan Visually, Execute Deeply

DeepFlow treats Langflow and Deep Agents as complementary layers with distinct roles:

| Layer | Tool | Role |
|---|---|---|
| **Visual Planning** | Langflow | Design workflows, configure agents, map data flow, iterate on architecture |
| **Execution Bridge** | DeepFlow Runtime | HTTP API that translates Langflow workflow definitions into Deep Agents invocations |
| **Deep Execution** | Deep Agents CLI/SDK | Runs complex multi-step tasks with planning, sub-agents, filesystem access, and memory |

```
┌──────────────────────────────────┐
│         Langflow (UI)            │
│   Visual workflow design &       │
│   orchestration planning         │
│                                  │
│   ┌──────────────────────────┐   │
│   │   DeepFlow Component     │   │
│   │   (custom Langflow node) │   │
│   └───────────┬──────────────┘   │
└───────────────┼──────────────────┘
                │ HTTP (JSON)
┌───────────────┼──────────────────┐
│   DeepFlow Runtime Server        │
│   (isolated Python environment)  │
│                                  │
│   ┌──────────────────────────┐   │
│   │   Deep Agents SDK        │   │
│   │   create_deep_agent()    │   │
│   │   Planning, sub-agents,  │   │
│   │   filesystem, memory     │   │
│   └──────────────────────────┘   │
└──────────────────────────────────┘
```

**Langflow is the planner, not the executor.** You design and visualize your agent workflows in Langflow's drag-and-drop interface. When a flow triggers a Deep Agents task, DeepFlow bridges the call to an isolated runtime where Deep Agents has full access to its native capabilities — planning tools, sub-agent spawning, filesystem backends, and conversation summarization.

For direct Deep Agents work (coding tasks, deep research, interactive sessions), use the **Deep Agents CLI or SDK directly** in your terminal or IDE. DeepFlow does not attempt to replace that workflow. It adds a visual planning and orchestration layer on top of it.

## Why Not Just Wait for Langflow to Upgrade?

Langflow will eventually migrate to LangChain 1.x — the 0.3.x line is a maintenance branch. When that happens, `pip install langflow deepagents` may just work, and the dependency isolation problem disappears.

DeepFlow exists because that migration hasn't happened yet, and there's no published timeline. If you need Deep Agents capabilities in a Langflow-orchestrated workflow today, DeepFlow is how you get there.

When the upstream conflict resolves, DeepFlow's HTTP bridge becomes optional — but the visual planning pattern it establishes remains useful regardless.

## Quick Start

### Option 1: Docker (recommended)

```bash
git clone https://github.com/Optimal-Living-Systems/deepflow.git
cd deepflow
cp .env.example .env
# Edit .env with your API keys

docker compose up
```

This starts both Langflow and the DeepFlow runtime as sibling containers. Langflow is available at `http://localhost:7860`.

### Option 2: Manual (two virtual environments)

```bash
# Terminal 1: DeepFlow Runtime
python -m venv .venv-runtime
source .venv-runtime/bin/activate
pip install -e ".[runtime]"
deepflow-runtime serve --port 8100

# Terminal 2: Langflow
python -m venv .venv-langflow
source .venv-langflow/bin/activate
pip install langflow
# Install the DeepFlow custom component
cp langflow_components/*.py ~/.langflow/components/
langflow run
```

### Option 3: Deep Agents CLI Only (no Langflow)

If you don't need visual planning and just want Deep Agents:

```bash
pip install deepagents
deepagents  # Interactive terminal agent
```

DeepFlow is not required for standalone Deep Agents usage.

## Project Structure

```
deepflow/
├── src/deepflow_runtime/     # FastAPI server wrapping Deep Agents SDK
├── langflow_components/      # Custom Langflow nodes for DeepFlow integration
├── deploy/                   # Docker Compose and deployment configs
├── docs/                     # Architecture docs and guides
├── examples/langflow/        # Example Langflow flows using DeepFlow
├── skills/                   # Deep Agents skills (reusable agent capabilities)
├── memories/                 # Agent memory/context persistence
├── editor/                   # Editor integration configs
├── scripts/                  # Setup and utility scripts
└── tests/                    # Test suite
```

## How It Works

### The DeepFlow Runtime

A lightweight FastAPI server that runs in its own Python environment with `deepagents` and `langchain>=1.2` installed. It exposes:

- `POST /run` — Execute a Deep Agent task synchronously
- `POST /stream` — Execute with streaming response
- `GET /health` — Runtime health check

The runtime wraps `create_deep_agent()` and handles model configuration, tool registration, and result serialization.

### The Langflow Component

A custom Langflow node (`DeepFlowAgent`) that appears in Langflow's component palette. It provides UI fields for:

- Runtime URL (default: `http://localhost:8100`)
- Model selection (any LangChain-compatible model)
- System prompt
- Tools configuration
- Memory/thread management

From Langflow's perspective, it's a standard component that takes a message and returns a message. The HTTP bridge is invisible to the flow designer.

## The Dependency Conflict Explained

For technical readers who want the full picture:

- **LangChain 1.x** (current main line): Introduced `langchain.agents.middleware`, `AgentMiddleware`, `AgentState`, restructured `langchain.chat_models`, and the `create_agent()` / `create_deep_agent()` APIs. Deep Agents is built entirely on these 1.x APIs.

- **LangChain 0.3.x** (maintenance branch): The API surface that Langflow's internals depend on — different class hierarchies, different import paths, different runtime behavior.

- **Python's constraint**: A single Python process can only have one version of a package loaded. You cannot `import langchain` and get 0.3.x in one module and 1.2.x in another. The interpreter's module cache (`sys.modules`) is global.

This is why DeepFlow uses process-level isolation (separate server, separate venv) rather than attempting any in-process bridging. It's the same pattern used by every production ML system that needs incompatible dependency trees — microservice isolation over monolithic packaging.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

DeepFlow is an [Optimal Living Systems](https://github.com/Optimal-Living-Systems) project — a mutual aid nonprofit building open-source AI infrastructure for community benefit. Contributions are welcome from developers of all levels.

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.

## Status

**Early development.** The HTTP bridge works. The Langflow component works. Documentation and packaging are actively being improved. This project exists to solve a real problem while the upstream ecosystem catches up.

If Langflow migrates to LangChain 1.x and this project becomes unnecessary, that's a good outcome.

---

> **Built on the shoulders of giants.**
> DeepFlow is a community integration layer — not a LangChain product.
> All core agent capabilities belong to the LangChain team.
> [Deep Agents](https://github.com/langchain-ai/deepagents) · [LangGraph](https://github.com/langchain-ai/langgraph) · [LangSmith](https://smith.langchain.com) · [LangChain](https://github.com/langchain-ai/langchain)

```text
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   Built on Deep Agents · LangGraph · LangSmith · LangChain      ║
║                                                                  ║
║                  ★   LANGCHAIN RULES   ★                         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

*Built with [Claude Sonnet 4.6](https://www.anthropic.com) and Codex 5.4.*
