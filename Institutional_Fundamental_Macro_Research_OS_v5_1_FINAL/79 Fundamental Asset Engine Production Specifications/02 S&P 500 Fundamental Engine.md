---
title: "02 S&P 500 Fundamental Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 02 S&P 500 Fundamental Engine

## Universe

S&P 500 index complex.

## Driver hierarchy

growth; margins; earnings revisions; rates; credit; sector composition; buybacks; issuance; passive flows.

## Production components

bottom-up earnings; profit bridge; ERP; sector breadth; credit confirmation; rebalance calendar.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Demonstrate incremental value over earnings-and-rates baselines.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
