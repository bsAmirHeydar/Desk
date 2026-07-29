---
title: "14 Model Card Standard"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [model-card, validation, governance]
---
# 14 Model Card Standard

## Model identity

A model card must contain model ID, owner, purpose, target, horizon, code commit, environment lock, data snapshot, feature set, estimation window, hyperparameters, dependencies and approval status.

## Scientific specification

Document:

- mathematical formulation;
- identification or predictive objective;
- variable definitions and transformations;
- missing-data handling;
- regularization and priors;
- estimation algorithm;
- uncertainty calculation;
- benchmark models;
- sensitivity and ablation tests;
- computational complexity and latency.

## Validation

Report:

- pseudo-real-time design;
- out-of-sample results;
- calibration;
- regime and subgroup stability;
- revision and vintage sensitivity;
- leakage checks;
- cost and capacity stress;
- failure examples;
- challenger-model comparison.

## Operational controls

- deployment environment;
- data-quality dependencies;
- monitoring metrics;
- drift thresholds;
- fallback behavior;
- kill switch;
- access and change controls;
- review frequency;
- retirement conditions.

## Prohibited claims

A model card may not describe a model as robust, causal, calibrated, production-ready or institution-grade unless the corresponding test results are attached.
