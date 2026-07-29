---
title: "01 Nasdaq 100 Fundamental Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 01 Nasdaq 100 Fundamental Engine

## Universe

Nasdaq-100 cash index, futures, options and liquid proxies.

## Driver hierarchy

policy path; real yields; term premium; earnings and guidance; semiconductor capital cycle; concentration; credit; dollar; options and systematic flow.

## Production components

bottom-up index earnings; rate sensitivity by regime; sector leadership; constituent and weight history; implied distribution; liquidity.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Separate cash-flow, discount-rate, risk-premium and mechanical-flow contributions. Evaluate intraday and multi-day decisions point in time.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
