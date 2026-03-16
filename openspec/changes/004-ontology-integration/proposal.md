# Proposal: Ontology Integration

**Change ID:** 004-ontology-integration
**Status:** Complete
**Created:** 2026-03-16
**Author:** Joel / OLS AI Lab

## Why

DeepFlo's research agents need a controlled taxonomy and vocabulary
to search, extract, and synthesize systematically — not ad hoc.
Without ontological grounding, the agent uses whatever terms it
thinks of. With it, queries map to disciplinary structure.

The OLS Domain Knowledge Architecture (DKA) defines a 6-domain taxonomy
scaffolding built on ELSST (European Language Social Science Thesaurus)
and W3C SKOS standards. This change brings the operational subset
into DeepFlo's workspace as a living reference layer.

## What's Changing

- New `ontology/` directory with domain scaffolds and schemas
- New `ontology-lookup` skill for taxonomy queries and term validation
- `memories/AGENTS.md` and root `AGENTS.md` updated with ontology reference instructions
- Sociology domain seeded with L0-L2 taxonomy + ~20 core vocabulary terms
- Scaffold directories for psychology, environmentalism, neuroscience
- Agent-assisted taxonomy population workflow documented

## Connection to DKA

Based on the OLS Domain Knowledge Architecture specification
(T2KG Pipeline, TWP-2026-001). The standalone ols-domain-knowledge-architecture
repo contains the frozen spec. This change brings the operational
subset into DeepFlo's workspace.

The DKA repo was not found locally or on GitHub at time of implementation.
The ontology scaffold was created directly in DeepFlo from the spec.

## Acceptance Criteria

- `ontology/domains/sociology/taxonomy.md` contains L0-L2 branches
- `ontology/domains/sociology/vocabulary.md` contains ≥20 seed terms
- `ontology/schemas/base-node-schema.json` validates knowledge graph entries
- `skills/ontology-lookup/SKILL.md` is loadable by the agent
- `memories/AGENTS.md` instructs the agent to reference the ontology
- Research agents, when asked to research a sociology topic, can use the taxonomy
