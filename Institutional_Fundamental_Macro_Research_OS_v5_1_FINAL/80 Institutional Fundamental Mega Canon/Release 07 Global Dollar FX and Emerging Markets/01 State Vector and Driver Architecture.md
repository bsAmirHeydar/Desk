---
title: "Global Dollar, FX and Emerging Markets — State Vector and Driver Architecture"
type: release-standard
status: canonical
version: 7.0.0
release: "Release 07"
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, release-standard, release-07]
---

# Global Dollar, FX and Emerging Markets — State Vector and Driver Architecture

## Purpose

This state vector defines the minimum representation required before the Vault can answer a current or historical question in this release. Each component must be timestamped, assigned a horizon, linked to evidence and separated into level, momentum, surprise and uncertainty.

## State axes

- **relative policy and growth:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **external balance and funding:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **hedging demand and basis:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **reserve and intervention capacity:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **valuation and carry:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **global risk appetite:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **commodity terms of trade:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **political and institutional credibility:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.

## Topic coverage

- [[Global Dollar System and Offshore Credit]]
- [[Cross-Currency Basis and CIP Deviations]]
- [[Balance of Payments and External Adjustment]]
- [[International Investment Position and Currency Mismatch]]
- [[Capital Flows and Flow-Price Feedback]]
- [[FX Valuation Purchasing Power and Equilibrium]]
- [[Carry Value Momentum and Regime Interaction]]
- [[Central-Bank Intervention and Reserve Management]]
- [[Emerging-Market Local Rates and Currency Risk]]
- [[Currency Crisis and Sudden-Stop Mechanics]]
- [[Commodity Currencies and Terms of Trade]]
- [[Dollar Regimes and Global Financial Cycle]]
- [[Stablecoins and Digital Dollar Channels]]

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
