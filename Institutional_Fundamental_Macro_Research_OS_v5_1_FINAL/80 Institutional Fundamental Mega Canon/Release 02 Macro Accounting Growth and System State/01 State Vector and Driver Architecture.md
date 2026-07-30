---
title: "Macro Accounting, Growth and System State — State Vector and Driver Architecture"
type: release-standard
status: canonical
version: 7.0.0
release: "Release 02"
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, release-standard, release-02]
---

# Macro Accounting, Growth and System State — State Vector and Driver Architecture

## Purpose

This state vector defines the minimum representation required before the Vault can answer a current or historical question in this release. Each component must be timestamped, assigned a horizon, linked to evidence and separated into level, momentum, surprise and uncertainty.

## State axes

- **real activity level and momentum:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **nominal income and expenditure:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **sectoral saving and borrowing:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **credit-supported versus income-supported demand:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **productivity and potential output:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **inventory and trade contributions:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **housing and construction:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **revision and measurement uncertainty:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.

## Topic coverage

- [[National Accounts and GDP Architecture]]
- [[Sectoral Balances and Financial Positions]]
- [[Flow of Funds and Balance-Sheet Transmission]]
- [[Household Income Consumption and Saving]]
- [[Business Investment and Capital Formation]]
- [[Inventories Trade and Final Demand]]
- [[Productivity Potential Output and Supply Capacity]]
- [[Business-Cycle Regime and Turning Points]]
- [[Housing Residential Investment and Shelter System]]
- [[Supply Chains Inventories and Production Networks]]
- [[Growth Nowcast Interpretation and Revision Risk]]

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
