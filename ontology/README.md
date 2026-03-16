# DeepFlo Ontology Reference

Domain taxonomies, controlled vocabularies, and knowledge graph schemas
for the OLS Open Science Research Lab.

This directory provides the ontological foundation that DeepFlo's research
agents use to:

- Map search queries to correct subfields and concepts
- Validate extracted terminology against controlled vocabularies
- Organize synthesis by disciplinary structure (not ad hoc categories)
- Place findings in the correct L0-L4 taxonomy position
- Connect concepts across domains (e.g., SDT from psychology applied to sociology)

## Source

Based on the OLS Domain Knowledge Architecture specification (T2KG Pipeline).
Reference standard: ELSST (European Language Social Science Thesaurus) + W3C SKOS.

## Structure

Each domain folder contains up to 7 artifact files:

1. `vocabulary.md` — Controlled vocabulary (canonical terms)
2. `definitions.md` — Term definitions (textbook + plain-language + contextual)
3. `taxonomy.md` — L0-L4 hierarchical classification
4. `thesaurus.md` — Related terms, synonyms, broader/narrower relationships
5. `ontology.md` — Formal relationships (prerequisite, part-of, contrast-with)
6. `nodes-schema.json` — Knowledge graph node format
7. `cross-domain.md` — Connections to other domains

## Usage by Research Skills

- `literature-search` reads taxonomy.md to map queries to subfields
- `source-extraction` reads vocabulary.md to validate extracted terms
- `thematic-synthesis` reads taxonomy.md to organize findings by branch
- `sdt-analysis` reads psychology/cross-domain.md for SDT framework mapping
- All skills reference definitions.md for canonical term meanings

## Status

Scaffold created. Sociology domain is the priority for population.
Other domains will be populated as research cycles produce terminology.

**Important:** Research agents can propose additions to these files.
Every extraction that surfaces a term not in the vocabulary is a
candidate for inclusion. The ontology grows with the research.
