---
title: "04 Model Card Schema"
type: schema
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - schema
  - machine-readable
  - research-governance
---
# 04 Model Card Schema

```yaml
schema_version: 5.0.0
model_id: string
version: string
owner: string
purpose: string
target: string
decision_use: [string]
universe: [string]
horizons: [string]
information_cutoff_logic: string
features: [string]
target_construction: string
estimation: string
hyperparameters: object
training_window: object
validation_design: object
benchmarks: [string]
metrics: object
calibration: object
cost_model: object
capacity_assumptions: object
known_failure_modes: [string]
forbidden_uses: [string]
monitoring: object
retraining_policy: object
retirement_triggers: [string]
approvals: [string]
artifact_hashes: [string]
```
