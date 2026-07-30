---
title: "Cross-Asset, Geopolitics and Structural Systems — State Vector and Driver Architecture"
type: release-standard
status: canonical
version: 7.0.0
release: "Release 11"
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, release-standard, release-11]
---

# Cross-Asset, Geopolitics and Structural Systems — State Vector and Driver Architecture

## Purpose

This state vector defines the minimum representation required before the Vault can answer a current or historical question in this release. Each component must be timestamped, assigned a horizon, linked to evidence and separated into level, momentum, surprise and uncertainty.

## State axes

- **discount-rate transmission:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **cash-flow and growth transmission:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **funding and collateral:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **risk premium and volatility:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **trade and supply-chain disruption:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **resource and energy security:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **demographic and productivity trend:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **institutional credibility:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.

## Topic coverage

- [[Cross-Asset Transmission Matrix]]
- [[Relative Value and Common-Driver Decomposition]]
- [[Global Financial Cycle and Risk Appetite]]
- [[Geopolitical Shock Taxonomy]]
- [[Sanctions Economic Warfare and Financial Channels]]
- [[Tariffs Trade Policy and Supply-Chain Reallocation]]
- [[Energy Security and Strategic Reserves]]
- [[Climate Physical Risk and Transition Policy]]
- [[Demographics Migration and Dependency]]
- [[Institutions Political Economy and Credibility]]
- [[Technology AI Productivity and Capital Cycle]]
- [[Supply-Chain Resilience and Strategic Materials]]
- [[Tail Systems and Nonlinear Regime Change]]

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
