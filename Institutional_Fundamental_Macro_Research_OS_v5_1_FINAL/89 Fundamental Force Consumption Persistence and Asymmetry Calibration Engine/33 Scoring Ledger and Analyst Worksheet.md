---
title: "Scoring Ledger and Analyst Worksheet"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Scoring Ledger and Analyst Worksheet

## Decision purpose

Provide a reproducible sequence for producing an auditable V11 state without hiding judgment inside a summary score.

## Governing distinctions

- Evidence selection precedes scoring.
- Applicability precedes weighting.
- Contradiction is not negative confirmation.
- Missing evidence reduces confidence, not necessarily direction.
- Summary values must be reconstructable from component ledgers.

## Operating method

1. Freeze cutoff, asset, horizon and information set.
2. List candidate state changes and pre-catalyst expectations.
3. Select applicable force and consumption components.
4. Enter evidence, source, timestamp, provenance, direction and strength band for each component.
5. Enter rival models and discriminator evidence.
6. Apply observability confidence caps.
7. Estimate counterfactual repricing range and consumption state.
8. Decompose remaining pressure, persistence and reversal risk.
9. Complete the execution handoff and validator checklist.

## Required outputs

- `analysis_header`
- `force_component_ledger`
- `expectation_revision_ledger`
- `consumption_component_ledger`
- `remaining_pressure_ledger`
- `persistence_ledger`
- `rival_model_ledger`
- `confidence_cap_ledger`
- `handoff`

## Failure modes and controls

- **Failure:** Scoring before freezing evidence  
  **Control:** Lock cutoff and sources first.
- **Failure:** Changing weights after seeing price outcome  
  **Control:** Version weights before outcome window.
- **Failure:** Hiding disagreement  
  **Control:** Store analyst-specific records and adjudication.
- **Failure:** Using an average over non-applicable fields  
  **Control:** Exclude explicitly.

## Worksheet rule

A summary field is optional when aggregation would create false precision. Component ledgers and a qualitative class are sufficient. When an aggregate is supplied, the worksheet must disclose weighting method, missing-field treatment and whether the value is ordinal or calibrated.

## Canonical dependencies

- [[21 Score Provenance Intervals and False-Precision Control]]
- [[22 Analyst Reproducibility and Adjudication Protocol]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
