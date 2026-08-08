---
title: "Liquidity Availability Time-of-Day without Price Direction"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Liquidity Availability Time-of-Day without Price Direction

Liquidity is temporal, but V15 separates **liquidity availability** from directional analysis.

## Observables
- bid/ask spread and quoted depth where available;
- trade volume and participation;
- futures/spot basis stability;
- cross-venue continuity;
- funding liquidity and cross-currency basis;
- market-maker/dealer presence proxies;
- auction concentration;
- holiday/session staffing state.

BIS research shows FX liquidity can deteriorate when FX-swap funding liquidity deteriorates (`SRC-BIS-FX-LIQ`) and that time-of-day vulnerability can amplify order imbalances (`SRC-BIS-FLASH`).

## Temporal liquidity classes
`DEEP`, `NORMAL`, `THIN`, `FRAGILE`, `DISLOCATED`, `UNKNOWN`.

## Permission consequence
Liquidity can veto a **new entry** or shorten validity. It does not convert a bullish thesis to bearish. If execution costs/slippage data are unavailable for the broker instrument, state that limitation explicitly.

## No price-pattern leakage
A narrow range or quiet candles are not sufficient evidence of low institutional liquidity. Use direct/proxy liquidity evidence, not chart aesthetics.
