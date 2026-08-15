---
title: "Freshness TTL Half-Life and Expiry"
type: scientific-contract
status: shadow-development
---
# Freshness, TTL, Half-Life and Expiry

## Freshness

A causal root may declare a `freshness_ttl_seconds`. P02 derives:

- `FRESH`
- `AGING`
- `STALE`
- `EXPIRED`
- `UNKNOWN`

An expired root is not allowed to preserve its old directional contribution. In explicit-root aggregation it is treated as economically applicable but currently unavailable, widening the pressure interval instead of silently carrying stale force.

## TTL is not half-life

TTL is an evidence-reassessment contract. Half-life describes survival/decay of a causal state.

P02 preserves half-life only with provenance:

- `EMPIRICAL`
- `MODEL_IMPLIED`
- `JUDGMENTAL`
- `UNKNOWN`

An `EMPIRICAL` half-life must include a validation reference. Otherwise the engine fails closed on that claim.

## No price-decay shortcut

A large target-price move is not evidence that a causal root expired or consumed its half-life.
