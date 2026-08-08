---
title: "Dynamic Calendar Retrieval Source Registry and Provenance"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Dynamic Calendar Retrieval, Source Registry and Provenance

The Vault stores **timing science**, not a frozen calendar.

## Dynamic retrieval hierarchy
1. exchange/clearinghouse/index provider/benchmark administrator;
2. central bank/statistical agency/Treasury/government source;
3. regulated market association or official calendar;
4. licensed institutional calendar/data vendor;
5. high-quality secondary source only when primary is unavailable.

## Never hard-code forever
Market hours, index methodology, option programs and benchmark administration change. Nasdaq-100 methodology changed in 2026 (`SRC-NASDAQ-NDX-2026`), illustrating why each run must retrieve the current rule set when material.

## Source ledger
Root `V15_SOURCE_LEDGER.csv` is the baseline registry. Live runs record URL/source ID, retrieval time, source-local date, effective date, and whether the rule is current or historical.

## Calendar compiler
The production engine builds a normalized calendar for the target horizons, resolves timezones/DST/holidays, detects collisions and emits only events causally relevant to the six target markets.

## Licensed data
Options positioning, benchmark flows and some real-time auction/market-depth data can be licensed. Mark them `UNAVAILABLE` or use an explicit proxy; never synthesize proprietary observations.
