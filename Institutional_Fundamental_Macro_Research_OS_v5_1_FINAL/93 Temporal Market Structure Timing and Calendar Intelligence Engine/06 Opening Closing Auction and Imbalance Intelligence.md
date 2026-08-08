---
title: "06 Opening Closing Auction and Imbalance Intelligence"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Opening, Closing, Auction and Imbalance Intelligence

Opening/closing auctions concentrate institutional orders. Track venue-specific imbalance dissemination, freeze periods, cross times and effective benchmark/index implementation overlap.

Opening auction = overnight inventory clearing + cash constituent discovery. Closing auction = benchmarked execution, passive/index orders, mutual-fund/ETF implementation and market-on-close concentration.

Classify observed close pressure as `FUNDAMENTAL_CONTINUATION`, `BENCHMARK_MECHANICAL`, `REBALANCE_MECHANICAL`, `DE_RISKING`, or `UNDETERMINED`.

Mechanical close flow may shorten validity or create `MECHANICAL_FLOW_DOMINANT`; it does not invalidate the fundamental thesis by itself.
