---
title: "NASDAQ100 Timing Operating Book"
type: asset-specific-operating-book
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# NASDAQ100 Timing Operating Book

## Core clocks
- NQ/MNQ Globex session, daily settlement and quarterly expiry/SOQ (`SRC-CME-EQ-HOURS`);
- Nasdaq cash Opening/Closing Cross and imbalance dissemination (`SRC-NASDAQ-CROSS`);
- NDX/QQQ options expiry families and product-specific cutoffs (`SRC-OCC-INDEX`, Nasdaq/Cboe sources as applicable);
- Nasdaq-100 quarterly review/rebalance and annual reconstitution under the **current** methodology (`SRC-NASDAQ-NDX-2026`);
- mega-cap/semiconductor earnings release and call sequence;
- 08:30/10:00 ET US macro data and FOMC stages;
- Treasury auctions/rate-market clocks;
- month/quarter-end passive and balance-sheet flows.

## Key handoffs
`OVERNIGHT_FUTURES -> 08:30_MACRO -> 09:30_CASH_DISCOVERY -> CONTINUOUS -> 15:50_CLOSE_IMBALANCE -> 16:00_CLOSE -> POST_CLOSE_EARNINGS`.

## Special risk
Nasdaq is concentration-sensitive. An after-hours release from a top-weight constituent can create a new information clock before cash breadth is observable. Timing schedules a cash-open re-adjudication when constituent adoption matters.

## Rebalance discipline
Do not infer index-level flow direction from “rebalance day.” Use actual additions/removals/weights and effective timing; otherwise state mechanical direction as unknown.
