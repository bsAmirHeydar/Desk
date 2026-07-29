---
title: "12 Copper and Industrial Metals Engine"
type: asset-engine-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [asset-engine, fundamental-research]
---
# 12 Copper and Industrial Metals Engine

## Universe

copper and major industrial metals.

## Driver hierarchy

China and global activity; construction; grids; manufacturing; mine supply; smelters; inventories; scrap.

## Production components

physical balance; treatment charges; warehouse stocks; regional premiums; curve.

## Required state objects

Structural, cyclical, tactical, multi-day, intraday and event states are stored separately. Each includes a market-implied baseline, pricing gap, causal and rival models, confirmations, uncertainty, half-life, invalidation and expiry.

## Data and evidence

Every input must resolve to the source registry, data dictionary, admissible vintage and transformation version. Estimated positioning or flow is explicitly distinguished from observed data.

## Validation gate

Separate cyclical demand, structural transition and temporary inventory relocation.

## Monitoring

Monitor data freshness, model drift, sensitivity changes, liquidity, cost, scenario loss and the quality of causal confirmation.
