---
source_id: CME_VOLUME_OI
type: source-contract
status: canonical
version: 21.3.0
created: 2026-08-09
updated: 2026-08-09
language: en
tags: [source-registry, observability-v21-3]
---
# CME Group — Volume and Open Interest

## Official route
https://www.cmegroup.com/market-data/volume-open-interest.html

## Institutional use
Exchange-published futures/options volume and open interest.

## Cadence / latency
Daily / product-specific

## Hard boundaries
- Volume is activity, not net directional flow.
- Open interest is outstanding contracts, not identified long/short participant flow.

## Admission contract
Preserve event/reference/publication/retrieval times, exact table/file/product or release identifier, units, revisions/corrections, and access class. Registration never implies that the source was available or retrieved in a particular run.
