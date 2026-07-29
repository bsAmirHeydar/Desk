---
title: "20 Equity Index and Sector Fundamental Engines"
type: program-phase
status: planned
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-transformation]
---
# 20 Equity Index and Sector Fundamental Engines

## Mission

Aggregate company fundamentals, rates, risk premia, concentration, buybacks, issuance, passive flows and index mechanics.

## Why this phase exists

This phase closes a specific gap between a large knowledge base and a production institutional capability. Work is not complete when prose exists; it is complete when the required artifacts can be independently reproduced, tested and governed.

## Dependencies

Phase 12, Phase 19

## Build scope

- Bottom-up index earnings and cash-flow models.
- Sector and factor exposure maps.
- Breadth, concentration and rebalance datasets.

## Required artifacts

- architecture decision record;
- source and data contracts;
- implementation specification;
- test plan and expected failure cases;
- reproducible evidence package;
- ownership, review and retirement record;
- change log linked to claim and model IDs.

## Acceptance gates

- Index conclusions reconcile with constituent fundamentals.
- Cash-flow and discount-rate contributions are separated.
- Passive and derivative flows are not misclassified as earnings information.


## Red-team questions

- Which claim could still be true for the wrong reason?
- Which missing dataset or institutional constraint could reverse the conclusion?
- What simple benchmark would make this phase unnecessary?
- How could revised data, survivorship, timestamp error or selection bias create a false success?
- What operational failure would make a valid research result unusable?

## Exit condition

The phase closes only after artifacts, tests and approvals are attached. Narrative completion, file count and word count do not close the phase.
