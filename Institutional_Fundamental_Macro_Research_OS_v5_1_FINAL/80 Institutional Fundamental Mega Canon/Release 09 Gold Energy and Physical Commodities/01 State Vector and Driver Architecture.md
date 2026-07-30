---
title: "Gold, Energy and Physical Commodities — State Vector and Driver Architecture"
type: release-standard
status: canonical
version: 7.0.0
release: "Release 09"
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, release-standard, release-09]
---

# Gold, Energy and Physical Commodities — State Vector and Driver Architecture

## Purpose

This state vector defines the minimum representation required before the Vault can answer a current or historical question in this release. Each component must be timestamped, assigned a horizon, linked to evidence and separated into level, momentum, surprise and uncertainty.

## State axes

- **physical balance:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **inventory and spare capacity:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **curve and convenience yield:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **location and quality basis:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **logistics and storage:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **policy and geopolitics:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **financial flows:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **currency and real rates:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.

## Topic coverage

- [[Gold Monetary and Physical Demand System]]
- [[Silver Dual Monetary and Industrial Demand]]
- [[Central-Bank Reserve Demand and Gold Allocation]]
- [[Gold ETF Futures and Physical Market Linkage]]
- [[Global Oil Balance and Barrel Accounting]]
- [[Refining Product Markets and Crack Spreads]]
- [[Oil Inventories Storage and Curve Structure]]
- [[OPEC Spare Capacity and Supply Policy]]
- [[Natural Gas LNG and Regional Balances]]
- [[Power Markets Capacity and Fuel Switching]]
- [[Copper Industrial Metals and China Demand]]
- [[Agriculture Weather and Balance Sheets]]
- [[Shipping Freight and Trade Bottlenecks]]
- [[Carbon Critical Minerals and Transition Constraints]]

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
