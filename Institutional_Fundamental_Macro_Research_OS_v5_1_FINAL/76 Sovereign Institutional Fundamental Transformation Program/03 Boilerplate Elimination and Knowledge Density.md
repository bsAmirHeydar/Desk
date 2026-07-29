---
title: "03 Boilerplate Elimination and Knowledge Density"
type: program-phase
status: planned
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-transformation]
---
# 03 Boilerplate Elimination and Knowledge Density

## Mission

Centralize shared doctrine and rebuild domain notes around subject-specific mechanics, equations, data fields, examples and failure modes.

## Why this phase exists

This phase closes a specific gap between a large knowledge base and a production institutional capability. Work is not complete when prose exists; it is complete when the required artifacts can be independently reproduced, tested and governed.

## Dependencies

Phase 01, Phase 02

## Build scope

- Duplicate-paragraph scanner and near-duplicate document report.
- Central standards for shared methods.
- Editorial queue ranked by low information density.

## Required artifacts

- architecture decision record;
- source and data contracts;
- implementation specification;
- test plan and expected failure cases;
- reproducible evidence package;
- ownership, review and retirement record;
- change log linked to claim and model IDs.

## Acceptance gates

- No normalized paragraph appears in more than 100 substantive notes unless explicitly allow-listed.
- Each domain note contains variables, sources, mechanisms and tests unique to its subject.
- Title substitution cannot leave most of a note valid.


## Red-team questions

- Which claim could still be true for the wrong reason?
- Which missing dataset or institutional constraint could reverse the conclusion?
- What simple benchmark would make this phase unnecessary?
- How could revised data, survivorship, timestamp error or selection bias create a false success?
- What operational failure would make a valid research result unusable?

## Exit condition

The phase closes only after artifacts, tests and approvals are attached. Narrative completion, file count and word count do not close the phase.
