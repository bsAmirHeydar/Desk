---
title: "Catalyst Freshness Reinforcement and Reopening"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Catalyst Freshness Reinforcement and Reopening

## Decision purpose

Model freshness as decision relevance, then handle reinforcing, offsetting and reopening information as state transitions rather than resetting a clock mechanically.

## Governing distinctions

- Age is not decay.
- A continuing process can remain active without new headlines.
- A second independent catalyst can reopen capacity.
- Repeated commentary without incremental information does not reinforce the thesis.

## Operating method

1. Identify catalyst family and expiry conditions.
2. Separate time-driven from evidence-driven decay.
3. Classify new observations as duplicate, confirmatory, reinforcing, offsetting or invalidating.
4. Update force and consumption vectors asymmetrically.
5. Record reopened capacity and new horizon.

## Required outputs

- `freshness_state`
- `decay_basis`
- `new_information_class`
- `reinforcement_strength`
- `reopening_state`
- `new_expiry_condition`

## Failure modes and controls

- **Failure:** Daily freshness reduced by fixed points  
  **Control:** Use stated decay evidence and event clocks.
- **Failure:** Duplicate headline counted as reinforcement  
  **Control:** Require independent incremental information.
- **Failure:** Reopening returns all consumption components to zero  
  **Control:** Update only affected dimensions.

## Canonical dependencies

- [[88 Hybrid Daily Session Event Fundamental State Engine/05 State Decay and No-Change Reassessment]]
- [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Information Half-Life, Shock Decay, Persistence and Thesis Expiry]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
