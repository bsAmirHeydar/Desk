---
title: "NYSE — Auction Order Imbalances"
type: source-contract
status: canonical
version: 21.3.0
created: 2026-08-09
updated: 2026-08-09
language: en
tags: [source-registry, observability-v21-3]
source_key: "NYSE_ORDER_IMBALANCES"
canonical_url: "https://www.nyse.com/data-products/catalog/imbalances"
---
# NYSE — Auction Order Imbalances

## Official route
https://www.nyse.com/data-products/catalog/imbalances

## Access / cadence
SUBSCRIPTION_REQUIRED

## Institutional use
Real-time buy/sell imbalance publications during NYSE-group auctions.

## Point-in-time / latency
Real-time proprietary feed; historical TAQ imbalance data available separately.

## Hard boundaries
- Imbalance is not realized auction execution until the auction.
- Constituent imbalances must be aggregated using index weights.

## Admission contract
Record publication/retrieval/reference times, exact table/file/product, units, corrections/cancellations where applicable, access class, and whether the observation is direct, aggregate, proxy or model inference. A registered source is not assumed available in a run.
