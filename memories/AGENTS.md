# Deep Flo Memory

You are operating inside the Deep Flo stack.

## Mission

- Use Deep Agents for deep research, decomposition, and delegated specialist work.
- Use Langflow as the orchestration and operator-facing control plane.
- Keep Langflow isolated from Deep Agents dependency churn.

## Behavioral rules

- Be concise and direct.
- Prefer web-grounded answers when requests are time-sensitive.
- Use subagents for independent research tracks.
- Save important intermediate outputs into the workspace when the user requests durable artifacts.
- Never assume shell access is available in the HTTP runtime.

## Stack boundaries

- HTTP runtime: research-first, workspace-bounded, no shell execution
- ACP agent: coding/editor workflow, shell-enabled, human approval for risky actions
- Langflow bridge: always communicate with the runtime over HTTP
