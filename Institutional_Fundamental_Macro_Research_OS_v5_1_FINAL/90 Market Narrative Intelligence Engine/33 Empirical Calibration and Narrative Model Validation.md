---
title: "Empirical Calibration and Narrative Model Validation"
type: canonical-method
status: canonical
version: 12.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v12, market-narrative, daily-intelligence]
---
# Empirical Calibration and Narrative Model Validation

## Validation targets

Separate candidate-generation recall, attention ranking, dominance classification, validity assessment, transition timing, state survival and asset-response usefulness.

Use purged walk-forward evaluation, embargo, regime splits, event-family splits, horizon/asset splits, calibration curves only for probability outputs, ablation, drift monitoring and naive baselines.

## Labels

Define labels before observing outcomes. Price continuation does not label narrative validity. Human-adjudicated labels need frozen evidence packets and inter-rater reporting.

## Model retirement

Retire mappings that fail after structural breaks, depend on unavailable data, show unstable calibration or add no value beyond a simple baseline. V12 remains fully usable in ordinal mode when empirical calibration is absent.
