---
title: "CHI_NFCI — Chicago Fed — NFCI"
type: source
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - source-registry
  - official-source
  - chi-nfci
source_key: "CHI_NFCI"
canonical_url: "https://www.chicagofed.org/research/data/nfci/current-data"
---
# CHI_NFCI — Chicago Fed — NFCI

> [!source] Canonical institutional source
> **Source key:** `CHI_NFCI`  
> **Publisher/resource:** Chicago Fed — NFCI  
> **Canonical URL:** `https://www.chicagofed.org/research/data/nfci/current-data`

## Permitted use

Financial conditions and leverage/risk subindexes.

## Source contract

Record the exact dataset, series, table, release, document version, publication timestamp, reference period, units, seasonal adjustment, and retrieval timestamp. A homepage link is not a claim citation.

## Point-in-time requirements

- preserve raw responses or documents where licensing permits;
- store publication and ingestion timestamps separately;
- retain revisions rather than overwriting;
- record methodology changes and series breaks;
- test timezone, holiday, and late-release behavior;
- carry the source key into every derived feature and decision claim.

## Citation format

```text
[CHI_NFCI; series/table=<identifier>; reference=<period>;
 published=<timestamp>; vintage=<timestamp>; retrieved=<timestamp>;
 transformation=<code/version>]
```

## Reliability questions

1. Is the value an observation, estimate, forecast, or administrative record?
2. What population and exclusions define it?
3. How large and systematic are revisions?
4. What breaks comparability through time?
5. Which decision fields depend on it?
6. What substitute source exists during outage?

## Related standards

- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]]
- [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]]
