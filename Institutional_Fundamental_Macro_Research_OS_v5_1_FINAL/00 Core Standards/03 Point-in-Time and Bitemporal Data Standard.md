---
title: "03 Point-in-Time and Bitemporal Data Standard"
type: standard
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - institutional-standard
  - fundamental-research
  - governance
---
# 03 Point-in-Time and Bitemporal Data Standard

> [!abstract] Purpose
> Prevent future information, revised history, and silent data replacement from entering research or backtests.

## Two times are mandatory

Every observation has at least:

- **valid time** — period or instant the value describes;
- **system time** — instant the value became available to the research system.

A third timestamp is often required:

- **source publication time** — official release instant;
- **ingestion time** — when the internal system captured it;
- **decision cutoff** — latest admissible timestamp for a decision.

\[
x = x(entity,\ valid\_time,\ source\_vintage,\ system\_time)
\]

## Immutable raw layer

Raw files and payloads are append-only. Corrections create new vintages. They never overwrite prior values. The raw layer stores source metadata, retrieval response, publication timestamp, checksum, and parser version.

## Curated point-in-time layer

Transformations must use only observations whose source publication time is no later than the simulated decision time. A pseudo-real-time query is:

\[
\mathcal I_t=\{x_{s}^{(v)}: release\_time(s,v)\le t\}
\]

Seasonal factors, constituent lists, classifications, corporate share counts, and benchmark weights are also time-varying data and need vintage control.

## Revision decomposition

Measure:

- first release;
- latest available at each historical decision date;
- current final estimate;
- revision from first to second;
- benchmark revision;
- methodological break;
- effect on the signal and decision.

The goal is not always to forecast final truth. Markets trade the value released at the time, the revision, and the perceived reliability of the measurement process.

## Calendar engine

A release calendar records timezone, daylight saving, embargo, expected publication, actual publication, early/late release, reference period, and simultaneous releases. Market timestamps must be synchronized to the same clock.

## Corporate and market data

Point-in-time control applies to:

- filings and amendments;
- earnings consensus and estimate history;
- index membership and free float;
- ratings and outlooks;
- futures deliverable baskets;
- option chains and corporate actions;
- COT classifications;
- fund holdings and restatements.

## Acceptance tests

- no query can return a vintage unavailable at the requested timestamp;
- first-release and final-vintage series differ where revisions exist;
- backtests reproduce historical constituent universes;
- timezone and DST tests cover event boundaries;
- parser changes are versioned and replayable;
- source outages and late arrivals are logged;
- model features carry maximum-source timestamp;
- every decision stores a data snapshot ID.

## Related

- [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]]
- [[72 Historical Research Permission and Alpha Validation Laboratory/01 Bitemporal Research Database Architecture]]
- [[55 Data Platform Ontology Lineage and Governance/00 MOC]]
