---
title: "LBMA Gold Benchmark Auction and Precious-Metals Clock"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# LBMA Gold Benchmark Auction and Precious-Metals Clock

Gold has a benchmark clock distinct from COMEX and US macro releases. ICE Benchmark Administration runs electronic LBMA Gold Price auctions at **10:30 and 15:00 London time** (`SRC-ICE-LBMA`, `SRC-LBMA`).

## V15 objects
`LBMA_AM_AUCTION`, `LBMA_PM_AUCTION`, auction start, final-round publication latency, holiday/non-publication status, direct-participant context where publicly known, and overlap with London/NY session handoff or US macro data.

## Interpretation
The auction is a benchmark/physical-loco-London mechanism. It may concentrate transactions and influence short-window flow, but it does not automatically redefine the daily gold thesis.

## Collision examples
- LBMA PM auction near US data/Fed communication;
- London benchmark window during geopolitical shock;
- auction plus COMEX expiry/roll pressure;
- month-end asset allocation and FX translation.

## Output
The gold timing book must explicitly state the next LBMA benchmark window, whether it is relevant to the current Edge, and whether it is expected to be `NEUTRAL`, `FLOW_RELEVANT`, or `DOMINANT`.
