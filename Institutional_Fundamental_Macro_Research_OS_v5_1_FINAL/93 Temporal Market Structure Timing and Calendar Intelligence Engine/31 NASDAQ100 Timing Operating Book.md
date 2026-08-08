---
title: "31 NASDAQ100 Timing Operating Book"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# NASDAQ100 Timing Operating Book

Core clocks: NQ/MNQ Globex, US 08:30/10:00 ET macro, Nasdaq cash Opening/Closing Cross, constituent earnings/calls, NDX/QQQ option expiries, futures quarterly roll/SOQ, Nasdaq-100 review/rebalance/reconstitution, FOMC, Treasury/rates, month/quarter-end.

Key sequence: `OVERNIGHT_FUTURES -> 08:30_MACRO -> 09:30_CASH_DISCOVERY -> CONTINUOUS -> 15:50_CLOSE_IMBALANCE -> 16:00_CLOSE -> POST_CLOSE_EARNINGS`.

High-weight constituent after-hours releases create a pre-cash information state; cash-open breadth may be required for transmission validation without using technical direction.
