---
title: "28 Positioning Systematic Flows and Dealer Constraints"
type: program-phase
status: planned
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-transformation]
---
# 28 Positioning Systematic Flows and Dealer Constraints

## Mission

Estimate CFTC positions, ETF flows, CTA exposures, volatility-control allocations, risk parity, dealer hedging and rebalancing.

## Why this phase exists

This phase closes a specific gap between a large knowledge base and a production institutional capability. Work is not complete when prose exists; it is complete when the required artifacts can be independently reproduced, tested and governed.

## Dependencies

Phase 26, Phase 27

## Build scope

- Positioning feature store.
- Transparent proxy and uncertainty framework.
- Flow-event database.

## Required artifacts

- architecture decision record;
- source and data contracts;
- implementation specification;
- test plan and expected failure cases;
- reproducible evidence package;
- ownership, review and retirement record;
- change log linked to claim and model IDs.

## Acceptance gates

- Estimated positions are never presented as observed facts.
- Models include mandate, rebalance frequency and leverage constraints.
- Flow effects are separated from fundamental information.


## Red-team questions

- Which claim could still be true for the wrong reason?
- Which missing dataset or institutional constraint could reverse the conclusion?
- What simple benchmark would make this phase unnecessary?
- How could revised data, survivorship, timestamp error or selection bias create a false success?
- What operational failure would make a valid research result unusable?

## Exit condition

The phase closes only after artifacts, tests and approvals are attached. Narrative completion, file count and word count do not close the phase.
