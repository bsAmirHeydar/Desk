---
title: "36 Six-Market Global Clock Graph"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Six-Market Global Clock Graph

Build one common clock graph before individual symbol analysis. Shared nodes include US macro/FOMC/Treasury, NY cash open/close, London/NY overlap, WMR, month/quarter/year-end, US holidays and major shocks.

Add asset overlays: LBMA/COMEX for XAUUSD; Nasdaq crosses/NDX methodology/earnings for NQ; SPX options/S&P rebalance for SP500; price-weighted constituent events for DJIA; ECB/TARGET for EURUSD; BoJ/Japan fiscal/banking clocks for USDJPY.

A single shared clock can expire all six permissions simultaneously; treat that as common exposure, not six independent vetoes.
