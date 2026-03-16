# Testing

## What is currently tested

Automated tests currently cover:
- settings path behavior
- provider status reporting
- response text extraction from runtime messages
- API behavior for missing model configuration

Run tests:

```bash
cd /path/to/deepflow
uv run pytest
```

## What has been manually verified

- `uv run deepflow --help`
- `uv run deepflow doctor`
- Langflow-side import of the DeepFlow component from the Langflow environment
- runtime `/health` over a real localhost port
- upstream `deepagents-cli` installation
- live DeepFlow smoke tests:
  - Anthropic: passed
  - OpenAI: passed
  - OpenRouter: passed
  - DeepSeek: passed
  - Gemini: provider wiring passed, but the supplied Google project is quota-blocked for `gemini-2.5-pro`
- Langflow bridge smoke test against the real runtime over HTTP: passed
- LangSmith run visibility on the `deepflow` project: passed
- ACP server boot smoke test: passed
- MCP streamable HTTP smoke test with official Python client: passed
- MCP tool call `deepflow_research` returning `MCP_OK`: passed
- Langflow MCP utility test discovering and invoking DeepFlow tools: passed
- `docker compose config` validation for Postgres-only and full-stack files: passed
- portable config path behavior after removing hardcoded `/home/joel/...` defaults: passed
- local Langflow database initialization against PostgreSQL: passed
- full Docker stack startup: passed
- containerized Langflow HTTP endpoint returning `200`: passed

## Current live blockers

- the supplied Google project does not currently have usable Gemini quota

## Optional follow-on validation

1. Start `uv run deepflow acp`
2. Connect from an ACP-capable editor
3. Verify prompt, tool use, and local approvals from the editor
4. Import one of the checked-in bridge flows and save it as a reusable subflow
5. Orchestrate DeepFlow through `Run Flow`

## Known environment-specific caveat

Direct localhost verification required running the runtime outside the default sandbox restrictions. That is an environment limitation, not a DeepFlow design requirement.


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
