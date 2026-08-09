---
title: "Cboe DataShop — Options Open-Close Volume"
type: source-contract
status: canonical
version: 21.3.0
created: 2026-08-09
updated: 2026-08-09
language: en
tags: [source-registry, observability-v21-3]
source_key: "CBOE_OPEN_CLOSE_OPTIONS"
canonical_url: "https://datashop.cboe.com/cboe-options-open-close-volume-summary"
---
# Cboe DataShop — Options Open-Close Volume

## Official route
https://datashop.cboe.com/cboe-options-open-close-volume-summary

## Access / cadence
SUBSCRIPTION_REQUIRED

## Institutional use
Participant/action/open-close classified options volume where subscribed.

## Point-in-time / latency
EOD and intraday products are subscription data; cadence depends product.

## Hard boundaries
- Participant-class activity is not a complete dealer book.
- Buy/sell/open/close labels need position context before gamma/hedging inference.

## Admission contract
Record publication/retrieval/reference times, exact table/file/product, units, corrections/cancellations where applicable, access class, and whether the observation is direct, aggregate, proxy or model inference. A registered source is not assumed available in a run.
