# Workflows

## Workflow 1: CLI research

Use this when you want Deep Flo directly in the terminal.

```bash
cd /path/to/deep-flo
uv run deep-flo chat
```

Or one-shot:

```bash
uv run deep-flo run "Research the latest LangGraph release notes."
```

## Workflow 2: Langflow orchestration

Use this when you want Deep Flo as one specialist capability inside a larger visual flow.

1. Start the Deep Flo runtime
2. Start Langflow with `LANGFLOW_COMPONENTS_PATH`
3. Add the `Deep Flo Runtime` node
4. Send a prompt and thread ID into that node
5. Route the output into downstream Langflow components

Current state:
- the node exists
- tool-oriented use is supported
- bridge flow JSON assets are checked in under `examples/langflow/`
- `Run Flow` usage is documented with a checked-in recipe
- MCP-based Langflow access is also available through the Deep Flo MCP server

## Workflow 3: ACP editor workflow

Use this when you want a coding/editor-facing agent rather than an HTTP research runtime.

```bash
cd /path/to/deep-flo
uv run deep-flo acp
```

The ACP profile:
- uses a local shell backend
- is rooted at the editor project directory
- supports approval modes for edits and shell execution

Setup details:
- [editor/README.md](../editor/README.md)
- [editor/zed-settings.example.json](../editor/zed-settings.example.json)

## Workflow 4: VS Code MCP workflow

Use this when you want Deep Flo available in VS Code through MCP.

1. Open the Deep Flo repo in VS Code
2. Use the workspace config at [/.vscode/mcp.json](../.vscode/mcp.json)
3. Start the MCP server over `stdio`
4. Call `deep-flo_research` or `deep-flo_status` from the IDE

The MCP profile:
- is research-oriented rather than shell-edit oriented
- works with VS Code's MCP integration
- can also be exposed to Langflow via streamable HTTP

Current state:
- server startup is verified
- tool discovery is verified
- live `deep-flo_research` invocation is verified
- Langflow MCP client utility compatibility is verified
- VS Code MCP configuration is checked in and ready to use

## Workflow 5: Official upstream CLI

The upstream `deepagents-cli` is also installed.

```bash
deepagents --help
```

This gives you:
- upstream terminal UX
- upstream session management
- upstream sandbox integrations

Deep Flo still remains the project-specific runtime and Langflow integration layer.


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
