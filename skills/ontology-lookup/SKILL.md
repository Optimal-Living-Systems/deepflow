---
name: ontology-lookup
description: Query the OLS domain taxonomy to classify concepts, find related terms, and validate terminology
globs: ["ontology/**"]
---

# Ontology Lookup

## When to Use
- When mapping a research topic to its correct taxonomy position
- When validating extracted terms against the controlled vocabulary
- When organizing synthesis findings by disciplinary branch
- When connecting concepts across domains (e.g., SDT in sociology context)
- When a new term is encountered that may need to be added to the vocabulary

## Procedure

### Concept Classification
1. Read `ontology/domains/{domain}/taxonomy.md`
2. Find the L1 branch that best fits the concept
3. Identify the L2 subfield
4. If the concept maps to L3/L4, note the full path
5. If the concept doesn't exist in the taxonomy, flag it as a candidate for addition

### Term Validation
1. Read `ontology/domains/{domain}/vocabulary.md`
2. Check if the extracted term matches a canonical term or alias
3. If match found: use the canonical form in all outputs
4. If no match: check ELSST match column for standard form
5. If truly new: propose addition in extraction notes

### Cross-Domain Mapping
1. Read `ontology/domains/{domain}/cross-domain.md` (when it exists)
2. Identify connections to concepts in other domains
3. Use these connections to enrich analysis (e.g., SDT from psychology applied to sociology)

### Taxonomy Population (agent-assisted)
When extracting from sources, if you encounter:
- A concept not in the taxonomy → note in extraction as "PROPOSED: [concept] under [L1]/[L2]"
- A definition not in the vocabulary → note as "PROPOSED DEFINITION: [term] = [definition]"
- A relationship not captured → note as "PROPOSED RELATION: [term A] [relation type] [term B]"

These proposals accumulate in extraction files. A human review cycle
periodically promotes validated proposals into the official taxonomy.

## Output Format
When reporting taxonomy position:
```
Domain: sociology
Path: L1:Economic Sociology → L2:Cooperative Economics → L3:[concept]
ELSST: [match or "no match"]
Confidence: [0-1]
```
