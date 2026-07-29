---
title: "10 Brent Crude Fundamental Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 10 Brent Crude Fundamental Engine

## Universe

Brent complex and global crude benchmarks.

## Driver hierarchy

Atlantic balance; OPEC; seaborne trade; grades; freight; sanctions; refinery demand.

## Production components

cargo and export data; spreads; grade differentials; floating storage.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Model benchmark-specific delivery and global marginal barrel.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
