---
title: "09 WTI Crude Fundamental Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 09 WTI Crude Fundamental Engine

## Universe

WTI cash, futures, options, spreads and related equities.

## Driver hierarchy

US and global balance; inventories; production; refinery runs; products; exports; OPEC; freight; sanctions; weather.

## Production components

barrel balance; curve and basis; cracks; location stocks; options; producer hedging.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Reconcile physical and financial signals and distinguish temporary logistics from global scarcity.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
