---
title: "Country Books and Historical Regime Atlas — State Vector and Driver Architecture"
type: release-standard
status: canonical
version: 7.0.0
release: "Release 12"
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, release-standard, release-12]
---

# Country Books and Historical Regime Atlas — State Vector and Driver Architecture

## Purpose

This state vector defines the minimum representation required before the Vault can answer a current or historical question in this release. Each component must be timestamped, assigned a horizon, linked to evidence and separated into level, momentum, surprise and uncertainty.

## State axes

- **growth and inflation structure:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **fiscal and monetary institutions:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **bank and household balance sheets:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **external position and currency:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **housing and credit:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **market microstructure:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **political economy:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **historical regime:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.

## Topic coverage

- [[United States Country System]]
- [[Euro Area Monetary Union System]]
- [[United Kingdom Country System]]
- [[Japan Country System]]
- [[China Country System]]
- [[Canada Country System]]
- [[Australia and New Zealand Systems]]
- [[Switzerland Country System]]
- [[India Country System]]
- [[Brazil and Mexico Systems]]
- [[Emerging Asia Technology Export Systems]]
- [[Turkey and South Africa Vulnerability Systems]]
- [[Commodity Exporter Sovereign Systems]]
- [[Historical Regime Atlas and Analogue Method]]
- [[Historical Crisis Reconstruction Protocol]]

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
