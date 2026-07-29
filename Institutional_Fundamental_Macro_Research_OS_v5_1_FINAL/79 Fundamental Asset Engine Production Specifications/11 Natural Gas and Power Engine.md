---
title: "11 Natural Gas and Power Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 11 Natural Gas and Power Engine

## Universe

regional gas, LNG and power markets.

## Driver hierarchy

weather; storage; production; pipelines; LNG; outages; fuel switching; power demand.

## Production components

degree-day models; storage balance; regional basis; shipping; generation stack.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Respect regional infrastructure and nonlinear weather sensitivity.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
