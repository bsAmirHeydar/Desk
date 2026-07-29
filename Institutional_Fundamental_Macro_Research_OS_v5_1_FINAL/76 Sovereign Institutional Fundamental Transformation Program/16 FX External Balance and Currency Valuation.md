---
title: "16 FX External Balance and Currency Valuation"
type: program-phase
status: planned
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-transformation]
---
# 16 FX External Balance and Currency Valuation

## Mission

Combine relative policy, growth, inflation, balance of payments, valuation, carry, hedging and intervention.

## Why this phase exists

This phase closes a specific gap between a large knowledge base and a production institutional capability. Work is not complete when prose exists; it is complete when the required artifacts can be independently reproduced, tested and governed.

## Dependencies

Phase 14, Phase 15

## Build scope

- Country external-account books.
- REER, BEER/FEER and balance-sheet valuation models.
- FX options and flow integration.

## Required artifacts

- architecture decision record;
- source and data contracts;
- implementation specification;
- test plan and expected failure cases;
- reproducible evidence package;
- ownership, review and retirement record;
- change log linked to claim and model IDs.

## Acceptance gates

- Spot narratives reconcile with funding and external accounts.
- Intervention and capital controls are historically versioned.
- Relative-value expressions include carry, basis and tail risk.


## Red-team questions

- Which claim could still be true for the wrong reason?
- Which missing dataset or institutional constraint could reverse the conclusion?
- What simple benchmark would make this phase unnecessary?
- How could revised data, survivorship, timestamp error or selection bias create a false success?
- What operational failure would make a valid research result unusable?

## Exit condition

The phase closes only after artifacts, tests and approvals are attached. Narrative completion, file count and word count do not close the phase.
