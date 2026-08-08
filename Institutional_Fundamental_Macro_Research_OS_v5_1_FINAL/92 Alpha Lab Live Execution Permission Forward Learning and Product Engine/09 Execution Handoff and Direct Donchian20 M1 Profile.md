---
title: "Execution Handoff and Direct Donchian20 M1 Profile"
type: execution-handoff-contract
status: active-deployment
version: 14.1.0
---
# Execution Handoff and Direct Donchian20 M1 Profile

## Architecture
```text
Full fundamental + narrative brain
→ Edge Engine
→ BUY / SELL / NO_TRADE
→ M1 Donchian-20 trigger
→ 4 ATR initial stop
→ candle-by-candle trailing exit
```

## Permission mapping
- `EDGE_ACTIVE` + bullish approved direction → `BUY`
- `EDGE_ACTIVE` + bearish approved direction → `SELL`
- every other Edge class → `NO_TRADE`

## Entry
The fundamental layer does not select a discretionary chart location. In the direct profile:
- BUY permits only the upper M1 Donchian-20 breakout;
- SELL permits only the lower M1 Donchian-20 breakout;
- period = prior 20 completed M1 bars;
- forming bar is excluded.

## Position lifecycle
Permission governs **new entries only**. Once a trade is open, a later permission change does not automatically close it. The established 4 ATR initial stop and candle-by-candle trailing logic remain responsible for exit unless a separately researched emergency-invalidation layer is later validated.

## Comparative research
Preserve any older higher-timeframe-location profile as a separate benchmark; do not silently delete it. The direct profile is the current deployment profile.
