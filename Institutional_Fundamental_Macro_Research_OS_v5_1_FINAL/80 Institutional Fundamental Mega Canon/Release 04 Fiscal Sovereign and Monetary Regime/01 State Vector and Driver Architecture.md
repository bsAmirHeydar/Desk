---
title: "Fiscal, Sovereign and Monetary Regime — State Vector and Driver Architecture"
type: release-standard
status: canonical
version: 7.0.0
release: "Release 04"
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, release-standard, release-04]
---

# Fiscal, Sovereign and Monetary Regime — State Vector and Driver Architecture

## Purpose

This state vector defines the minimum representation required before the Vault can answer a current or historical question in this release. Each component must be timestamped, assigned a horizon, linked to evidence and separated into level, momentum, surprise and uncertainty.

## State axes

- **fiscal impulse and composition:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **debt arithmetic and maturity:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **monetary reaction function:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **reserve and balance-sheet regime:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **financial-condition transmission:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **credibility and institutional constraints:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **fiscal-monetary interaction:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **distributional and external effects:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.

## Topic coverage

- [[Fiscal Impulse Structural Balance and Demand Impact]]
- [[Government Spending Taxes and Fiscal Multipliers]]
- [[Sovereign Debt Arithmetic and Sustainability]]
- [[Fiscal Dominance and Monetary-Fiscal Interaction]]
- [[Central-Bank Reaction Functions]]
- [[Policy Instruments Conventional and Unconventional]]
- [[QE QT Reserves and Balance-Sheet Regimes]]
- [[Financial Conditions and Monetary Transmission]]
- [[Credibility Time Consistency and Policy Error]]
- [[Fiscal-Monetary Regime Classification]]
- [[Sovereign Issuance and Private-Sector Absorption]]

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
