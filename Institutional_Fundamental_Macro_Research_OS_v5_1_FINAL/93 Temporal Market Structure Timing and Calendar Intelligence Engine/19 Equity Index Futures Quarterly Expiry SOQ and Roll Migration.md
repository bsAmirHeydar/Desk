---
title: "Equity Index Futures Quarterly Expiry SOQ and Roll Migration"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Equity Index Futures Quarterly Expiry, SOQ and Roll Migration

ES/NQ/YM and related Micro E-mini contracts use the March/June/September/December quarterly cycle. CME's Micro E-mini documentation states final settlement uses the corresponding Special Opening Quotation on the third Friday (`SRC-CME-EQ-HOURS`).

## Distinguish three clocks
1. **liquidity roll** — when volume migrates to the next contract;
2. **last trade/expiry** — product rule;
3. **SOQ/final settlement** — component opening-price calculation.

These need not occur at the same moment.

## Institutional implications
During roll migration, spread/basis activity can be large without representing a change in outright fundamental direction. On settlement morning, opening prices of constituents become directly relevant to settlement mechanics. When quarterly index rebalance or option expiry overlaps, V15 creates a `QUARTERLY_EXPIRY_COLLISION` state.

## Edge rule
A fundamental index Edge can remain valid through roll season if the chosen execution symbol maps correctly and liquidity is adequate. Timing can veto a specific contract expression without vetoing the index thesis.
