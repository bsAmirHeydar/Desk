---
title: "17 Banking Credit and Deposit Intelligence"
type: program-phase
status: planned
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-transformation]
---
# 17 Banking Credit and Deposit Intelligence

## Mission

Model bank assets, liabilities, deposits, liquidity, capital, asset quality, lending standards and monetary transmission.

## Why this phase exists

This phase closes a specific gap between a large knowledge base and a production institutional capability. Work is not complete when prose exists; it is complete when the required artifacts can be independently reproduced, tested and governed.

## Dependencies

Phase 05, Phase 07, Phase 11, Phase 13

## Build scope

- Bank-level and aggregate balance-sheet datasets.
- Deposit beta and funding-cost models.
- Credit impulse and lending-condition indices.

## Required artifacts

- architecture decision record;
- source and data contracts;
- implementation specification;
- test plan and expected failure cases;
- reproducible evidence package;
- ownership, review and retirement record;
- change log linked to claim and model IDs.

## Acceptance gates

- Accounting and regulatory definitions are harmonized.
- Stress scenarios include liquidity and solvency interaction.
- Bank behavior is linked to household and corporate credit.


## Red-team questions

- Which claim could still be true for the wrong reason?
- Which missing dataset or institutional constraint could reverse the conclusion?
- What simple benchmark would make this phase unnecessary?
- How could revised data, survivorship, timestamp error or selection bias create a false success?
- What operational failure would make a valid research result unusable?

## Exit condition

The phase closes only after artifacts, tests and approvals are attached. Narrative completion, file count and word count do not close the phase.
