---
title: "Cash Futures Options ETF and Venue Synchronization"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Cash, Futures, Options, ETF and Venue Synchronization

US index exposure exists across cash constituents, index futures, index/ETF options and ETFs. These clocks are not identical.

## Required synchronization
For NASDAQ100/SP500/DJIA map:
- CME Globex session and maintenance/halts;
- US cash pre-open/core/close;
- Nasdaq/NYSE opening and closing auctions;
- index options and ETF options trading cutoffs;
- futures daily settlement markers;
- final settlement and SOQ mechanics;
- ETF creation/redemption and passive implementation windows when data are available.

## Why
A futures move at 08:30 ET after macro data occurs before the cash opening auction. At 09:30 ET, constituent opening prices and cash participation can validate or change transmission. At 16:00 ET, closing auctions and benchmark implementation can dominate volume while futures continue trading.

## State
`FUTURES_ONLY`, `PRE_CASH`, `CASH_DISCOVERY`, `FULL_CROSS_VENUE`, `CLOSE_CONCENTRATION`, `POST_CASH_FUTURES`, `EXPIRY_SETTLEMENT`.

The timing engine may require a post-open re-adjudication when the Edge relies materially on cash breadth/constituent transmission, but it must not use price pattern analysis to decide direction.
