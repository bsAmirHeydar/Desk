---
title: "Measurement, Reconstruction and Institutional Synthesis — State Vector and Driver Architecture"
type: release-standard
status: canonical
version: 7.0.0
release: "Release 13"
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, release-standard, release-13]
---

# Measurement, Reconstruction and Institutional Synthesis — State Vector and Driver Architecture

## Purpose

This state vector defines the minimum representation required before the Vault can answer a current or historical question in this release. Each component must be timestamped, assigned a horizon, linked to evidence and separated into level, momentum, surprise and uncertainty.

## State axes

- **measurement and vintage:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **state estimation:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **forecast distribution:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **causal identification:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **event response:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **historical reconstruction:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **multihorizon synthesis:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **portfolio exposure:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.

## Topic coverage

- [[Nowcasting Architecture and Ragged Edge]]
- [[State-Space Models and Kalman Filtering]]
- [[Dynamic Factor Models]]
- [[MIDAS Bridge and Mixed-Frequency Regression]]
- [[VAR BVAR and Structural Identification]]
- [[Local Projections and State-Dependent Effects]]
- [[Panel Models Instruments and Natural Experiments]]
- [[Event Studies and Market Response Measurement]]
- [[Density Forecasts Calibration and Scoring]]
- [[Point-in-Time Historical Reconstruction]]
- [[Current Full-Spectrum Analysis Synthesis]]
- [[Day-Horizon Fundamental Context]]
- [[Multi-Day Fundamental Context]]
- [[Scenario Analysis Wargaming and Tail States]]
- [[Portfolio Fundamental Exposure and Hidden Drivers]]

## State object

```yaml
analysis_object:
cutoff:
horizon:
observed_state:
estimated_state:
expectations_baseline:
pricing_gap:
causal_leaders:
mediators:
constraints:
rival_models:
cross_domain_confirmation:
contradictions:
scenario_distribution:
confidence:
invalidation:
expiry:
unknowns:
source_lineage:
```

## Aggregation rule

Do not average unlike signals. Aggregate only after mapping every observation to a causal role: state, expectation, price, flow, constraint, policy response or outcome. Weighting must reflect timeliness, measurement quality, causal proximity, independence and regime relevance.
