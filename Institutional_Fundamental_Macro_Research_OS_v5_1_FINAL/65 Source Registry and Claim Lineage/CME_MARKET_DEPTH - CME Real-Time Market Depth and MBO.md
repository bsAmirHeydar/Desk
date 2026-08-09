---
title: "CME Group — Market Depth / Market-by-Order"
type: source-contract
status: canonical
version: 21.3.0
created: 2026-08-09
updated: 2026-08-09
language: en
tags: [source-registry, observability-v21-3]
source_key: "CME_MARKET_DEPTH"
canonical_url: "https://www.cmegroup.com/market-data/real-time-and-historical-data.html"
---
# CME Group — Market Depth / Market-by-Order

## Official route
https://www.cmegroup.com/market-data/real-time-and-historical-data.html

## Access / cadence
SUBSCRIPTION_REQUIRED

## Institutional use
Trades, top of book, market depth and order-level/historical data for CME-listed products.

## Point-in-time / latency
Real-time/historical subscription data.

## Hard boundaries
- Displayed depth is not total latent liquidity.
- Futures book is not OTC FX/gold book.
- Capacity must be size/horizon/venue/state specific.

## Admission contract
Record publication/retrieval/reference times, exact table/file/product, units, corrections/cancellations where applicable, access class, and whether the observation is direct, aggregate, proxy or model inference. A registered source is not assumed available in a run.
