---
title: "Nasdaq — Net Order Imbalance Indicator (NOII)"
type: source-contract
status: canonical
version: 21.3.0
created: 2026-08-09
updated: 2026-08-09
language: en
tags: [source-registry, observability-v21-3]
source_key: "NASDAQ_NOII"
canonical_url: "https://www.nasdaqtrader.com/trader.aspx?id=openclose"
---
# Nasdaq — Net Order Imbalance Indicator (NOII)

## Official route
https://www.nasdaqtrader.com/trader.aspx?id=openclose

## Access / cadence
SUBSCRIPTION_REQUIRED

## Institutional use
Opening/closing-cross imbalance, paired shares and indicative-clearing information.

## Point-in-time / latency
Real-time around Nasdaq opening/closing cross; entitlement/data-feed access may be required.

## Hard boundaries
- Indicative imbalance is not executed flow until the cross.
- Index impact requires constituent weights and venue coverage.

## Admission contract
Record publication/retrieval/reference times, exact table/file/product, units, corrections/cancellations where applicable, access class, and whether the observation is direct, aggregate, proxy or model inference. A registered source is not assumed available in a run.
