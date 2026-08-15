---
title: "Target Price Exclusion and Adversarial Invariants"
type: quality-standard
status: shadow-development
---
# Target Price Exclusion and Adversarial Invariants

## PRICE_CONTAMINATION_ATTACK

Hold all causal evidence fixed. Change only target price from strongly positive to strongly negative.

Required result:

- Directional Pressure sign unchanged;
- magnitude range unchanged;
- class unchanged;
- trend/acceleration unchanged;
- consumption unchanged;
- remaining causal pressure unchanged.

Any pressure mutation is a **HARD FAIL**.

## Forbidden pressure sources

- `TARGET_PRICE`
- `TARGET_PRICE_RETURN`
- `TARGET_TECHNICAL_MOMENTUM`
- `TARGET_BREAKOUT`
- `TARGET_SUPPORT_RESISTANCE`
- `TARGET_CANDLE_PATTERN`
- `TRADE_OUTCOME`

## Cross-asset nuance

`CROSS_ASSET_CAUSAL_STATE` is allowed only with an explicit mechanism. Therefore DXY, nominal/real yields, credit or commodity inputs may participate when causally justified; they are not automatically independent roots.

## Anti-storytelling

P02 has no field called liquidity grab, absorption, accumulation or release. The engine cannot infer them because this phase does not yet own transmission or market-microstructure latent states.
