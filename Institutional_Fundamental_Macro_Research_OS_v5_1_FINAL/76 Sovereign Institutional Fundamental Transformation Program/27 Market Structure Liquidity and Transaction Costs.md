---
title: "27 Market Structure Liquidity and Transaction Costs"
type: program-phase
status: planned
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-transformation]
---
# 27 Market Structure Liquidity and Transaction Costs

## Mission

Measure order books, auctions, spreads, depth, impact, settlement, basis and intermediary capacity without price-pattern analysis.

## Why this phase exists

This phase closes a specific gap between a large knowledge base and a production institutional capability. Work is not complete when prose exists; it is complete when the required artifacts can be independently reproduced, tested and governed.

## Dependencies

Phase 06, Phase 13, Phase 26

## Build scope

- Trade and quote data model.
- Transaction-cost analysis.
- Auction and liquidity-regime analytics.

## Required artifacts

- architecture decision record;
- source and data contracts;
- implementation specification;
- test plan and expected failure cases;
- reproducible evidence package;
- ownership, review and retirement record;
- change log linked to claim and model IDs.

## Acceptance gates

- Clock synchronization and venue rules are correct.
- Impact models are evaluated out of sample.
- Research distinguishes information effects from mechanical flow.


## Red-team questions

- Which claim could still be true for the wrong reason?
- Which missing dataset or institutional constraint could reverse the conclusion?
- What simple benchmark would make this phase unnecessary?
- How could revised data, survivorship, timestamp error or selection bias create a false success?
- What operational failure would make a valid research result unusable?

## Exit condition

The phase closes only after artifacts, tests and approvals are attached. Narrative completion, file count and word count do not close the phase.
