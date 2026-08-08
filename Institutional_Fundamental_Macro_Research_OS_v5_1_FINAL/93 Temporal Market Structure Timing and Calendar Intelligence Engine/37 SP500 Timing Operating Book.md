---
title: "SP500 Timing Operating Book"
type: asset-specific-operating-book
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# SP500 Timing Operating Book

## Core clocks
- ES/MES Globex, settlement and quarterly SOQ (`SRC-CME-EQ-HOURS`, `SRC-CME-ES`);
- US cash open/close auctions (`SRC-NYSE-HOURS`, `SRC-NASDAQ-CROSS`);
- SPX/SPXW and ETF option expiries with product-specific AM/PM rules (`SRC-CBOE-SPX`, `SRC-OCC-INDEX`);
- S&P 500 quarterly rebalance/index maintenance (`SRC-SP500`, `SRC-SPDJI-METHOD`);
- broad earnings season and sector-weighted release clusters;
- Treasury auctions and real/nominal-rate clocks;
- US macro/FOMC;
- month-end/quarter-end futures/options and passive implementation.

## Breadth of clock exposure
SP500's broader sector mix means timing analysis must aggregate concurrent earnings and sector clocks rather than over-focus on one technology constituent.

## Close concentration
SPX-linked assets and passive funds can create substantial closing activity. Distinguish closing mechanical flow from a fundamental narrative transition.

## Expiry
Resolve whether the relevant option series is AM or PM settled and whether the day is routine daily/weekly, monthly or quarterly. Never use a generic “OpEx” flag.
