---
title: "04 Claim-Level Evidence and Citation"
type: program-phase
status: planned
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-transformation]
---
# 04 Claim-Level Evidence and Citation

## Mission

Convert source-route lists into claim-level evidence chains with precise locators, timestamps, vintages and transformations.

## Why this phase exists

This phase closes a specific gap between a large knowledge base and a production institutional capability. Work is not complete when prose exists; it is complete when the required artifacts can be independently reproduced, tested and governed.

## Dependencies

Phase 01, Phase 03

## Build scope

- Claim-evidence matrix service.
- Archived source artifacts and hash records where licensing permits.
- Citation locators for series, tables, filings, transcripts and API fields.

## Required artifacts

- architecture decision record;
- source and data contracts;
- implementation specification;
- test plan and expected failure cases;
- reproducible evidence package;
- ownership, review and retirement record;
- change log linked to claim and model IDs.

## Acceptance gates

- Every material claim resolves to an evidence record.
- Unsupported and judgment claims remain visible.
- Source contamination tests pass by asset and domain.


## Red-team questions

- Which claim could still be true for the wrong reason?
- Which missing dataset or institutional constraint could reverse the conclusion?
- What simple benchmark would make this phase unnecessary?
- How could revised data, survivorship, timestamp error or selection bias create a false success?
- What operational failure would make a valid research result unusable?

## Exit condition

The phase closes only after artifacts, tests and approvals are attached. Narrative completion, file count and word count do not close the phase.
