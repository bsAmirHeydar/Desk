---
title: "03 US Rates Fundamental Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 03 US Rates Fundamental Engine

## Universe

Treasuries, OIS, futures, swaps and options.

## Driver hierarchy

policy path; inflation; growth; term premium; issuance; repo; dealer capacity; foreign demand; mortgage convexity.

## Production components

zero curves; term-premium models; auction and CTD analytics; key-rate risks; volatility surface.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Reconcile instruments and distinguish expected-rate, inflation and term-premium shocks.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
