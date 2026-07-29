---
title: "20 Fundamental Portfolio Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 20 Fundamental Portfolio Engine

## Universe

multi-asset portfolio and hedges.

## Driver hierarchy

expected returns; scenarios; common drivers; correlations; liquidity; financing; convexity; concentration.

## Production components

factor map; scenario P&L; optimizer; risk budgets; stress and exit capacity.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Beat simple allocation baselines while satisfying independent risk and liquidity limits.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
