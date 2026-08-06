---
title: "Cross-Asset Confirmation and Causal-Leader Adjudication"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Cross-Asset Confirmation and Causal-Leader Adjudication

## Decision purpose

Adjudicate which market or state variable leads the repricing and whether cross-asset evidence independently supports, lags or contradicts the winning model.

## Governing distinctions

- Sequence plus mechanism is stronger than correlation.
- Leader identity can change.
- A common latent driver can create false multiplicity.
- Confirmation failure can reduce edge without flipping direction.

## Operating method

1. List model-implied lead and follow variables.
2. Timestamp changes at comparable cutoffs.
3. Cluster overlapping evidence and score independence.
4. Compare winning and rival-model predictions.
5. Record leader changes, breaks and confidence effects.

## Required outputs

- `causal_leader`
- `leader_evidence`
- `independence_weight`
- `cross_asset_state`
- `confirmation_break`
- `rival_discriminator`

## Failure modes and controls

- **Failure:** Most volatile asset called leader  
  **Control:** Use timing and causal mechanism.
- **Failure:** DXY and EURUSD double counted  
  **Control:** Apply mechanical-overlap rule.
- **Failure:** No confirmation treated as contradiction  
  **Control:** Separate absent, lagging and opposite evidence.

## Canonical dependencies

- [[88 Hybrid Daily Session Event Fundamental State Engine/08 Cross-Asset Confirmation and Causal-Leader Changes]]
- [[49 Cross-Asset Relative Value and Trade Expression/00 49 Cross-Asset Relative Value and Trade Expression MOC]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
