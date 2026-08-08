---
title: "Options Expiration Daily Weekly Monthly Quarterly and 0DTE"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Options Expiration: Daily, Weekly, Monthly, Quarterly and 0DTE

Modern US index complexes have multiple overlapping expiration families. OCC documents weekly and quarterly programs (`SRC-OCC-WEEKLY`, `SRC-OCC-QUARTERLY`), while Cboe and Nasdaq publish product-specific hours and settlement rules.

## Required distinctions
- same-day/0DTE versus future expiry;
- weekly versus standard monthly;
- quarterly/end-of-quarter;
- index option versus ETF option;
- AM versus PM settlement;
- cash-settled versus physical/deliverable;
- regular versus holiday-shortened session;
- exercise style and last trading time.

## Dealer-flow caution
Gamma/hedging effects can be material, but V15 may only use them when options positioning data are observable and appropriately licensed/proxied. “Large gamma” must never be invented from price behavior.

## Temporal state
`NO_MAJOR_EXPIRY`, `ROUTINE_DAILY_EXPIRY`, `CONCENTRATED_WEEKLY`, `MONTHLY_EXPIRY`, `QUARTERLY_EXPIRY`, `0DTE_HIGH_NOTIONAL`, `POSITIONING_UNKNOWN`.

## Edge interaction
Options expiry can be a temporary mechanical-force modifier or execution-risk constraint. It does not automatically reverse the fundamental/narrative direction.
