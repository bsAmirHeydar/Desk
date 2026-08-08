---
title: "WMR FX Benchmark Fixing and Reference-Rate Intelligence"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# WMR FX Benchmark, Fixing and Reference-Rate Intelligence

Benchmark clocks can create concentrated execution that is mechanical rather than informational.

## WMR
LSEG's WMR FX Benchmarks include daily 4:00 p.m. London closing spot rates (`SRC-LSEG-WMR`). For asset managers benchmarked to these rates, hedge/rebalance implementation can concentrate around the fix.

V15 tracks:
- benchmark time in London local time with DST normalization;
- month/quarter-end overlap;
- known or inferred benchmark-related flow only when evidence exists;
- whether the flow reinforces or opposes the fundamental FX thesis;
- expected decay after the fixing window.

## Reference-rate distinction
Do not confuse a published reference rate with a transactional fixing. ECB reference rates are information-only and based on a concertation procedure; transaction use is strongly discouraged (`SRC-ECB-FXREF`). The system labels them `REFERENCE_NON_TRANSACTIONAL` rather than treating them as WMR-like flow events.

## Governance
Never manufacture a month-end “fix direction” from price action. Directional benchmark-flow estimates require a documented rebalancing/hedging model, licensed data, or explicit high-quality proxy and must carry confidence limits.
