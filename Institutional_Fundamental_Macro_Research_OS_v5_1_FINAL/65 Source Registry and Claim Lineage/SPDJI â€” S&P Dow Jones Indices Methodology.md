---
title: "SPDJI — S&P Dow Jones Indices Methodology"
type: source
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - source-registry
  - official-source
  - spdji
source_key: "SPDJI"
canonical_url: "https://www.spglobal.com/spdji/en/documents/methodologies/"
---
# SPDJI — S&P Dow Jones Indices Methodology

> [!source] Canonical institutional source
> **Source key:** `SPDJI`  
> **Publisher/resource:** S&P Dow Jones Indices Methodology  
> **Canonical URL:** `https://www.spglobal.com/spdji/en/documents/methodologies/`

## Permitted use

S&P index construction, maintenance, rebalancing, and classification.

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
[SPDJI; series/table=<identifier>; reference=<period>;
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
