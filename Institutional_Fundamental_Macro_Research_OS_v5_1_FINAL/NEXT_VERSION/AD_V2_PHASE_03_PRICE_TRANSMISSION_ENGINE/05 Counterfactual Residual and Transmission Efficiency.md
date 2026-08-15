---
title: "Counterfactual Residual and Transmission Efficiency"
type: scientific-contract
status: shadow-development
---
# Counterfactual Residual

When a defensible expected magnitude range exists, P03 computes the pressure-aligned residual:

`actual_aligned_response - expected_aligned_response_range`

Because the expectation is a range, the residual is also a range.

Example:

- Pressure: BUY
- Expected aligned response: +0.30% to +0.70%
- Actual response: -0.40%

Residual interval:

`-1.10% to -0.70%`

This is a large below-expectation residual and triggers model-disagreement diagnostics. It does **not** weaken P02 Pressure automatically.

## Transmission Efficiency

When expected and actual responses use the same defensible unit and expected midpoint is non-zero, P03 may report:

`relative_response_ratio = actual_aligned_response / expected_midpoint`

The ratio is a diagnostic measure, not a probability, not expected return and not a trade score.

Versioned ordinal classes:

- `NEGATIVE`
- `VERY_LOW`
- `LOW`
- `EXPECTED`
- `HIGH`
- `OVER`
- `UNAVAILABLE`

## Counterfactual discipline

An expert range is allowed when data are sparse, but provenance remains `JUDGMENTAL`. An `EMPIRICAL` expected range requires a validation reference. False empirical labeling is a hard failure.
