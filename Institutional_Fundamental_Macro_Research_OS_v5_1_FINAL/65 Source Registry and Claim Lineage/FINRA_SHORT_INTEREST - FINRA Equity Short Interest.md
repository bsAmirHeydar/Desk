---
title: "FINRA — Equity Short Interest"
type: source-contract
status: canonical
version: 21.3.0
created: 2026-08-09
updated: 2026-08-09
language: en
tags: [source-registry, observability-v21-3]
source_key: "FINRA_SHORT_INTEREST"
canonical_url: "https://www.finra.org/finra-data/browse-catalog/equity-short-interest"
---
# FINRA — Equity Short Interest

## Official route
https://www.finra.org/finra-data/browse-catalog/equity-short-interest

## Access / cadence
PUBLIC_DELAYED

## Institutional use
Reported equity short positions on designated settlement dates.

## Point-in-time / latency
Delayed snapshot; current reporting cadence must be read from FINRA rules/schedule at run time.

## Hard boundaries
- Short interest is a stock, not daily flow.
- Do not equate with short-sale volume.

## Admission contract
Record publication/retrieval/reference times, exact table/file/product, units, corrections/cancellations where applicable, access class, and whether the observation is direct, aggregate, proxy or model inference. A registered source is not assumed available in a run.
