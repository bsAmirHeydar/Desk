---
title: "02 Multi-Clock Temporal Ontology"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Multi-Clock Temporal Ontology

A live market is governed by simultaneous clocks:

1. **Micro clock:** seconds/minutes around auctions, release timestamps, fixes, option expiries, settlement markers and halts.
2. **Session clock:** Asia/Tokyo, London/Europe, New York, futures-to-cash handoff, opening discovery, midday, closing concentration.
3. **Daily clock:** business-day conventions, daily settlements, Treasury auctions, policy releases, benchmark publication.
4. **Weekly clock:** weekly options, recurring data days, weekend/long-weekend exposure.
5. **Monthly clock:** month-end benchmark rebalancing, FX hedge resets, NAV/closing flows, month-end derivatives.
6. **Quarterly clock:** futures/options expiry, index review, earnings season, bank/dealer balance-sheet reporting, cross-currency funding.
7. **Annual/fiscal clock:** year-end balance sheets, tax/fiscal boundaries, annual index reconstitution, holiday clusters.
8. **Contract-lifecycle clock:** listing, liquidity migration, roll, last trade, notice/delivery, final settlement.

The engine ranks these clocks by causal materiality, not proximity alone.
