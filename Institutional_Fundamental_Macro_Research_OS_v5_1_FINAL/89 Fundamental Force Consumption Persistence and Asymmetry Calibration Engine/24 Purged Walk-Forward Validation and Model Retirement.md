---
title: "Purged Walk-Forward Validation and Model Retirement"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Purged Walk-Forward Validation and Model Retirement

## Decision purpose

Turn historical calibration into a disciplined model lifecycle rather than a one-time backtest.

## Governing distinctions

- Random train/test splits are unsafe for time series.
- Good discrimination can coexist with poor calibration.
- A profitable implementation does not validate causal attribution.
- Model retirement is part of scientific maturity.

## Operating method

1. Define walk-forward folds and overlapping-label purge.
2. Apply embargo around dependent windows.
3. Benchmark against naive and reduced models.
4. Evaluate calibration, discrimination, coverage and stability.
5. Monitor drift and execute retirement rules.

## Required outputs

- `walk_forward_design`
- `purge_embargo`
- `benchmark_results`
- `calibration_results`
- `stability_results`
- `model_status`
- `retirement_reason`

## Failure modes and controls

- **Failure:** In-sample threshold chosen after outcomes  
  **Control:** Lock threshold before test fold.
- **Failure:** All regimes pooled  
  **Control:** Publish stratified results and interaction risk.
- **Failure:** Only profit factor reported  
  **Control:** Evaluate state, causal, persistence and consumption targets separately.

## Minimum validation report

- walk-forward windows, purge and embargo;
- sample counts by asset, event, regime and horizon;
- calibration curve and Brier/log score when probabilities are claimed;
- discrimination versus naive baselines;
- interval coverage for range forecasts;
- component ablation;
- model stability and drift;
- missing-data sensitivity;
- public-only versus licensed/proprietary incremental value;
- inter-rater sensitivity;
- failure clusters and retirement decision.

A model is retired or downgraded when semantic drift, calibration failure, regime break, data discontinuity or reproducibility failure exceeds predeclared limits.

## Canonical dependencies

- [[53 Research Statistics Forecasting and Causal Inference/00 53 Research Statistics Forecasting and Causal Inference MOC]]
- [[81 Scientific QA and Certification Framework/24 Executed Benchmark Register]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
