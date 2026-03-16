# Skill: Literature Search

**Skill ID:** literature-search
**Version:** 1.0.0
**Change:** 002-literature-search-skill

---

## Purpose

Search academic databases and the web for peer-reviewed sources relevant to a sociology research topic. Returns structured bibliography entries ready for extraction and synthesis.

---

## Inputs

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Research topic or question |
| `max_results` | int | no | Maximum sources to return (default: 20) |
| `from_year` | int | no | Filter sources from this year onward |
| `methodology_filter` | string | no | Filter by type: `quantitative`, `qualitative`, `mixed`, `review`, `any` (default: `any`) |
| `open_access_only` | bool | no | Restrict to freely available sources (default: false) |

---

## Outputs

Structured bibliography written to `research-data/bibliography-{slug}.md`.

Each entry contains:
- Title
- Authors
- Year
- DOI or URL
- Abstract excerpt (first 300 chars)
- Methodology type (inferred from abstract)
- Open access status
- Relevance score (1-5, estimated from title/abstract match to query)
- Source database (OpenAlex, Semantic Scholar, or Web)

---

## Tools Used

- `search_openalex` — OpenAlex API (free, no key required). Best for peer-reviewed academic papers.
- `search_semantic_scholar` — Semantic Scholar API (free, rate-limited). Good for CS/interdisciplinary coverage.
- `web_search` — Tavily or DuckDuckGo fallback. For grey literature, policy reports, community research.

---

## Usage Instructions

Before executing, explain your search strategy:
1. Name the databases you'll search and why
2. List the search terms you'll use
3. Estimate expected result count

Execute in this order:
1. Search OpenAlex (primary — best sociology coverage)
2. Search Semantic Scholar (secondary — broader interdisciplinary)
3. Web search for grey literature if < 10 peer-reviewed results found

Deduplicate by DOI. Assign relevance scores. Write to `research-data/bibliography-{slug}.md`.

Report: total sources found, peer-reviewed count, open access count, date range covered.

---

## Quality Standards

- Prefer sources from the last 10 years unless the query is historical
- Flag predatory journals when identifiable
- Note when a highly-cited source is not open access — include DOI for institutional access
- Minimum 5 peer-reviewed sources before proceeding to extraction stage

---

## Example Call

```
Use the literature-search skill to find sources on platform cooperativism and gig worker outcomes, 2018-2026, any methodology.
```

Expected output: `research-data/bibliography-platform-cooperativism.md` with 15-25 entries.
