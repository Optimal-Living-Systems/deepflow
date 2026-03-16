# Proposal: Source Extraction Skill
**Change ID:** 003-source-extraction-skill
**Status:** Complete
**Created:** 2026-03-16
**Author:** Joel / OLS AI Lab

## What We Are Building

The deep-reading skill. Given a DOI, URL, or PDF, the agent reads the full source and produces a structured extraction: research question, methodology, sample, key findings, limitations, quality score, and conflict of interest flags.

## What Gets Built

- `skills/source-extraction/SKILL.md` — skill definition with full extraction template, quality scoring guide, and usage instructions

## Acceptance Criteria

- Agent reads a source and produces a structured extraction in the correct template format
- Quality scores include explicit reasoning (not just a number)
- Agent attempts to find open access version before reporting a source as unavailable
- Extractions written to `research-data/extractions/{slug}.md`
- Agent flags unverifiable claims with `[NEEDS VERIFICATION]`
- Methodology type is always specified
