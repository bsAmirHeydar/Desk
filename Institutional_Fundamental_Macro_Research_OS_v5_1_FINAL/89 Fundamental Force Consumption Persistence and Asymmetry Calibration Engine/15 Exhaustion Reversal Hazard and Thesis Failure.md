---
title: "Exhaustion Reversal Hazard and Thesis Failure"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Exhaustion Reversal Hazard and Thesis Failure

## Decision purpose

Separate exhaustion, reversal hazard and thesis failure. Exhaustion means a propagation mechanism is depleted; reversal hazard measures vulnerability; thesis failure means the causal state itself is invalidated.

## Governing distinctions

- Exhaustion need not reverse price.
- Reversal can occur without thesis failure through flow/liquidity.
- Thesis failure can occur before price reversal.
- Over-consumption raises vulnerability but is not a timing signal.

## Operating method

1. Score thesis evidence and rival-model takeover separately.
2. Assess repricing completion, valuation, crowding and flow exhaustion.
3. Map binary event and liquidity-gap hazards.
4. Identify confirmation breaks and policy-reaction risk.
5. State explicit invalidation evidence and reversal triggers.

## Required outputs

- `thesis_status`
- `exhaustion_state`
- `reversal_hazard_components`
- `reversal_risk_range`
- `rival_model_takeover`
- `invalidation_trigger`

## Failure modes and controls

- **Failure:** Any pullback called fundamental reversal  
  **Control:** Separate price path from state evidence.
- **Failure:** High consumption equals immediate reversal  
  **Control:** Require a trigger or opposing force.
- **Failure:** Rival model omitted after confirmation break  
  **Control:** Reopen adjudication and lower confidence.

## Canonical dependencies

- [[88 Hybrid Daily Session Event Fundamental State Engine/07 Direction Usability and Edge Availability]]
- [[81 Scientific QA and Certification Framework/08 Causal Identification Rival Models and Reflexivity Gate]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
