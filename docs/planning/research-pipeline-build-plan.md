# Building the OLS Agentic Sociology Research Pipeline on DeepFlo
## From Architecture to Implementation — The Complete Build Plan

**Date:** 2026-03-16
**Status:** Work in Progress
**License:** CC BY 4.0

---

## 1. What DeepFlo Actually Is Now

DeepFlo started as an HTTP bridge solving a dependency conflict. CC built it into something bigger. It's now a full integration and operations layer:

- **Runtime** — FastAPI server wrapping Deep Agents SDK (`/invoke`, `/invoke/stream`, `/health`)
- **CLI** — `serve`, `run`, `chat`, `acp`, `mcp` commands
- **MCP Server** — IDE and Langflow can call DeepFlo agents via MCP
- **ACP Server** — Editor-facing agent communication protocol
- **Langflow Bridge** — Custom component for visual workflow design
- **Workspace** — Memory, skills, checkpoint persistence
- **OpenSpec** — Spec-driven development governance for the build process itself

The sociology research pipeline doesn't need a separate system. It's built AS DeepFlo's primary use case. DeepFlo is the chassis. The research pipeline is the engine you bolt onto it.

---

## 2. The Build Strategy: OpenSpec-Governed, Skill-by-Skill

Every feature of the research pipeline gets built through OpenSpec's workflow:

```
/opsx:propose → /opsx:apply → /opsx:archive
```

This means every skill, every sub-agent, every MCP integration, every Kestra flow has:
- A proposal document (why, what's changing)
- A spec (requirements, scenarios)
- A design doc (technical approach)
- A task checklist (implementation steps)
- An archive (what was delivered)

For a no-code practitioner directing AI agents, this is essential. You describe what you want in the proposal. CC reads the spec and implements it. The spec prevents drift, hallucination, and "agent rewrote everything" surprises.

### The Build Sequence

Each item below is one OpenSpec change. Build them in order — each depends on the previous.

```
openspec/changes/
├── 001-research-agent-identity/          # AGENTS.md + base config
├── 002-literature-search-skill/          # First skill: OpenAlex + Semantic Scholar
├── 003-source-extraction-skill/          # Deep reading + structured extraction
├── 004-methodology-evaluation-skill/     # Quality assessment
├── 005-thematic-synthesis-skill/         # Cross-source pattern finding
├── 006-academic-writing-skill/           # Journal-quality reports
├── 007-accessible-translation-skill/     # Plain language for communities
├── 008-fact-check-skill/                 # Verification against sources
├── 009-sub-agent-definitions/            # 6 specialist sub-agents
├── 010-research-dossier-orchestrator/    # Full pipeline skill
├── 011-openalex-mcp-server/             # MCP tool: academic paper search
├── 012-lancedb-mcp-server/              # MCP tool: RAG retrieval + ingestion
├── 013-lancedb-ingestion-pipeline/      # Agent outputs → vector DB
├── 014-kestra-weekly-automation/         # Scheduled research cycles
├── 015-training-data-extraction/         # Agent outputs → fine-tune dataset
├── 016-sdt-analysis-skill/              # Self-Determination Theory lens
├── 017-mutual-aid-lens-skill/           # Cooperative economics lens
├── 018-news-monitor-skill/              # Current events tracking
├── 019-media-production-skill/          # Blog, social, newsletter outputs
├── 020-ovnn-scoring-skill/              # OVNN advisory scoring
├── 021-local-model-integration/         # Swap bulk sub-agents to Qwen 14B
├── 022-training-pipeline-automation/    # Kestra flow for model fine-tuning
```

Each one is a self-contained, spec-governed, reviewable unit of work.
You can hand any single change to CC (or Codex, or any agent) and it
implements exactly what the spec says — nothing more, nothing less.

---

## 3. The Architecture: DeepFlo as Research Platform

### System Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                        LANGFLOW (Visual Planning)                     │
│  Design pipelines │ Configure agents │ Monitor flows │ Iterate       │
│                                                                       │
│  ┌─────────────────────┐  ┌──────────────────┐  ┌────────────────┐  │
│  │ DeepFlo Component   │  │ LanceDB Query    │  │ Kestra Trigger │  │
│  │ (research pipeline) │  │ Component        │  │ Component      │  │
│  └─────────┬───────────┘  └────────┬─────────┘  └───────┬────────┘  │
└────────────┼───────────────────────┼────────────────────┼────────────┘
             │ HTTP / MCP            │                     │
┌────────────┼───────────────────────┼────────────────────┼────────────┐
│            ▼                       ▼                     ▼            │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                    DEEPFLO RUNTIME                            │    │
│  │                                                              │    │
│  │  ┌────────────────────────────────────────────────────────┐  │    │
│  │  │              DIRECTOR AGENT (Claude Sonnet)             │  │    │
│  │  │  AGENTS.md: SDT framework, OLS conventions, sociology  │  │    │
│  │  │  Plans with write_todos │ Delegates with task()        │  │    │
│  │  └──────────┬────────────────────────┬────────────────────┘  │    │
│  │             │                        │                       │    │
│  │    ┌────────┴──────────┐    ┌────────┴──────────┐           │    │
│  │    │  FRONTIER AGENTS  │    │   LOCAL AGENTS     │           │    │
│  │    │  (Claude Sonnet)  │    │   (Qwen 14B)       │           │    │
│  │    │                   │    │                     │           │    │
│  │    │  • Librarian      │    │  • Extractor        │           │    │
│  │    │  • Academic Writer│    │  • Analyst           │           │    │
│  │    │  • Reviewer       │    │  • Community Writer  │           │    │
│  │    └───────────────────┘    └─────────────────────┘           │    │
│  │                                                              │    │
│  │  Skills:  14 research skills loaded on demand                │    │
│  │  Memory:  AGENTS.md (persistent) + filesystem (per-project)  │    │
│  │  MCP:     OpenAlex, Semantic Scholar, LanceDB, Kestra        │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────────┐   │
│  │ DeepFlo CLI    │  │ DeepFlo MCP    │  │ DeepFlo ACP          │   │
│  │ Terminal agent │  │ IDE integration│  │ Editor integration   │   │
│  └────────────────┘  └────────────────┘  └──────────────────────┘   │
│                                                                       │
│                        DEEPFLO (Integration Layer)                    │
└───────────────────────────────────────┬──────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
          ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
          │   LanceDB    │    │   Kestra     │    │  Training Data   │
          │   4 domain   │    │   Weekly     │    │  Pipeline        │
          │   RAG        │    │   automation │    │                  │
          │   collections│    │   + triggers │    │  Agent outputs   │
          │              │    │              │    │  → <think> traces│
          │  sociology   │    │  news scan   │    │  → fine-tune     │
          │  psychology  │    │  lit update  │    │    dataset       │
          │  environment │    │  report gen  │    │  → model trains  │
          │  neuroscience│    │  notify Joel │    │  → cheaper agents│
          └──────────────┘    └──────────────┘    └──────────────────┘
```

### Access Points — Same Runtime, Multiple Interfaces

| Interface | Command / URL | Use Case |
|---|---|---|
| **Terminal** | `uv run deepflo chat` | Interactive research sessions, `/research` commands |
| **Terminal (headless)** | `uv run deepflo run "Research X"` | Scripted/automated research, Kestra triggers |
| **HTTP API** | `POST http://localhost:8011/invoke` | Programmatic access from any client |
| **Langflow** | Custom component in UI | Visual pipeline design and orchestration |
| **IDE (VS Code)** | MCP server via DeepFlo | Research from within your editor |
| **Kestra** | Shell task calling `deepflo run --headless` | Scheduled weekly research cycles |

All six interfaces hit the SAME runtime with the SAME skills, SAME memory, SAME sub-agents. One system, many doors.

---

## 4. Building It: The First 6 OpenSpec Changes

### Change 001: Research Agent Identity

```
/opsx:propose research-agent-identity
```

**Proposal:** Configure the DeepFlo runtime as a sociology research director. This is the foundation everything else builds on.

**What gets built:**
- `AGENTS.md` for the DeepFlo workspace with:
  - Identity: OLS Open Science Research Lab director
  - Theoretical frameworks: SDT, mutual aid, degrowth, direct democracy
  - Research standards: methodology evaluation, primary sources, open access
  - OLS conventions: CC BY 4.0, ASA citation style, file naming, GitHub-ready
  - Domain scope: sociology (primary), psychology, environmentalism, neuroscience
  - Infrastructure awareness: LanceDB, OpenAlex, Kestra, MCP servers
  - Joel's preferences: direct communication, YAML over Python, explain simply
- Default model configuration in `.env` (Claude Sonnet for director)
- Workspace directory structure for research outputs

**Spec acceptance criteria:**
- `uv run deepflo chat` starts with the sociology research identity
- Agent demonstrates knowledge of SDT when asked
- Agent uses ASA citation style by default
- Agent writes outputs to `research-output/` directory
- Memory persists across sessions

---

### Change 002: Literature Search Skill

```
/opsx:propose literature-search-skill
```

**Proposal:** First research skill. Searches OpenAlex and Semantic Scholar for academic papers, plus web search for grey literature.

**What gets built:**
- `skills/literature-search/SKILL.md`
- Tool functions for OpenAlex API and Semantic Scholar API
- Web search fallback (Tavily or DuckDuckGo)
- Structured bibliography output format
- Quality filters (peer-reviewed preference, recency weighting, methodology tagging)

**Spec acceptance criteria:**
- `/search mutual aid networks` returns 15+ structured bibliography entries
- Each entry has: title, authors, year, DOI, abstract excerpt, methodology type, relevance score
- Results written to `research-data/bibliography-{slug}.md`
- Agent explains search strategy before executing
- Works with both Tavily (if key present) and DuckDuckGo (fallback)

**Implementation notes for CC:**
- OpenAlex API is free, no key needed: `https://api.openalex.org/works?search=...`
- Semantic Scholar API is free with rate limits: `https://api.semanticscholar.org/graph/v1/paper/search?query=...`
- Write the tool functions in `deepflo/tools/` (or wherever the existing tool structure is)
- Register them in the Deep Agent's tool list

---

### Change 003: Source Extraction Skill

```
/opsx:propose source-extraction-skill
```

**Proposal:** Deep reading skill. Takes a source from the bibliography and extracts structured data: methodology, findings, limitations, data points.

**What gets built:**
- `skills/source-extraction/SKILL.md`
- Extraction template (structured markdown format)
- Web fetch tool for online sources
- PDF text extraction (if source is PDF)
- Quality assessment rubric (1-5 with criteria)

**Spec acceptance criteria:**
- Given a DOI or URL, agent reads the source and produces structured extraction
- Extraction includes: research question, methodology, sample, key findings (with quotes), limitations, quality score
- Output written to `research-data/extractions/{source-slug}.md`
- Agent flags potential conflicts of interest
- Agent identifies methodology type (quantitative/qualitative/mixed/review)

---

### Change 004: Methodology Evaluation Skill

```
/opsx:propose methodology-evaluation-skill
```

**Proposal:** Critical evaluation skill. Assesses research methodology quality with explicit reasoning.

**What gets built:**
- `skills/methodology-evaluation/SKILL.md`
- Evaluation rubric covering: sample size, sampling method, measurement validity, statistical approach, generalizability, bias, replication
- Reasoning trace format (explicit `<think>` style step-by-step evaluation)

**Spec acceptance criteria:**
- Given an extraction, agent produces a methodology evaluation with explicit reasoning
- Each criterion scored 1-5 with justification
- Overall quality assessment with confidence level
- Agent identifies specific methodological strengths and weaknesses
- Reasoning traces are structured enough to serve as training data

**Why this matters for the flywheel:**
The reasoning traces from this skill are EXACTLY the training data the fine-tuned model needs. Every methodology evaluation the agent produces teaches the next model version how to think about research quality.

---

### Change 005: Thematic Synthesis Skill

```
/opsx:propose thematic-synthesis-skill
```

**Proposal:** Cross-source synthesis. Reads all extractions for a topic and identifies patterns, contradictions, gaps.

**What gets built:**
- `skills/thematic-synthesis/SKILL.md`
- Synthesis template (organized by theme, not by source)
- Confidence scoring per finding
- Gap identification protocol

**Spec acceptance criteria:**
- Given 5+ extraction files, agent produces a thematic synthesis
- Synthesis organized by emergent themes, not by source
- Each theme cites specific extraction files
- Contradictions between sources explicitly noted
- Literature gaps identified with suggestions for future research
- Confidence levels stated for each finding

---

### Change 006: Academic Writing Skill

```
/opsx:propose academic-writing-skill
```

**Proposal:** Produces journal-quality sociology reports from synthesis documents.

**What gets built:**
- `skills/academic-writing/SKILL.md`
- Report template: abstract, introduction, literature review, methodology notes, findings, discussion, conclusion, references
- ASA citation formatting
- Academic register and tone guidelines

**Spec acceptance criteria:**
- Given a synthesis document, agent produces a structured academic report
- Report follows ASA style guide
- Every claim cites a specific source
- Limitations section present
- Abstract under 250 words
- Output to `research-output/{date}-{slug}/academic-report.md`

---

## 5. How OpenSpec Governs the Build Process

For each of the 22 changes:

```bash
# Step 1: You describe what you want
uv run deepflo chat
> /opsx:propose literature-search-skill

# Step 2: CC reads the proposal and generates specs
# Creates:
#   openspec/changes/002-literature-search-skill/
#     proposal.md
#     specs/
#     design.md
#     tasks.md

# Step 3: You review the proposal
# Edit anything that's wrong
# Approve when satisfied

# Step 4: CC implements against the spec
> /opsx:apply

# Step 5: CC works through the task list
# ✓ 1.1 Create SKILL.md
# ✓ 1.2 Implement OpenAlex search tool
# ✓ 1.3 Implement Semantic Scholar search tool
# ✓ 2.1 Add bibliography output formatter
# ✓ 2.2 Add quality filters
# ✓ 3.1 Write tests
# ✓ 3.2 Verify with real search

# Step 6: Archive when complete
> /opsx:archive

# The spec moves to openspec/changes/archive/
# The skill is now part of the live system
# The source-of-truth specs are updated
```

This gives you:
- **Reviewable change history** for every feature
- **Living documentation** that stays current with the code
- **Agent governance** — CC can only implement what the spec says
- **Contributor-friendly** — interns read specs, not code
- **Multi-agent portable** — switch from CC to Codex mid-project, specs travel

---

## 6. The Research Pipeline in Action

After the first 10 OpenSpec changes are built:

```bash
# Start DeepFlo
uv run deepflo chat

# The agent loads with sociology research identity, all skills,
# all sub-agents, persistent memory from prior sessions

> /research Impact of platform cooperativism on gig worker outcomes,
  focusing on studies from 2020-2026. Include SDT analysis.

# Agent activates research-dossier skill
# Plans with write_todos:

Planning research: "Impact of platform cooperativism on gig worker outcomes"

Todo list:
  1. □ Scope topic and identify sub-questions
  2. □ Search literature (delegate to librarian)
  3. □ Extract from top sources (delegate to extractor)
  4. □ Evaluate methodology (delegate to extractor)
  5. □ Synthesize across sources (delegate to analyst)
  6. □ Apply SDT lens
  7. □ Write academic report (delegate to academic writer)
  8. □ Write accessible summary (delegate to community writer)
  9. □ Fact-check all outputs (delegate to reviewer)
  10. □ Present for approval

# Each delegation spawns a sub-agent with isolated context
# Sub-agents write to the shared filesystem
# Director reads accumulated work and coordinates

# 30-60 minutes later:

Research complete. Outputs in research-output/2026-03-16-platform-cooperativism/

Files:
  plan.md                    — Research plan and sub-questions
  bibliography.md            — 22 sources with relevance scores
  extractions/               — 18 structured extraction files
  methodology-evaluations/   — 18 quality assessments
  synthesis.md               — Thematic synthesis (4 major themes)
  sdt-analysis.md            — SDT lens: autonomy (+), competence (+), relatedness (mixed)
  academic-report.md         — 3,200 word academic report, ASA citations
  accessible-summary.md      — 600 word blog post + key findings + social excerpts
  review-report.md           — 2 claims flagged for verification

Flagged issues:
  1. Smith (2023) citation count discrepancy — verify against original
  2. Rodriguez (2024) sample size claim needs page number

Approve for publication? [y/n]
```

---

## 7. How DeepFlo's Existing Infrastructure Supports This

What CC already built maps directly:

| DeepFlo Feature | Research Pipeline Use |
|---|---|
| `/invoke` endpoint | Kestra calls this for automated weekly scans |
| `/invoke/stream` SSE | Langflow streams research progress to UI |
| `/threads/{id}` | Thread persistence — resume research across sessions |
| MCP server | IDE can trigger research from VS Code |
| `--headless` mode via `deepflo run` | Kestra cron jobs run research non-interactively |
| API key auth | Protect the runtime in Docker deployment |
| Multi-provider support | Director uses Claude, bulk agents use Ollama (local Qwen) |
| LangSmith tracing | Observe every sub-agent call, debug pipeline issues |
| Docker stack | Postgres + Runtime + MCP + Langflow all containerized |
| `make demo` | New users see the system working in one command |
| OpenSpec | Every pipeline feature is spec-governed and reviewable |

---

## 8. The Build Timeline (Revised for DeepFlo)

### Phase 1: Foundation (Weeks 1-2)
OpenSpec changes 001-003

- [ ] 001: Research agent identity (AGENTS.md, workspace config)
- [ ] 002: Literature search skill (OpenAlex, Semantic Scholar)
- [ ] 003: Source extraction skill (deep reading, structured output)
- [ ] Validate: search for papers → extract from them → review quality

### Phase 2: Analysis Pipeline (Weeks 3-4)
OpenSpec changes 004-008

- [ ] 004: Methodology evaluation skill
- [ ] 005: Thematic synthesis skill
- [ ] 006: Academic writing skill
- [ ] 007: Accessible translation skill
- [ ] 008: Fact-check skill
- [ ] Validate: full 5-stage pipeline on a real sociology topic

### Phase 3: Sub-Agents + Orchestrator (Weeks 5-6)
OpenSpec changes 009-010

- [ ] 009: 6 sub-agent definitions (librarian, extractor, analyst, writers, reviewer)
- [ ] 010: Research dossier orchestrator (full pipeline skill)
- [ ] Validate: `/research <topic>` runs end-to-end with delegation

### Phase 4: Infrastructure Integration (Weeks 7-8)
OpenSpec changes 011-014

- [ ] 011: OpenAlex MCP server
- [ ] 012: LanceDB MCP server
- [ ] 013: LanceDB ingestion (agent outputs → vector DB)
- [ ] 014: Kestra weekly automation
- [ ] Validate: automated weekly scan runs, outputs appear in LanceDB

### Phase 5: Domain Lenses + Media (Weeks 9-10)
OpenSpec changes 015-020

- [ ] 015: Training data extraction pipeline
- [ ] 016: SDT analysis skill
- [ ] 017: Mutual aid lens skill
- [ ] 018: News monitor skill
- [ ] 019: Media production skill (blog, social, newsletter, infographic briefs)
- [ ] 020: OVNN scoring skill
- [ ] Validate: complete research-to-publication cycle with all lenses

### Phase 6: Local Model + Flywheel (Weeks 11-12)
OpenSpec changes 021-022

- [ ] 021: Swap bulk sub-agents to local Qwen 14B via Ollama
- [ ] 022: Kestra flow for automated model fine-tuning
- [ ] Validate: research cycle runs with hybrid models, training data accumulates
- [ ] First fine-tuning run on accumulated dataset

---

## 9. What This System Looks Like at Maturity

After 6 months of weekly research cycles:

**LanceDB contains:**
- 500+ structured bibliography entries across 4 domains
- 300+ source extractions with methodology evaluations
- 50+ thematic syntheses
- 50+ academic reports (OLS's own research corpus)
- 50+ accessible translations
- 26 weekly news digests
- SDT analyses, OVNN scores, mutual aid evaluations

**The training dataset contains:**
- 2,000+ reasoning trace examples
- Methodology evaluations with explicit `<think>` traces
- Synthesis examples with cross-source reasoning
- Academic ↔ accessible translation pairs
- Fact-checking verification chains

**The fine-tuned model:**
- Qwen 14B that reasons like a sociologist
- Powers 3 of 6 sub-agents locally
- Reduces per-cycle API cost from $15 to $3
- Improves with every research cycle

**The publication pipeline:**
- Academic reports publishable in journals
- Accessible summaries ready for blog/newsletter
- Social media excerpts ready to post
- All CC BY 4.0, all open access, all GitHub-hosted

**The team capability:**
- Interns read OpenSpec specs to understand the system
- Contributors add skills through the OpenSpec workflow
- The system documents itself as it builds

---

## 10. Why DeepFlo is the Right Platform for This

You could build the research pipeline as a standalone project — just
Deep Agents skills in a directory. But DeepFlo gives you:

1. **The runtime** — one server that CLI, Langflow, IDE, and Kestra all share
2. **The MCP server** — IDE integration without separate tooling
3. **The Langflow bridge** — visual pipeline design for non-coders
4. **The Docker stack** — reproducible deployment for the full system
5. **The thread persistence** — resume research across sessions
6. **The multi-provider routing** — Claude for judgment, Ollama for labor
7. **The LangSmith tracing** — observe and debug multi-agent research cycles
8. **The OpenSpec governance** — every feature spec-driven and reviewable
9. **The API auth** — protect the runtime when deployed
10. **The streaming** — watch research happen in real-time through Langflow

None of these are things the research skills need to implement themselves.
DeepFlo provides them as platform infrastructure. The skills just do
sociology. DeepFlo handles everything else.

This is the whole point. DeepFlo is the operations layer.
Deep Agents is the agent layer. The skills are the domain layer.
Each layer does one job.
