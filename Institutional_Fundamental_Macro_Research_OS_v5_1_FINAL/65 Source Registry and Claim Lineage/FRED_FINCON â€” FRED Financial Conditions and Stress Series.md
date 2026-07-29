---
title: "FRED_FINCON — FRED Financial Conditions and Stress Series"
type: source
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - source-registry
  - official-source
  - fred-fincon
source_key: "FRED_FINCON"
canonical_url: "https://fred.stlouisfed.org/"
---
# FRED_FINCON — FRED Financial Conditions and Stress Series

> [!source] Canonical institutional source
> **Source key:** `FRED_FINCON`  
> **Publisher/resource:** FRED Financial Conditions and Stress Series  
> **Canonical URL:** `https://fred.stlouisfed.org/`

## Permitted use

Financial conditions, stress, spreads, rates, credit, and macro market series.

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
[FRED_FINCON; series/table=<identifier>; reference=<period>;
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
