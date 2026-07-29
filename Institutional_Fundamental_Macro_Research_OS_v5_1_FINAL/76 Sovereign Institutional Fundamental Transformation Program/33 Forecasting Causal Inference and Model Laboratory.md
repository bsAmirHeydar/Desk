---
title: "33 Forecasting Causal Inference and Model Laboratory"
type: program-phase
status: planned
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-transformation]
---
# 33 Forecasting Causal Inference and Model Laboratory

## Mission

Implement models as tested software packages with benchmarks, uncertainty, reproducibility and retirement rules.

## Why this phase exists

This phase closes a specific gap between a large knowledge base and a production institutional capability. Work is not complete when prose exists; it is complete when the required artifacts can be independently reproduced, tested and governed.

## Dependencies

Phase 05, Phase 08, Phase 09, Phase 10

## Build scope

- State-space, factor, MIDAS, VAR, local-projection, panel and regime packages.
- Model registry and experiment tracking.
- Simulation and synthetic recovery tests.

## Required artifacts

- architecture decision record;
- source and data contracts;
- implementation specification;
- test plan and expected failure cases;
- reproducible evidence package;
- ownership, review and retirement record;
- change log linked to claim and model IDs.

## Acceptance gates

- Code, environment and data snapshots reproduce published results.
- Models beat appropriate baselines or are retired.
- Causal and predictive claims are labeled correctly.


## Red-team questions

- Which claim could still be true for the wrong reason?
- Which missing dataset or institutional constraint could reverse the conclusion?
- What simple benchmark would make this phase unnecessary?
- How could revised data, survivorship, timestamp error or selection bias create a false success?
- What operational failure would make a valid research result unusable?

## Exit condition

The phase closes only after artifacts, tests and approvals are attached. Narrative completion, file count and word count do not close the phase.
