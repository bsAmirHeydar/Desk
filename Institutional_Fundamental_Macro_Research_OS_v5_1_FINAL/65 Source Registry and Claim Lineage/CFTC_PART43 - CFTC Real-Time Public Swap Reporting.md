---
title: "CFTC Part 43 — Real-Time Public Swap Reporting"
type: source-contract
status: canonical
version: 21.3.0
created: 2026-08-09
updated: 2026-08-09
language: en
tags: [source-registry, observability-v21-3]
source_key: "CFTC_PART43_FRAMEWORK"
canonical_url: "https://www.cftc.gov/LawRegulation/DoddFrankAct/Rulemakings/DF_18_RealTimeReporting/index.htm"
---
# CFTC Part 43 — Real-Time Public Swap Reporting

## Official route
https://www.cftc.gov/LawRegulation/DoddFrankAct/Rulemakings/DF_18_RealTimeReporting/index.htm

## Access / cadence
PUBLIC_FREE

## Institutional use
Defines the legal/public-reporting framework used to interpret SDR transaction feeds.

## Point-in-time / latency
Rule/event driven; actual transaction clocks belong to the SDR dissemination record.

## Hard boundaries
- Part 43 framework is not itself a transaction tape.
- Block/large-notional delays and caps must remain visible.
- Public swap prints do not identify client intent.

## Admission contract
Record publication/retrieval/reference times, exact table/file/product, units, corrections/cancellations where applicable, access class, and whether the observation is direct, aggregate, proxy or model inference. A registered source is not assumed available in a run.
