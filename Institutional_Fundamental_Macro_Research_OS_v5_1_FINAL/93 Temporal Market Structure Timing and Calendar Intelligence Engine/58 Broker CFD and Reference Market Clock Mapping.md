---
title: "Broker CFD and Reference Market Clock Mapping"
type: canonical-instrument-standard
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, cfd, reference-market]
---
# Broker CFD and Reference Market Clock Mapping

Alpha Lab deployment symbols can be CFDs or broker aliases while timing mechanisms originate in reference markets.

## Mapping object
For each deployed symbol resolve:
- broker symbol / venue if known;
- economic underlying;
- primary reference index/spot/benchmark;
- relevant futures/options proxies;
- cash-market session if applicable;
- benchmark/fixing calendar;
- broker trading-hours/maintenance schedule when available.

## Examples
- `NASDAQ100` CFD: reference NDX/Nasdaq cash constituents plus NQ/MNQ derivatives clocks; broker CFD hours are not the same as Nasdaq cash opening/closing mechanisms.
- `SP500` CFD: SPX cash/index ecosystem plus ES/MES derivatives clocks.
- `DJIA` CFD: DJIA cash/index methodology plus YM/MYM derivatives clocks.
- `XAUUSD`: OTC spot/reference pricing plus LBMA benchmark and COMEX derivatives lifecycle; do not pretend spot gold has a single centralized exchange session.
- `EURUSD` / `USDJPY`: OTC FX calendar plus relevant currency business days, WMR benchmark and CME FX proxies where useful.

## Rule
A reference-market clock can constrain the economic expression even if the CFD itself is technically open. Conversely, a CFD maintenance closure can block execution even when the reference market is open. Store both layers separately.
