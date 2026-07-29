---
title: "13 Credit Fundamental Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 13 Credit Fundamental Engine

## Universe

cash bonds, CDS, indices and options.

## Driver hierarchy

default risk; recovery; refinancing; liquidity; rates; earnings; covenants; dealer balance sheets.

## Production components

expected loss; spread decomposition; maturity walls; fund flows; stress scenarios.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Measure liquidity premium separately and validate against issuer fundamentals.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
