---
title: "Index Rebalance Reconstitution and Implementation Clock"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Index Rebalance, Reconstitution and Implementation Clock

Index maintenance produces predictable **implementation obligations** for passive and benchmark-aware capital, but timing varies by provider and methodology.

## Lifecycle
`METHODOLOGY_RULE -> REFERENCE_DATE -> ANNOUNCEMENT -> PRO_FORMA/WEIGHT_PUBLICATION -> IMPLEMENTATION_WINDOW -> EFFECTIVE_DATE -> POST_REBALANCE_NORMALIZATION`.

## Required distinctions
- rebalance: weights/shares adjusted;
- reconstitution: membership reviewed;
- corporate-action change: unscheduled/event-driven maintenance;
- special rebalance: concentration/governance event;
- fast entry/deletion when methodology permits.

## S&P/Dow
Use S&P DJI methodology and calendars (`SRC-SPDJI-METHOD`, `SRC-SP500`, `SRC-DJIA`).

## Nasdaq-100
Use current Nasdaq methodology because the framework changed in 2026; quarterly review/rebalance and annual processes must be retrieved dynamically (`SRC-NASDAQ-NDX-2026`).

## Directional discipline
A rebalance can create stock-specific and index-close flows. V15 does not infer the sign of index-level pressure without constituent weight changes and implementation data. Unknown sign = `MECHANICAL_FORCE_UNDETERMINED`.
