---
title: "Repricing Completion and Counterfactual Baselines"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Repricing Completion and Counterfactual Baselines

## Decision purpose

Estimate how much economically justified expectation-path or valuation adjustment has occurred, using an explicit counterfactual range rather than raw price distance.

## Governing distinctions

- Counterfactual repricing is a range, not known fair value.
- Observed movement must be decomposed into fundamental, flow and liquidity components.
- Completion is asset-, regime- and horizon-specific.
- Overshoot is possible and separate from thesis invalidation.

## Operating method

1. Choose a counterfactual method appropriate to the catalyst.
2. Record required inputs and point-in-time availability.
3. Estimate expected repricing range and uncertainty.
4. Attribute observed repricing to relevant channels.
5. Report completion range, model risk and alternative estimates.

## Required outputs

- `counterfactual_method`
- `expected_repricing_range`
- `observed_causal_repricing`
- `repricing_completion_range`
- `overshoot_state`
- `model_risk`

## Failure modes and controls

- **Failure:** Using total price move as numerator  
  **Control:** Remove unrelated flow, liquidity and rival-model components where identifiable.
- **Failure:** Single historical average used across regimes  
  **Control:** Condition or widen the range.
- **Failure:** Precision despite missing expectation curve  
  **Control:** Return `UNDETERMINED` or a broad judgmental band.

## Counterfactual repricing methods

| Method | Best use | Primary risk |
|---|---|---|
| Event-conditioned historical distribution | repeated scheduled releases | regime instability |
| Regime-conditioned local projection | dynamic multihorizon response | sample/specification risk |
| Policy-path decomposition | central-bank and macro releases | curve mapping and term-premium contamination |
| Earnings/cash-flow valuation bridge | company/index earnings | discount-rate and terminal-value assumptions |
| Duration or convexity bridge | rate-sensitive assets | nonlinear and cross-factor response |
| Physical-balance elasticity | commodities and gold channels | poor inventory/elasticity observability |
| Options-implied distribution shift | event distributions | risk-neutral versus physical probability |
| Matched historical controls | complex events | imperfect matching and selection bias |
| Expert range | sparse unique events | judgmental anchoring |

No method produces a universal fair move. The output is an uncertainty range conditional on assumptions and horizon.

## Completion ratio

When a defensible counterfactual range exists, repricing completion may be reported as a range. The numerator is relevant, causally linked repricing—not total price movement. The denominator is the expected repricing range under the declared method. Values above 100 indicate possible overshoot, not automatic reversal.

## Canonical dependencies

- [[68 Mathematical Econometric and Market Model Monographs/11 Event Studies Surprise Vectors and Multi-Horizon Price Response]]
- [[72 Historical Research Permission and Alpha Validation Laboratory/07 Multi-Horizon Event Response and Half-Life Estimation]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
