---
title: "02 Fundamental-Only Boundary Migration"
type: program-phase
status: planned
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-transformation]
---
# 02 Fundamental-Only Boundary Migration

## Mission

Remove price-pattern analysis and all references to chart triggers while preserving legitimate price-derived measurements, market-implied information and implementation analytics.

## Why this phase exists

This phase closes a specific gap between a large knowledge base and a production institutional capability. Work is not complete when prose exists; it is complete when the required artifacts can be independently reproduced, tested and governed.

## Dependencies

Phase 01

## Build scope

- Rename decision, intraday and multi-day modules to fundamental-only language.
- Remove prohibited pattern language from notes, schemas and prompts.
- Add an automated prohibited-term and semantic-boundary test.

## Required artifacts

- architecture decision record;
- source and data contracts;
- implementation specification;
- test plan and expected failure cases;
- reproducible evidence package;
- ownership, review and retirement record;
- change log linked to claim and model IDs.

## Acceptance gates

- Zero prohibited analysis terms in the production Vault.
- All operational outputs use the fundamental decision-state vocabulary.
- Market data are used only for pricing, response, liquidity, valuation, volatility, positioning or outcome measurement.


## Red-team questions

- Which claim could still be true for the wrong reason?
- Which missing dataset or institutional constraint could reverse the conclusion?
- What simple benchmark would make this phase unnecessary?
- How could revised data, survivorship, timestamp error or selection bias create a false success?
- What operational failure would make a valid research result unusable?

## Exit condition

The phase closes only after artifacts, tests and approvals are attached. Narrative completion, file count and word count do not close the phase.
