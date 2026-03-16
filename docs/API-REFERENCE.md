# Deep Flo Runtime API Reference

> HTTP API exposed by the Deep Flo runtime server (`src/deep_flo_runtime/`).
> Default base URL: `http://localhost:8100`

---

## Endpoints

### POST /run

Execute a Deep Agent task synchronously. Blocks until the agent completes.

**Request:**

```json
{
  "message": "Research the latest developments in cooperative economics",
  "config": {
    "model": "anthropic:claude-sonnet-4-20250514",
    "system_prompt": "You are a research assistant specializing in mutual aid and cooperative economics.",
    "tools": ["web_search"],
    "thread_id": "optional-thread-id-for-memory",
    "max_steps": 50
  }
}
```

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | The user message / task description |
| `config.model` | string | No | LangChain model identifier. Format: `provider:model-name`. Default: uses `DEEP_FLO_MODEL` env var |
| `config.system_prompt` | string | No | Custom system prompt for the agent |
| `config.tools` | string[] | No | List of tool names to enable. Default: all configured tools |
| `config.thread_id` | string | No | Thread ID for conversation persistence. Omit for stateless execution |
| `config.max_steps` | integer | No | Maximum agent loop iterations. Default: 50 |

**Response (200):**

```json
{
  "output": "Based on my research, here are the key developments in cooperative economics...",
  "metadata": {
    "steps": 8,
    "sub_agents_spawned": 1,
    "tokens_used": 4215,
    "model": "anthropic:claude-sonnet-4-20250514",
    "thread_id": "optional-thread-id-for-memory",
    "duration_seconds": 12.4
  }
}
```

**Error Response (4xx/5xx):**

```json
{
  "error": "description of what went wrong",
  "code": "AGENT_ERROR",
  "details": {
    "step": 5,
    "tool": "web_search",
    "original_error": "..."
  }
}
```

**Error Codes:**

| Code | HTTP Status | Meaning |
|------|-------------|---------|
| `INVALID_REQUEST` | 400 | Missing required fields or malformed JSON |
| `MODEL_NOT_FOUND` | 400 | Requested model identifier not recognized |
| `NO_API_KEY` | 401 | Required provider API key not set |
| `AGENT_ERROR` | 500 | Agent encountered an error during execution |
| `TIMEOUT` | 504 | Agent exceeded maximum execution time |

---

### POST /stream

Execute a Deep Agent task with streaming output via server-sent events (SSE).

**Request:** Same as `/run`.

**Response:** `text/event-stream`

```
event: status
data: {"step": 1, "action": "planning", "detail": "Creating task list..."}

event: status
data: {"step": 2, "action": "tool_call", "tool": "web_search", "detail": "Searching..."}

event: token
data: {"text": "Based on "}

event: token
data: {"text": "my research, "}

event: token
data: {"text": "here are the key developments..."}

event: done
data: {"metadata": {"steps": 8, "tokens_used": 4215, "duration_seconds": 12.4}}
```

**Event Types:**

| Event | Purpose |
|-------|---------|
| `status` | Agent lifecycle updates (planning, tool calls, sub-agent spawns) |
| `token` | Incremental text output from the agent |
| `error` | Error during execution (stream closes after) |
| `done` | Final event with execution metadata |

---

### GET /health

Returns runtime status. Use for monitoring and Docker health checks.

**Response (200):**

```json
{
  "status": "healthy",
  "model": "anthropic:claude-sonnet-4-20250514",
  "deepagents_version": "0.4.8",
  "langchain_version": "1.2.12",
  "uptime_seconds": 3421,
  "tools_loaded": ["web_search", "file_write", "file_read"]
}
```

---

### GET /ready

Returns 200 only when the agent is fully initialized and ready to accept requests. Returns 503 during startup.

Use this as a Kubernetes/Docker readiness probe.

**Response (200):**

```json
{
  "ready": true
}
```

**Response (503):**

```json
{
  "ready": false,
  "reason": "Agent initializing..."
}
```

---

## Configuration

All configuration is via environment variables. Set them in `.env` (Docker) or export them (manual).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEEP_FLO_PORT` | `8100` | Port for the runtime server |
| `DEEP_FLO_MODEL` | `anthropic:claude-sonnet-4-20250514` | Default model for agent creation |
| `DEEP_FLO_MAX_STEPS` | `50` | Default max agent loop iterations |
| `DEEP_FLO_TIMEOUT` | `300` | Request timeout in seconds |
| `DEEP_FLO_LOG_LEVEL` | `INFO` | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `ANTHROPIC_API_KEY` | — | Anthropic API key |
| `OPENAI_API_KEY` | — | OpenAI API key |
| `GOOGLE_API_KEY` | — | Google Gemini API key |

Per-request `config` fields override environment defaults.

---

## Usage from Langflow

The Deep Flo Langflow Component handles HTTP communication automatically. You configure it via the Langflow UI:

1. Drag the **Deep Flo Agent** component into your flow
2. Set **Runtime URL** to `http://localhost:8100` (or your deployment URL)
3. Configure model, system prompt, and tools via the component's input fields
4. Connect input/output edges like any other Langflow component

The component calls `/run` by default and `/stream` when streaming mode is enabled in the flow.

---

## Usage from curl

```bash
# Simple task
curl -X POST http://localhost:8100/run \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Self-Determination Theory?"}'

# With full config
curl -X POST http://localhost:8100/run \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Research SDT applications in community organizing",
    "config": {
      "model": "anthropic:claude-sonnet-4-20250514",
      "system_prompt": "You are a sociology research assistant.",
      "thread_id": "sdt-research-001"
    }
  }'

# Streaming
curl -N http://localhost:8100/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Write a summary of mutual aid principles"}'

# Health check
curl http://localhost:8100/health
```

---

## Usage from Python

```python
import httpx

runtime = "http://localhost:8100"

# Synchronous
response = httpx.post(f"{runtime}/run", json={
    "message": "Research cooperative economics",
    "config": {"model": "anthropic:claude-sonnet-4-20250514"}
})
result = response.json()
print(result["output"])

# Streaming
with httpx.stream("POST", f"{runtime}/stream", json={
    "message": "Write a research summary"
}) as response:
    for line in response.iter_lines():
        if line.startswith("data: "):
            print(line[6:])
```
