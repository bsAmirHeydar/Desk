---
title: "Timing Learning Promotion, Calibration and Governance"
type: learning-governance
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, learning, governance]
---
# Timing Learning Promotion, Calibration and Governance

## Learning objects
Learn only from immutable prior temporal states. Mature the relevant window before judging it.

Error classes include: `CLOCK_MISSED`, `CLOCK_FALSE_POSITIVE`, `WRONG_DOMINANT_ROOT`, `OVER_VETO`, `UNDER_VETO`, `VALIDITY_TOO_SHORT`, `VALIDITY_TOO_LONG`, `HAZARD_WINDOW_TOO_EARLY`, `HAZARD_WINDOW_TOO_LATE`, `TIME_BUDGET_ERROR`, `SCHEDULER_FEASIBILITY_ERROR`, `LATENCY_STALENESS_ERROR`, `REFERENCE_MARKET_MAPPING_ERROR`, `SOURCE_REVISION_ERROR`, `DEPENDENCY_DOUBLE_COUNT`, `MECHANICAL_SIGN_ERROR`, `NO_ERROR`.

## Hindsight firewall
Outcome can diagnose whether a prior timing decision was costly; it cannot prove a clock or mechanism that was not observable at the prior timestamp. Reconstruct the prior evidence set before proposing a change.

## Promotion
`OBSERVATION → CANDIDATE → VALIDATED → CANONICAL`.

Promotion requires repeated forward cases, rival explanation checks, asset/regime scope definition, failure examples and evidence that the change improves timing value rather than merely fitting one drawdown or one missed winner.

## Threshold governance
Event buffers, safe-window rules, clock materiality and veto criteria cannot be tuned on a single historical sample. Prefer forward calibration and preserve control-arm comparisons.
