---
source_id: SEC_NPORT
type: source-contract
status: canonical
version: 21.3.0
created: 2026-08-09
updated: 2026-08-09
language: en
tags: [source-registry, observability-v21-3]
---
# SEC — Form N-PORT

## Official route
https://www.sec.gov/data-research/sec-markets-data/form-n-port-data-sets

## Institutional use
Regulated investment-company portfolio holdings and related monthly reporting data.

## Cadence / latency
Monthly / public-data release lag

## Hard boundaries
- N-PORT holdings are not intraday fund flow.
- Publication/release lag must be respected in historical replay.

## Admission contract
Preserve event/reference/publication/retrieval times, exact table/file/product or release identifier, units, revisions/corrections, and access class. Registration never implies that the source was available or retrieved in a particular run.
