# Deep Flo Quickstart Guide

> Get Deep Flo running in under 10 minutes.

---

## Prerequisites

- **Docker Desktop** (for Docker path) or **Python 3.11+** and **uv** (for manual path)
- An API key for at least one LLM provider (Anthropic, OpenAI, or Google)
- Git

---

## Path 1: Docker Compose (Recommended)

This is the fastest way to get both Langflow and the Deep Flo runtime running.

### Step 1: Clone and configure

```bash
git clone https://github.com/Optimal-Living-Systems/deep_flo.git
cd deep-flo
cp .env.example .env
```

### Step 2: Add your API key

Open `.env` and set at least one provider key:

```env
# Required: at least one of these
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Optional: customize the model
DEEP_FLO_MODEL=anthropic:claude-sonnet-4-20250514
DEEP_FLO_PORT=8100
```

### Step 3: Start the stack

```bash
docker compose up
```

Wait for both services to report healthy. You'll see:

```
deep-flo-runtime  | INFO:     Uvicorn running on http://0.0.0.0:8100
langflow          | ╭───────────────────────────────────────────────╮
langflow          | │ Welcome to ⛓ Langflow                        │
langflow          | │ Access http://0.0.0.0:7860                    │
langflow          | ╰───────────────────────────────────────────────╯
```

### Step 4: Verify the bridge

```bash
curl http://localhost:8100/health
```

Expected response:

```json
{
  "status": "healthy",
  "model": "anthropic:claude-sonnet-4-20250514",
  "deepagents_version": "0.4.8",
  "langchain_version": "1.2.12"
}
```

### Step 5: Open Langflow

Navigate to `http://localhost:7860` in your browser. The Deep Flo component should be available in the component palette under **Agents**.

---

## Path 2: Manual Installation (Two Virtual Environments)

Use this if you want more control or can't run Docker.

### Step 1: Clone

```bash
git clone https://github.com/Optimal-Living-Systems/deep_flo.git
cd deep-flo
```

### Step 2: Set up the Deep Flo Runtime (Terminal 1)

```bash
# Create isolated environment for Deep Agents
python3 -m venv .venv-runtime
source .venv-runtime/bin/activate

# Install the runtime
pip install -e ".[runtime]"

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Start the runtime server
deep-flo-runtime serve --port 8100
```

Leave this terminal running. The runtime is now listening on `http://localhost:8100`.

### Step 3: Set up Langflow (Terminal 2)

```bash
# Create isolated environment for Langflow
python3 -m venv .venv-langflow
source .venv-langflow/bin/activate

# Install Langflow
pip install langflow

# Install the Deep Flo custom component
cp langflow_components/*.py ~/.langflow/components/

# Start Langflow
langflow run
```

### Step 4: Verify both services

```bash
# Check the runtime
curl http://localhost:8100/health

# Check Langflow
curl http://localhost:7860/health
```

---

## Path 3: Deep Agents CLI Only (No Langflow)

If you only need Deep Agents execution without visual planning:

```bash
# Install Deep Agents directly
pip install deepagents

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Launch interactive terminal agent
deepagents
```

Deep Flo is not required for this path. Use it when you want to work with Deep Agents directly in your terminal or IDE.

---

## Your First Flow

### Import the example flow

1. Open Langflow at `http://localhost:7860`
2. Click **Import** (or drag and drop)
3. Select `examples/langflow/deep-flo-research-example.json`
4. The flow loads with a Deep Flo Agent component pre-configured

### Run it

1. Open the **Playground** panel
2. Type a message: `Research the current state of mutual aid networks in the United States`
3. The message routes through the flow to the Deep Flo component
4. The component calls the runtime, which creates a Deep Agent
5. The agent plans, researches, and returns a structured response
6. The response appears in the Playground

### What's happening under the hood

```
Your message
  → Langflow routes to Deep Flo Component
    → HTTP POST to localhost:8100/run
      → Deep Agent plans tasks (write_todos)
      → Deep Agent executes research steps
      → Deep Agent writes findings to filesystem
      → Deep Agent summarizes and returns
    ← JSON response
  ← Component outputs to Langflow
Response displayed
```

---

## Troubleshooting

### "Connection refused" on port 8100

The Deep Flo runtime isn't running. Start it first:

```bash
# Docker
docker compose up deep-flo-runtime

# Manual
source .venv-runtime/bin/activate
deep-flo-runtime serve --port 8100
```

### "No API key found"

Deep Agents needs a model provider key. Set it in `.env` (Docker) or as an environment variable (manual):

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### Langflow can't find the Deep Flo component

Ensure the component files are in the right location:

```bash
# Check Langflow's custom components directory
ls ~/.langflow/components/

# If empty, copy them
cp langflow_components/*.py ~/.langflow/components/

# Restart Langflow
langflow run
```

### "ModuleNotFoundError: No module named 'deepagents'"

You're trying to import deepagents in Langflow's environment. This won't work — deepagents requires langchain 1.x which conflicts with Langflow. The Deep Flo runtime handles this by running deepagents in a separate environment. Make sure the runtime is running.

### Port conflicts

Change ports in `.env`:

```env
DEEP_FLO_PORT=8200       # Runtime port
LANGFLOW_PORT=7861       # Langflow port (set via langflow run --port 7861)
```

---

## Next Steps

- Read the [Architecture doc](ARCHITECTURE.md) for the full technical design
- Explore [example flows](../examples/langflow/) for more use cases
- Check the [API Reference](API-REFERENCE.md) for runtime endpoint details
- See [CONTRIBUTING.md](../CONTRIBUTING.md) to get involved
