# Deep Flo Architecture

> Technical design document for contributors and evaluators.
> Last updated: 2026-03-15

## Table of Contents

- [Design Philosophy](#design-philosophy)
- [The Dependency Conflict](#the-dependency-conflict)
- [System Architecture](#system-architecture)
- [Component Details](#component-details)
- [Data Flow](#data-flow)
- [Isolation Strategy](#isolation-strategy)
- [Alternatives Considered](#alternatives-considered)
- [Future: When the Conflict Resolves](#future-when-the-conflict-resolves)

---

## Design Philosophy

Deep Flo follows three principles:

1. **Use each tool for its strength.** Langflow is a visual workflow designer. Deep Agents is a multi-step execution engine. Neither needs to become the other.

2. **Process isolation over in-process hacks.** Python cannot host two versions of the same package in one interpreter. We don't pretend otherwise. Separate processes, separate environments, clean HTTP boundary.

3. **Disappear gracefully.** When Langflow migrates to LangChain 1.x, the dependency conflict vanishes. Deep Flo is designed so that its bridge layer becomes optional without breaking anyone's workflows.

---

## The Dependency Conflict

### What's Happening

The Python ecosystem has a fundamental constraint: one interpreter, one version per package name. The `langchain` namespace can resolve to either 0.3.x or 1.2.x, never both.

```
Langflow 1.8.x
  └── langflow-base ~= 0.8.0
        └── langchain ~= 0.3.x    ← pinned to maintenance branch
              └── langchain-core ~= 0.3.x

Deep Agents 0.4.x (deepagents)
  └── langchain >= 1.2.x           ← requires current main line
        └── langchain-core >= 1.2.x
```

### Why It Can't Be Shimmed

Deep Agents uses LangChain 1.x APIs that don't exist in 0.3.x:

- `langchain.agents.middleware.AgentMiddleware` — the middleware system that Deep Agents' planning, filesystem, sub-agent, and summarization middleware all extend
- `langchain.agents.AgentState` — the typed state schema base class
- `langchain.chat_models.init_chat_model()` — the unified model initialization API
- `langchain.agents.create_agent()` — the agent factory that `create_deep_agent()` builds on

These aren't minor API differences. They represent a full architectural restructuring between LangChain 0.3.x and 1.x. A compatibility shim would need to reimplement the middleware stack, state management, and agent creation pipeline — effectively forking Deep Agents.

### Why It's Temporary

LangChain 0.3.x is a maintenance branch. The LangChain team's active development is on 1.x. Langflow will need to migrate eventually — they've already been patching langchain-core compatibility issues in recent releases. No migration timeline has been published as of March 2026.

---

## System Architecture

### Overview

```
┌──────────────────────────────────────────────────────────┐
│                    User's Machine                         │
│                                                          │
│  ┌────────────────────────┐  ┌────────────────────────┐  │
│  │   Langflow Process     │  │  Deep Flo Runtime      │  │
│  │   (Python venv A)      │  │  (Python venv B)       │  │
│  │                        │  │                        │  │
│  │  langflow 1.8.x        │  │  deepagents 0.4.x     │  │
│  │  langchain 0.3.x       │  │  langchain 1.2.x      │  │
│  │  langflow-base 0.8.x   │  │  langgraph 1.x        │  │
│  │                        │  │                        │  │
│  │  ┌──────────────────┐  │  │  ┌──────────────────┐  │  │
│  │  │ Deep Flo         │  │  │  │ FastAPI Server   │  │  │
│  │  │ Langflow         │──┼──┼──│                  │  │  │
│  │  │ Component        │  │  │  │ /run             │  │  │
│  │  │                  │◄─┼──┼──│ /stream          │  │  │
│  │  └──────────────────┘  │  │  │ /health          │  │  │
│  │                        │  │  └──────────────────┘  │  │
│  │  Port 7860             │  │  Port 8100             │  │
│  └────────────────────────┘  └────────────────────────┘  │
│                                                          │
│  OR: Docker Compose (each service = one container)       │
└──────────────────────────────────────────────────────────┘
```

### Docker Compose Deployment

```
┌─────────────────────────────────────────────┐
│              Docker Network                  │
│                                             │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │  langflow     │    │  deep-flo-       │   │
│  │  container    │───▶│  runtime         │   │
│  │              │    │  container       │   │
│  │  Port 7860   │    │  Port 8100       │   │
│  └──────────────┘    └──────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
     ▲
     │ http://localhost:7860
     │
   User
```

---

## Component Details

### Deep Flo Runtime Server

**Location:** `src/deep_flo_runtime/`

A lightweight FastAPI application that wraps the Deep Agents SDK. It runs in its own Python environment where `deepagents` and `langchain>=1.2` are installed without conflict.

**Responsibilities:**
- Accept task requests over HTTP
- Instantiate Deep Agents via `create_deep_agent()`
- Manage agent configuration (model, tools, system prompt, memory backend)
- Serialize agent responses back to JSON
- Provide health/readiness endpoints for orchestration

**Endpoints:**

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/run` | Execute a Deep Agent task, return full result |
| `POST` | `/stream` | Execute with server-sent events streaming |
| `GET` | `/health` | Returns runtime status, loaded model, version info |
| `GET` | `/ready` | Returns 200 only when the agent is initialized and ready |

**Configuration:** Via environment variables (see `.env.example`):
- `DEEP_FLO_MODEL` — Model identifier (default: `anthropic:claude-sonnet-4-20250514`)
- `DEEP_FLO_PORT` — Server port (default: `8100`)
- `DEEP_FLO_TOOLS` — Comma-separated list of tool modules to load
- `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc. — Model provider credentials

### Langflow Custom Component

**Location:** `langflow_components/`

A Python class that integrates with Langflow's component system. It appears as a node in Langflow's visual editor alongside native Langflow components.

**Responsibilities:**
- Provide UI fields for runtime URL, model selection, system prompt, and tool configuration
- Marshal Langflow message format into Deep Flo runtime request format
- Handle HTTP communication with the runtime (timeouts, retries, error display)
- Support both synchronous and streaming response modes
- Display agent output as standard Langflow message output

**From Langflow's perspective:** This is just another component. It takes a message input and produces a message output. The HTTP bridge is an implementation detail invisible to the flow designer.

### Skills

**Location:** `skills/`

Reusable agent capability definitions that can be loaded into Deep Agents. These follow the emerging Agent Skills specification and define tools, prompts, and behaviors that agents can use.

### Memories

**Location:** `memories/`

Persistent agent context and memory files. Deep Agents supports AGENTS.md-based memory loading and LangGraph's Memory Store for cross-thread persistence.

---

## Data Flow

### Synchronous Execution

```
1. User triggers flow in Langflow UI
2. Flow reaches Deep Flo Component node
3. Component POSTs to runtime:
   {
     "message": "Research the latest changes to...",
     "config": {
       "model": "anthropic:claude-sonnet-4-20250514",
       "system_prompt": "You are a research assistant.",
       "tools": ["web_search", "file_write"],
       "thread_id": "flow-abc-123"
     }
   }
4. Runtime creates/reuses Deep Agent with config
5. Deep Agent executes:
   - Plans tasks (write_todos)
   - Spawns sub-agents if needed (task tool)
   - Reads/writes to filesystem backend
   - Calls configured tools
   - Manages context via summarization
6. Runtime serializes result and returns:
   {
     "output": "Here is the research summary...",
     "metadata": {
       "steps": 12,
       "sub_agents_spawned": 2,
       "tokens_used": 8432
     }
   }
7. Component passes output to next Langflow node
```

### Streaming Execution

Same as above, but step 6 uses server-sent events (SSE). The Langflow component progressively displays agent output as it arrives. This is important for long-running Deep Agent tasks that may take minutes.

---

## Isolation Strategy

### Why HTTP Over Alternatives

| Approach | Works? | Tradeoffs |
|----------|--------|-----------|
| **HTTP bridge** (what we use) | Yes | Two processes to manage. Clean isolation. Easy debugging. Works with Docker. Stateless by default. |
| **Subprocess with separate venv** | Technically yes | Harder to manage venv discovery. Slower startup (~2-5s per spawn). Error propagation is painful. No streaming without extra plumbing. |
| **sys.path / importlib tricks** | No | Python's `sys.modules` is global. Two versions of `langchain` will collide on import, corrupt shared state, and produce silent type mismatches. |
| **Compatibility shim** | No | Would require reimplementing Deep Agents' middleware stack against 0.3.x APIs. Breaks on every upstream update. |
| **Monkeypatching** | No | Same `sys.modules` problem plus fragility. One internal import change breaks everything. |

The HTTP bridge is the standard industry pattern for dependency isolation. It's how ML serving systems (TorchServe, Triton, vLLM) handle incompatible dependency trees. We're not doing anything novel — we're applying proven infrastructure patterns.

---

## Future: When the Conflict Resolves

When Langflow migrates to LangChain 1.x:

1. **Deep Flo runtime becomes optional.** You could install `deepagents` directly in Langflow's environment and call `create_deep_agent()` in a native Langflow component without the HTTP bridge.

2. **The Langflow component could be simplified** to a thin wrapper around the Deep Agents SDK instead of an HTTP client.

3. **The visual planning pattern persists.** Even without the bridge, using Langflow to design workflows and Deep Agents to execute complex sub-tasks remains a valid architecture. The separation of visual design from deep execution isn't just a dependency workaround — it's a useful abstraction.

Deep Flo is designed to make this transition smooth. The component's interface to the rest of Langflow doesn't change regardless of whether the backend is HTTP or direct SDK calls.
