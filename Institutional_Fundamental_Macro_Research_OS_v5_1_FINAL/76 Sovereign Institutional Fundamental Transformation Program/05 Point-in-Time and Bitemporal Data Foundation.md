---
title: "05 Point-in-Time and Bitemporal Data Foundation"
type: program-phase
status: planned
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-transformation]
---
# 05 Point-in-Time and Bitemporal Data Foundation

## Mission

Build a database that can reconstruct the information set available at any historical cutoff without revision, survivorship or timestamp leakage.

## Why this phase exists

This phase closes a specific gap between a large knowledge base and a production institutional capability. Work is not complete when prose exists; it is complete when the required artifacts can be independently reproduced, tested and governed.

## Dependencies

Phase 04

## Build scope

- Bitemporal observation schema.
- Release calendar and timezone service.
- Vintage query API and historical snapshot generator.

## Required artifacts

- architecture decision record;
- source and data contracts;
- implementation specification;
- test plan and expected failure cases;
- reproducible evidence package;
- ownership, review and retirement record;
- change log linked to claim and model IDs.

## Acceptance gates

- Pseudo-real-time queries reproduce first-release values and desk availability.
- Index constituents, estimates, filings and contract specifications are historically correct.
- Leakage test suite passes.


## Red-team questions

- Which claim could still be true for the wrong reason?
- Which missing dataset or institutional constraint could reverse the conclusion?
- What simple benchmark would make this phase unnecessary?
- How could revised data, survivorship, timestamp error or selection bias create a false success?
- What operational failure would make a valid research result unusable?

## Exit condition

The phase closes only after artifacts, tests and approvals are attached. Narrative completion, file count and word count do not close the phase.
