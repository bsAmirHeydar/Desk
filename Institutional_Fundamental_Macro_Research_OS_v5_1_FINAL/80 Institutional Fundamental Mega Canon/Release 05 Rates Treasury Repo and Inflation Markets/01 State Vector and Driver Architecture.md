---
title: "Rates, Treasury, Repo and Inflation Markets — State Vector and Driver Architecture"
type: release-standard
status: canonical
version: 7.0.0
release: "Release 05"
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, release-standard, release-05]
---

# Rates, Treasury, Repo and Inflation Markets — State Vector and Driver Architecture

## Purpose

This state vector defines the minimum representation required before the Vault can answer a current or historical question in this release. Each component must be timestamped, assigned a horizon, linked to evidence and separated into level, momentum, surprise and uncertainty.

## State axes

- **expected policy path:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **term premium:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **inflation compensation:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **real rate:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **net duration supply:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **funding and collateral:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **dealer intermediation:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.
- **convexity and hedging:** record observed state, direction, acceleration, dispersion, historical percentile, expected persistence and confidence.

## Topic coverage

- [[OIS Policy Path and Meeting-Dated Pricing]]
- [[Yield Curve Decomposition and Forward Rates]]
- [[Term Premium Models and Interpretation]]
- [[Real Rates and Inflation Compensation]]
- [[Treasury Refunding Issuance and Duration Supply]]
- [[Treasury Auctions and Demand Quality]]
- [[Repo Collateral and Funding Conditions]]
- [[Swap Spreads and Balance-Sheet Intermediation]]
- [[Treasury Futures CTD and Net Basis]]
- [[Duration Convexity and Key-Rate Risk]]
- [[Mortgage Convexity and Hedging Flows]]
- [[Sovereign Relative Value and Curve Expression]]

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
