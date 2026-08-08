---
title: "Regime-Conditional Interpretation and Structural Breaks"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Regime-Conditional Interpretation and Structural Breaks

## Decision purpose

Condition score interpretation and empirical mappings on macro, volatility, liquidity, policy, positioning and market-structure regimes, with structural-break controls.

## Governing distinctions

- The same surprise can transmit differently across regimes.
- Regime labels are uncertain and may overlap.
- A historical mapping can fail abruptly.
- Regime selection must be point-in-time.

## Operating method

1. Define candidate regime dimensions before viewing outcomes.
2. Use observable point-in-time indicators and a band when uncertain.
3. Estimate or select regime-specific mappings.
4. Test stability, breakpoints and out-of-regime degradation.
5. Retire or widen models when drift exceeds limits.

## Required outputs

- `regime_vector`
- `regime_confidence`
- `mapping_version`
- `break_indicator`
- `out_of_regime_flag`
- `drift_action`

## Failure modes and controls

- **Failure:** Final regime label backfilled into history  
  **Control:** Use contemporaneous indicators.
- **Failure:** One regime taxonomy controls all assets  
  **Control:** Allow asset-specific regime dimensions.
- **Failure:** Old calibration used after structural break  
  **Control:** Trigger retirement or uncertainty expansion.

## Canonical dependencies

- [[27 Macro Regime Ontology and State Machines/00 27 Macro Regime Ontology and State Machines MOC]]
- [[68 Mathematical Econometric and Market Model Monographs/06 Local Projections State Dependence and Nonlinear Responses]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.

## V21 regime-conditioned graph
V21 upgrades regime use from a label attached to an analysis into an input to the dynamic causal graph. Multiple regime dimensions may coexist. When regime mapping is uncertain or breaking, the system expands the scenario tree and reduces reliance on fixed historical mappings rather than forcing one sign.
