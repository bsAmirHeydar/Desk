---
title: "05 Cash Futures Options ETF and Venue Synchronization"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Cash, Futures, Options, ETF and Venue Synchronization

US equity-index exposure exists across futures, cash constituents, ETFs and options with different clocks. Resolve all clocks before judging timing.

For NASDAQ100/SP500/DJIA track CME Globex, cash pre-open/core/close, Nasdaq/NYSE opening and closing auctions, ETF/options trading cutoffs, daily futures settlement, quarterly final settlement/SOQ and rebalance implementation.

Temporal states include `FUTURES_ONLY`, `PRE_CASH`, `CASH_DISCOVERY`, `FULL_CROSS_VENUE`, `CLOSE_CONCENTRATION`, `POST_CASH_FUTURES`, `EXPIRY_SETTLEMENT`.

A futures move after 08:30 ET macro data occurs before cash breadth is fully observable. A 09:30 ET cash open can therefore be a **transmission confirmation clock** without becoming technical analysis.
