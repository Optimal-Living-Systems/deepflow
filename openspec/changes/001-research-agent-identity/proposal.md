# Proposal: Research Agent Identity
**Change ID:** 001-research-agent-identity
**Status:** Complete
**Created:** 2026-03-16
**Author:** Joel / OLS AI Lab

## What We Are Building

Configure the Deep Flo runtime as the OLS Open Science Research Director — a sociology research director agent with persistent identity, theoretical frameworks, and workspace conventions.

This is the foundation that all subsequent research pipeline changes build on.

## What Gets Built

- `memories/AGENTS.md` — Full research director identity for the runtime agent, including:
  - OLS mission and role identity
  - Theoretical frameworks: SDT, mutual aid, degrowth, direct democracy, OVNN
  - Research standards: ASA citations, CC BY 4.0, methodology typing, confidence levels
  - OLS conventions: file naming, output directories, GitHub-ready Markdown
  - Domain scope: sociology (primary) + psychology, environmental sociology, neuroscience
  - Infrastructure awareness: skills, MCP, thread persistence, sub-agents, multi-provider
  - Communication style preferences for Joel
  - Behavioral rules for multi-step research tasks
- `research-output/` directory — tracked in git (structure only, not content)
- `research-data/` directory with `extractions/` subdirectory — tracked in git (structure only)
- `.gitignore` updates to track directory structure but not research files

## Acceptance Criteria

- `uv run deep-flo chat` starts with the sociology research identity
- Agent demonstrates knowledge of SDT when asked about psychological frameworks
- Agent uses ASA citation style by default
- Agent plans with `write_todos` before multi-step tasks
- Agent writes outputs to `research-output/` and `research-data/` directories
- Memory persists across sessions via thread IDs
