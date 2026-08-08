---
title: "Validation Architecture — Forward First and Mechanical Backtest"
type: validation-policy
status: canonical-operational
version: 14.1.0
---
# Validation Architecture — Forward First

## Full live brain
The complete fundamental/narrative/attention/flow state should not be declared validated merely because a reconstructed historical backtest performs well or poorly when key historical evidence cannot be reproduced with high fidelity. Historical reconstruction remains useful research, but it is secondary evidence when contemporaneous narrative, attention, positioning or flow data are missing.

## Primary evidence
Use immutable forward states actually produced before outcomes were known. Compare:

```text
CONTROL: raw Donchian-20 M1 execution
vs
ALPHA: EDGE_ACTIVE permission + Donchian-20 M1 execution
```

Measure trade frequency, expectancy, profit factor, median/average R, drawdown, MFE/MAE, false permissions, missed opportunities, Edge-class performance, market/regime performance and permission coverage.

## Mechanical execution
Donchian-20 M1 + 4 ATR + candle trail remains directly backtestable with high mechanical reproducibility when price/cost data are reliable.

## Historical reconstruction
If used, enforce strict point-in-time first-release/vintage evidence and grade reconstruction quality. Missing live/proprietary signals must be unavailable/confidence-capped, never fabricated.
