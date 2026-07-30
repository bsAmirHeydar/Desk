---
title: "Inflation, Labor, Income and Demand — State Vector and Driver Architecture"
type: release-standard
status: canonical
version: 7.0.0
release: "Release 03"
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, release-standard, release-03]
---

# Inflation, Labor, Income and Demand — State Vector and Driver Architecture

## Purpose

This state vector defines the minimum representation required before the Vault can answer a current or historical question in this release. Each component must be timestamped, assigned a horizon, linked to evidence and separated into level, momentum, surprise and uncertainty.

## State axes

- **inflation source and breadth:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **persistence and mean reversion:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **wages, productivity and unit labor cost:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **labor demand and supply:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **income distribution and purchasing power:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **expectations and credibility:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **housing and services:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **policy reaction function:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.

## Topic coverage

- [[Inflation Measurement CPI PCE and Deflators]]
- [[Inflation Decomposition and Price-Setting Channels]]
- [[Shelter Housing and Rent Inflation]]
- [[Wages Productivity and Unit Labor Costs]]
- [[Labor Demand Vacancies Hiring and Separations]]
- [[Labor Supply Participation Demographics and Migration]]
- [[Unemployment Slack and Matching Efficiency]]
- [[Household Income Distribution and Consumption Capacity]]
- [[Inflation Expectations and Credibility]]
- [[Inflation Persistence Regimes and Disinflation]]
- [[Demand Formation and Distributional Multipliers]]

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
