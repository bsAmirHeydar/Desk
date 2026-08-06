---
title: "Persistence Half-Life and State Survival"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Persistence Half-Life and State Survival

## Decision purpose

Estimate survival of each thesis component across specified horizons instead of assigning one universal decay clock.

## Governing distinctions

- Different thesis components decay at different rates.
- State survival is conditional on future evidence.
- A half-life can be empirical, model-implied or judgmental; the label is mandatory.
- Persistence can increase after reinforcement.

## Operating method

1. Decompose thesis into persistence components.
2. Select evidence-driven expiry and invalidation conditions.
3. Estimate survival window or hazard only at the supported level.
4. Reassess at event, session and mandatory checkpoints.
5. Store transitions without rewriting earlier estimates.

## Required outputs

- `persistence_components`
- `survival_window`
- `half_life_range`
- `half_life_provenance`
- `expiry_conditions`
- `reassessment_clock`
- `state_survival_confidence`

## Failure modes and controls

- **Failure:** One half-life for the whole thesis  
  **Control:** Use component-specific survival.
- **Failure:** Later survival used to improve prior estimate  
  **Control:** Preserve immutable point-in-time records.
- **Failure:** Judgmental half-life presented as empirical  
  **Control:** Require provenance and validation reference.

## Persistence stack

- **Catalyst persistence:** how long the specific observation remains decision-relevant.
- **Economic-state persistence:** survival of the underlying state.
- **Policy-path persistence:** survival of expected reaction-function change.
- **Earnings-revision persistence:** survival of revision breadth and level.
- **Physical-balance persistence:** duration of scarcity, inventory or official-demand process.
- **Flow persistence:** duration of forced or systematic activity.
- **Narrative persistence:** stability of the dominant interpretation.
- **Repricing persistence:** resistance of the adjustment to reversal.

Half-life is not mandatory. When data do not support a hazard estimate, use a survival window, expiry map and confidence band.

## Canonical dependencies

- [[72 Historical Research Permission and Alpha Validation Laboratory/07 Multi-Horizon Event Response and Half-Life Estimation]]
- [[58 Multi-Day Fundamental Campaigns/01 Swing Campaign Architecture and Thesis Half-Life]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
