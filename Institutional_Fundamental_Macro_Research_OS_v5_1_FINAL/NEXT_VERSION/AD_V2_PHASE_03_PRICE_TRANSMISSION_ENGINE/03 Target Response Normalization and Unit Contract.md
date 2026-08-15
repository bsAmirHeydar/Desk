---
title: "Target Response Normalization and Unit Contract"
type: scientific-contract
status: shadow-development
---
# Target Response Normalization

P03 converts raw target response into **Pressure-aligned response**.

For BUY Pressure:

`aligned_response = observed_target_response`

For SELL Pressure:

`aligned_response = -observed_target_response`

Therefore:

- positive aligned response means price moved with Pressure;
- negative aligned response means price moved against Pressure;
- near-zero response means Pressure has not materially transmitted within the observed window.

## Unit integrity

Expected and actual target response must use the same declared unit, for example:

- `PCT_RETURN`;
- `LOG_RETURN`;
- `BPS_PRICE_RETURN`;
- a predeclared standardized response unit with an explicit transform reference.

P03 does not silently convert ATR, dollars, percentages, volatility units or R-multiples into one another.

A unit mismatch is `FAIL_CLOSED`.

## Price distance is not causal proof

Large opposite movement is diagnostic evidence of transmission disagreement. It is not proof of liquidation, accumulation, absorption or a hidden institutional actor.
