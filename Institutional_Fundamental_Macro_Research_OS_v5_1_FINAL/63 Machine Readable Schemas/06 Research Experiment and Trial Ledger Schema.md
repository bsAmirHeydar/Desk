---
title: "06 Research Experiment and Trial Ledger Schema"
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
# 06 Research Experiment and Trial Ledger Schema

```yaml
schema_version: 5.0.0
experiment_id: string
parent_hypothesis_id: string
created_at: datetime
researcher: string
status: [proposed, exploratory, frozen, validation, rejected, approved, retired]
data_snapshot_id: string
feature_set_version: string
model_specification: object
hyperparameters: object
train_period: object
validation_period: object
test_period: object
cost_assumptions: object
capacity_assumptions: object
primary_metric: string
secondary_metrics: [string]
results: object
multiple_testing_family: string
decision: string
reviewer: string
artifacts: [string]
hashes: [string]
```

All failed, abandoned, and modified trials remain in the ledger. A new look at the test set requires a new test set or explicit governance exception.
