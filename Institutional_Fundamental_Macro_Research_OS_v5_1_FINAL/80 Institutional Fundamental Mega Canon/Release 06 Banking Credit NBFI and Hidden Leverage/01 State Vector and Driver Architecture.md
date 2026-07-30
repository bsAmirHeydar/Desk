---
title: "Banking, Credit, NBFI and Hidden Leverage — State Vector and Driver Architecture"
type: release-standard
status: canonical
version: 7.0.0
release: "Release 06"
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, release-standard, release-06]
---

# Banking, Credit, NBFI and Hidden Leverage — State Vector and Driver Architecture

## Purpose

This state vector defines the minimum representation required before the Vault can answer a current or historical question in this release. Each component must be timestamped, assigned a horizon, linked to evidence and separated into level, momentum, surprise and uncertainty.

## State axes

- **bank asset quality:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **deposit and funding stability:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **credit creation and standards:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **default and recovery:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **private-credit opacity:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **nonbank leverage:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **margin and collateral:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **network contagion:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.

## Topic coverage

- [[Bank Balance-Sheet Mechanics]]
- [[Deposits Money Creation and Funding Competition]]
- [[Bank Lending Standards and Credit Supply]]
- [[Credit Cycle and Financial Accelerator]]
- [[Corporate Credit Spreads and Relative Risk]]
- [[Default Recovery and Distress Dynamics]]
- [[Private Credit Structure and Opacity]]
- [[NBFI System and Liquidity Transformation]]
- [[Hidden Leverage and Derivative Exposures]]
- [[Margin Liquidity Spirals and Fire Sales]]
- [[Contagion Networks and Counterparty Risk]]
- [[Commercial Real Estate and Bank Stress]]

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
