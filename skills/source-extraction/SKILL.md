# Skill: Source Extraction

**Skill ID:** source-extraction
**Version:** 1.0.0
**Change:** 003-source-extraction-skill

---

## Purpose

Deep-read a single academic source and extract structured data: research question, methodology, sample, key findings, limitations, and quality assessment. The output feeds directly into thematic synthesis and methodology evaluation stages.

---

## Inputs

| Parameter | Type | Required | Description |
|---|---|---|---|
| `source` | string | yes | DOI, URL, or path to PDF |
| `research_question` | string | yes | The overarching research question this source is being evaluated against |
| `output_slug` | string | yes | Filename slug for the extraction file (e.g., `smith-2023-platform-coop`) |

---

## Outputs

Structured extraction written to `research-data/extractions/{output_slug}.md`.

Extraction file structure:
```
# Source Extraction: {title}

## Bibliographic Reference
{ASA-formatted citation}

## Research Question Addressed
{What question does this source answer?}

## Methodology
- Type: quantitative / qualitative / mixed / systematic review / meta-analysis / theoretical
- Sample: {description of sample/data}
- Methods: {specific methods used}
- Time period: {data collection dates if available}

## Key Findings
{Bullet list of major findings, with direct quotes where significant}
> "{quote}" (p. X) — or note if page numbers unavailable

## Limitations Acknowledged by Authors
{What the authors say their study cannot claim}

## Additional Limitations (Analyst-Identified)
{Limitations the analyst identified beyond what authors acknowledged}

## Quality Assessment
- Overall score: X/5
- Justification: {explicit reasoning for the score}
- Methodology rigor: X/5
- Sample representativeness: X/5
- Generalizability: X/5

## Conflicts of Interest / Funding
{Any disclosed funding, institutional affiliations, or ideological commitments}

## Relevance to Research Question
{How directly this source addresses the research question, rated 1-5}

## Open Access
{URL if freely available, or note if paywalled}
```

---

## Tools Used

- `fetch_url` — For online sources (HTML pages, open access PDFs via URL)
- `web_search` — To find the open access version of a paywalled source

---

## Usage Instructions

1. Attempt to access the full text:
   - If DOI: try `https://doi.org/{doi}` first
   - If paywalled: search for open access version (`{title} filetype:pdf` or Unpaywall)
   - If PDF: use fetch_url on the direct PDF URL
2. Read the abstract, introduction, methods, results, and conclusion sections
3. Extract all required fields using the template above
4. Assign quality scores with explicit reasoning (not just a number)
5. Flag `[NEEDS VERIFICATION]` for any claim you cannot confirm from the text
6. Write output to `research-data/extractions/{output_slug}.md`

## Quality Scoring Guide

| Score | Meaning |
|---|---|
| 5 | Rigorous methodology, large/representative sample, findings well-supported, limitations clear |
| 4 | Sound methodology, adequate sample, minor limitations acknowledged |
| 3 | Acceptable methodology, some concerns about sample or generalizability |
| 2 | Weak methodology, small or unrepresentative sample, overclaimed findings |
| 1 | Serious methodological flaws, no sample description, or theoretical only |

---

## Example Call

```
Use the source-extraction skill to extract from DOI 10.1177/0950017019871532.
Research question: How does platform ownership structure affect worker autonomy?
Output slug: wood-2019-platform-worker-autonomy
```

Expected output: `research-data/extractions/wood-2019-platform-worker-autonomy.md`
