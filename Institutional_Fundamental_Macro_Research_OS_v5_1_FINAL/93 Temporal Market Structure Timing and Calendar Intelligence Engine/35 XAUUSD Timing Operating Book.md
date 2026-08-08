---
title: "XAUUSD Timing Operating Book"
type: asset-specific-operating-book
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# XAUUSD Timing Operating Book

## Primary clocks
1. London bullion participation and LBMA Gold Price auctions at 10:30/15:00 London (`SRC-ICE-LBMA`).
2. CME/COMEX gold futures session, settlement, expiry/roll/delivery calendar—resolved from the exact contract in live production.
3. US macro releases, especially inflation/labor/growth and Fed-path events (`SRC-BLS-CALENDAR`, `SRC-BEA-CALENDAR`, `SRC-FED-CALENDAR`).
4. London/New York overlap and USD/rates transmission window.
5. month/quarter/year-end FX/funding and portfolio-rebalance clocks.
6. holidays in London, US futures and relevant banking systems.

## Required timing synthesis
For every gold run identify: current bullion/futures session, next LBMA auction, next US macro/Fed clock, futures roll/expiry state, options-expiry state if data are available, month/quarter-end state, and whether dollar/rates liquidity centres are open.

## Gold-specific collisions
- LBMA PM + US macro/Fed communication;
- COMEX roll/expiry + benchmark auction;
- month-end WMR USD flows + gold benchmark;
- US holiday with London bullion open;
- geopolitical shock during thin Asia hours.

## Permission doctrine
Timing cannot decide gold direction. If fundamentals/narrative are bullish, Timing asks whether a benchmark/expiry/event/funding clock merely shortens validity or truly makes the new-entry window unusable. `Why Not Active?` must identify the exact temporal blocker.
