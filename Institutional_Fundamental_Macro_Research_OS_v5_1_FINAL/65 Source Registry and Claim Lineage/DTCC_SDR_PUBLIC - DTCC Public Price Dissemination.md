---
title: "DTCC SDR — Public Price Dissemination"
type: source-contract
status: canonical
version: 21.3.0
created: 2026-08-09
updated: 2026-08-09
language: en
tags: [source-registry, observability-v21-3]
source_key: "DTCC_SDR_PUBLIC"
canonical_url: "https://pddata.dtcc.com/"
---
# DTCC SDR — Public Price Dissemination

## Official route
https://pddata.dtcc.com/

## Access / cadence
PUBLIC_FREE

## Institutional use
Publicly disseminated reportable swap/security-based-swap transaction and pricing data.

## Point-in-time / latency
Near-real-time subject to regulatory dissemination rules, corrections and cancellations.

## Hard boundaries
- Transaction notional is not net directional flow.
- Counterparty/client identity may be unavailable.
- Coverage is transactions reported to that repository, not the entire OTC market.

## Admission contract
Record publication/retrieval/reference times, exact table/file/product, units, corrections/cancellations where applicable, access class, and whether the observation is direct, aggregate, proxy or model inference. A registered source is not assumed available in a run.
