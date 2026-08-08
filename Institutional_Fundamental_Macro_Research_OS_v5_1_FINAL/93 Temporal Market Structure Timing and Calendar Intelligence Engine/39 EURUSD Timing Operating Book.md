---
title: "EURUSD Timing Operating Book"
type: asset-specific-operating-book
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# EURUSD Timing Operating Book

## Core clocks
- Asia -> London -> London/New York overlap -> New York FX participation;
- WMR 4pm London benchmark (`SRC-LSEG-WMR`);
- ECB Governing Council decision/press-conference sequence (`SRC-ECB-MEETINGS`);
- Federal Reserve calendar (`SRC-FED-CALENDAR`);
- Euro-area and US macro releases;
- ECB/TARGET/banking holidays and US holidays;
- month-end hedge/rebalance and WMR overlap;
- quarter-end cross-currency funding/basis constraints (`SRC-BIS-FX-LIQ`);
- CME EUR/USD futures expiry/roll as an institutional proxy where relevant (`SRC-CME-FX`).

## Important distinction
ECB reference rates are usually published around 16:00 CET but are **information-only** and not a WMR-equivalent transactional fixing (`SRC-ECB-FXREF`).

## Bilateral calendar
Every event is mapped to both EUR and USD blocks. A US holiday can reduce dollar-side participation while Europe remains open; a TARGET closure can alter euro settlement even when global FX quotes continue.

## Timing output
Identify dominant centre, next bilateral information event, next WMR benchmark, month/quarter-end state, funding state and DST overlap state. Timing may constrain BUY/SELL permission but may not choose EURUSD direction from session behavior.
