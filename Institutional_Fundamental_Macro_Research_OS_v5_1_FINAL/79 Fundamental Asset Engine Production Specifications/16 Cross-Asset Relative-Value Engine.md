---
title: "16 Cross-Asset Relative-Value Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 16 Cross-Asset Relative-Value Engine

## Universe

pairs, curves, spreads and hedged baskets.

## Driver hierarchy

common and differential drivers; valuation; carry; basis; liquidity; convexity; catalyst.

## Production components

factor-neutralization; hedge ratios; scenario P&L; crowding; cost.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Prove factor purity and hedge stability under stress.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
