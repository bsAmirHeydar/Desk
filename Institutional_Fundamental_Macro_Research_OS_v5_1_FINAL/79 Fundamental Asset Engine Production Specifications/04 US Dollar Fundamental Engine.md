---
title: "04 US Dollar Fundamental Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 04 US Dollar Fundamental Engine

## Universe

DXY, broad dollar, spot, forwards and funding markets.

## Driver hierarchy

relative policy; global risk; dollar funding; external balances; hedging; reserves; commodity trade.

## Production components

cross-currency basis; carry; valuation; balance-sheet dollar demand; options.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Separate safe-haven, policy-divergence and funding-scarcity regimes.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
