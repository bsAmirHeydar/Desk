---
title: "Remaining Fundamental Pressure Decomposition"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Remaining Fundamental Pressure Decomposition

## Decision purpose

Estimate how much directionally usable force remains after part of the catalyst is processed and after opposing forces, valuation, event risk and uncertainty are considered.

## Governing distinctions

- Remaining pressure is not the complement of consumption.
- Structural carry and event impulse are separate.
- High force can have low remaining pressure after mature repricing.
- Low price response can coexist with high pressure during event waiting or impaired liquidity.

## Operating method

1. Start with force vector and expectation gap.
2. Subtract completed repricing and identified exhaustion, not arbitrary time.
3. Add persistent processes and unfinished transmission.
4. Subtract opposing force, payoff compression, event and reversal hazards.
5. Report range/class plus dominant positive and negative contributors.

## Required outputs

- `remaining_pressure_components`
- `aggregate_range`
- `aggregate_class`
- `dominant_residual_driver`
- `dominant_opposing_force`
- `evidence_uncertainty`

## Failure modes and controls

- **Failure:** Calculated as 100 minus consumption  
  **Control:** Use the residual component ledger.
- **Failure:** Structural and tactical forces netted invisibly  
  **Control:** Report separate horizon components.
- **Failure:** High unknowns produce a precise aggregate  
  **Control:** Widen the range and lower confidence.

## Residual decomposition

```text
Remaining pressure
= residual active-catalyst force
+ unresolved expectations gap
+ unfinished transmission
+ structural/cyclical carry
+ institutional constraint tail
+ persistent economic/physical process
+ mechanical-flow continuation
+ confirmed reinforcement
- opposing-force load
- valuation/payoff compression
- next-catalyst hazard
- reversal hazard
± evidence uncertainty
```

This is an analytical decomposition, not a universal linear formula. Components may interact nonlinearly and be reported as ranges or classes.

A high state requires more than low consumption: an unresolved causal gap, credible transmission capacity, persistence, manageable opposing forces and no hidden binary hazard. A low state can coexist with strong direction after mature repricing.

## Canonical dependencies

- [[87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/15 Hourly Direction Intensity Consumption and Remaining Pressure Standard]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/07 Direction Usability and Edge Availability]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
