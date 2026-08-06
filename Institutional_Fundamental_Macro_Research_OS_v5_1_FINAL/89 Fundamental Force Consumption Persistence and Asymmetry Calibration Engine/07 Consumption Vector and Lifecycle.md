---
title: "Consumption Vector and Lifecycle"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Consumption Vector and Lifecycle

## Decision purpose

Turn consumption into a lifecycle of informational, expectation, market, positioning and narrative processes. The vector shows which part of propagation is complete and which remains open.

## Governing distinctions

- Awareness can be high while repricing is incomplete.
- Target-instrument repricing can lead cross-asset transmission.
- Narrative saturation is not economic-state completion.
- Reinforcement can reduce net consumption and reopen capacity.
- Consumption is horizon-specific.

## Operating method

1. Freeze catalyst identity and pre-catalyst expectation.
2. Score each applicable consumption dimension independently.
3. Record direct evidence, proxy and unknown components.
4. Select a lifecycle state from the full vector.
5. Compare with the prior record using reason-coded transitions.

## Required outputs

- `consumption_vector`
- `consumption_lifecycle_state`
- `transition_reason_codes`
- `reopening_state`
- `unresolved_overhang`
- `summary_label`

## Failure modes and controls

- **Failure:** Consumption set equal to elapsed time  
  **Control:** Use evidence-driven component updates.
- **Failure:** Large price move set to 100  
  **Control:** Compare with expectation-path and counterfactual repricing.
- **Failure:** All components averaged despite unknown data  
  **Control:** Retain unknowns and cap aggregate confidence.

## V11 consumption vector

```yaml
information_awareness: 0-100 | band | unknown
expectation_incorporation: 0-100 | band | unknown
instrument_repricing_completion: 0-100 | range | unknown
cross_asset_transmission_completion: 0-100 | range | unknown
positioning_adjustment_completion: 0-100 | band | unknown
mechanical_flow_exhaustion: 0-100 | band | unknown
narrative_saturation: 0-100 | band | unknown
valuation_payoff_compression: 0-100 | band | unknown
time_decay: 0-100 | band | unknown
catalyst_expiry: ACTIVE | CONDITIONAL | EXPIRED | INVALIDATED
reinforcement_or_reopening: NONE | POSSIBLE | CONFIRMED | FAILED
unresolved_information_overhang: LOW | MEDIUM | HIGH | UNKNOWN
```

## Lifecycle

`UNOBSERVED_OR_UNKNOWN → AWARENESS_FORMING → PARTIALLY_ABSORBED → EXPECTATIONS_REPRICING → CROSS_ASSET_TRANSMISSION → FLOW_PROPAGATION → MATURE_REPRICING → MOSTLY_CONSUMED → EXHAUSTED`

Alternative transitions include `REINFORCED_AND_REOPENED`, `OVER_CONSUMED` and `REVERSED_OR_INVALIDATED`. Each transition requires a reason code and evidence timestamp.

## Canonical dependencies

- [[87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/15 Hourly Direction Intensity Consumption and Remaining Pressure Standard]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/05 State Decay and No-Change Reassessment]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
