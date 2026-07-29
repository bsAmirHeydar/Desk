---
title: "06 Japan Yen Fundamental Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 06 Japan Yen Fundamental Engine

## Universe

JPY crosses, JGBs, swaps and options.

## Driver hierarchy

BoJ reaction; wages; inflation; yield policy; carry; intervention; repatriation; global volatility.

## Production components

policy-path scenarios; real yields; intervention records; hedging costs; options.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Distinguish monetary divergence, carry unwind and official intervention.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
