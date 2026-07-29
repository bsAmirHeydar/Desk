---
title: "UST_TIC — U.S. Treasury International Capital System"
type: source
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - source-registry
  - official-source
  - ust-tic
source_key: "UST_TIC"
canonical_url: "https://home.treasury.gov/data/treasury-international-capital-system-tic"
---
# UST_TIC — U.S. Treasury International Capital System

> [!source] Canonical institutional source
> **Source key:** `UST_TIC`  
> **Publisher/resource:** U.S. Treasury International Capital System  
> **Canonical URL:** `https://home.treasury.gov/data/treasury-international-capital-system-tic`

## Permitted use

Cross-border securities holdings, banking claims, and international capital flows.

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
[UST_TIC; series/table=<identifier>; reference=<period>;
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
