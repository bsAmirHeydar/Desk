---
title: "Month-End Portfolio Rebalance FX Hedge and Benchmark Flow"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Month-End Portfolio Rebalance, FX Hedge and Benchmark Flow

Month-end is a family of mechanisms, not a statistical slogan.

## Potential mechanisms
- benchmark tracking and asset-allocation rebalance;
- currency hedge reset after equity/bond performance changes;
- WMR 4pm London benchmark execution;
- mutual-fund/NAV-related closing flows;
- futures/options month-end products and expiries;
- accounting/reporting inventory adjustments;
- index maintenance/effective dates;
- collateral and cash management.

## Evidence hierarchy
1. documented benchmark/rebalance rule or fund mandate;
2. observable index/futures/options implementation data;
3. quantified asset-performance-based hedge model with declared assumptions;
4. institutional flow proxy;
5. anecdotal “month-end effect” — insufficient for directional authority.

## Temporal windows
Distinguish final trading day, final business day, WMR fix, US cash close and any earlier local-market closes. The strongest window can differ between EURUSD, USDJPY and US indices.

## Edge interaction
Month-end can create `TEMPORAL_MECHANICAL_FORCE` that temporarily reinforces/opposes fundamentals. If direction of the flow is uncertain, it can still reduce confidence or shorten validity without inventing a sign.

## Learning
Track predicted benchmark-flow sign separately from realized price. A wrong price move does not prove the flow estimate wrong unless transaction/flow evidence supports that conclusion.
