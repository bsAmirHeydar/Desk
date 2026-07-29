---
title: "15 Global Dollar and Cross-Border Funding"
type: program-phase
status: planned
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-transformation]
---
# 15 Global Dollar and Cross-Border Funding

## Mission

Map dollar credit, FX swaps, cross-currency basis, reserves, hedging demand, offshore balance sheets and stablecoin interfaces.

## Why this phase exists

This phase closes a specific gap between a large knowledge base and a production institutional capability. Work is not complete when prose exists; it is complete when the required artifacts can be independently reproduced, tested and governed.

## Dependencies

Phase 05, Phase 06, Phase 12

## Build scope

- Global liquidity database.
- CIP and basis-curve service.
- Cross-border funding stress map.

## Required artifacts

- architecture decision record;
- source and data contracts;
- implementation specification;
- test plan and expected failure cases;
- reproducible evidence package;
- ownership, review and retirement record;
- change log linked to claim and model IDs.

## Acceptance gates

- Onshore and offshore dollar conditions are separated.
- Hedging demand and intermediary constraints are measured.
- Stress indicators are validated against historical episodes.


## Red-team questions

- Which claim could still be true for the wrong reason?
- Which missing dataset or institutional constraint could reverse the conclusion?
- What simple benchmark would make this phase unnecessary?
- How could revised data, survivorship, timestamp error or selection bias create a false success?
- What operational failure would make a valid research result unusable?

## Exit condition

The phase closes only after artifacts, tests and approvals are attached. Narrative completion, file count and word count do not close the phase.
