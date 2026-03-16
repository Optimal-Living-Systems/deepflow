# Proposal: Literature Search Skill
**Change ID:** 002-literature-search-skill
**Status:** Complete
**Created:** 2026-03-16
**Author:** Joel / OLS AI Lab

## What We Are Building

The first research skill: academic literature search using OpenAlex and Semantic Scholar APIs, with web search fallback for grey literature.

## What Gets Built

- `skills/literature-search/SKILL.md` — skill definition, inputs, outputs, usage instructions
- `search_openalex` tool in `src/deep_flo_runtime/tools.py` — OpenAlex API (free, no key)
- `search_semantic_scholar` tool in `src/deep_flo_runtime/tools.py` — Semantic Scholar API (free, rate-limited)
- Both tools registered in `create_runtime_tools()`

## Acceptance Criteria

- Searching for a sociology topic returns structured bibliography entries
- Each entry has: title, authors, year, DOI, abstract excerpt, cited-by count, open access status
- OpenAlex tool handles abstract reconstruction from inverted index format
- Semantic Scholar tool handles 429 rate limit gracefully
- Both tools registered and available to the runtime agent
