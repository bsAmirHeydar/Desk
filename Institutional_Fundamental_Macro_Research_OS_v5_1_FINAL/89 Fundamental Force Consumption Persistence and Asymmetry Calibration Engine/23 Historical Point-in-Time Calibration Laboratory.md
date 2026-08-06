---
title: "Historical Point-in-Time Calibration Laboratory"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Historical Point-in-Time Calibration Laboratory

## Decision purpose

Provide the data contract required to test whether force, consumption and remaining-pressure states predict defined future outcomes without lookahead.

## Governing distinctions

- State construction and outcome labelling are separate.
- Consensus vintage and instrument state belong in features.
- Missing archives lower coverage; they are not imputed with later knowledge.
- Causal quality and payoff prediction are scored separately.

## Operating method

1. Define immutable state rows and cutoff.
2. Recover first-release data, consensus vintage and contemporaneous market state.
3. Predeclare labels and horizons.
4. Split by time with purging and embargo.
5. Report coverage, missingness, regimes and data-tier dependence.

## Required outputs

- `point_in_time_dataset`
- `feature_vintage`
- `label_contract`
- `coverage_matrix`
- `missingness_report`
- `calibration_dataset_version`

## Failure modes and controls

- **Failure:** Later revision enters feature table  
  **Control:** Store revision chain separately and use only available vintage.
- **Failure:** Outcome adjudicates earlier causal model  
  **Control:** Keep ex-post audit distinct.
- **Failure:** Sparse proprietary sample generalized broadly  
  **Control:** Report incremental value and coverage limits.

## Dataset grain

A valid row is an immutable `(asset, horizon, cutoff, methodology_version)` state with contemporaneous expectation, source vintage, instrument/contract state and available evidence. Outcomes live in a separate table joined only after state freeze.

## Label families

- direction continuation over a predeclared horizon;
- expansion beyond a predeclared normalized threshold;
- state survival without invalidation;
- repricing completion within tolerance;
- remaining-pressure realization;
- reversal after exhaustion or over-consumption;
- reinforcement/reopening;
- fundamental-to-flow transition.

The lab must not tune a state definition after seeing its outcome window.

## Canonical dependencies

- [[69 Historical Point-in-Time Case Laboratory/00 Historical Point-in-Time Case Laboratory MOC]]
- [[72 Historical Research Permission and Alpha Validation Laboratory/00 Historical Research Permission and Alpha Validation Laboratory MOC]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
