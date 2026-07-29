---
title: "04 Reproducible Research Package"
type: institutional-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-reference]
---

# 04 Reproducible Research Package

A research package contains immutable references to data snapshots, code commits, dependency locks, configuration, random seeds, model artifacts, logs, tables and narrative conclusions.

## Directory contract

```text
research_package/
  manifest.json
  data_contracts/
  source_hashes/
  code/
  environment/
  configs/
  tests/
  outputs/
  figures/
  claim_matrix/
  model_cards/
  decision_records/
  review/
```

The manifest identifies which artifacts are redistributable and which require licensed regeneration. Reproduction must not depend on an analyst's local spreadsheet, browser cache or undocumented manual edit.
