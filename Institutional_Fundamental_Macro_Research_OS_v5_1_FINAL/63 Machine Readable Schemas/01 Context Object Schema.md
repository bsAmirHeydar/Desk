---
title: "01 Context Object Schema"
type: schema
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - schema
  - machine-readable
  - research-governance
---
# 01 Context Object Schema

## YAML schema example

```yaml
schema_version: 5.0.0
context_id: string
as_of: datetime
information_cutoff: datetime
asset: string
horizons:
  structural: {state: string, probability: number, expiry: datetime}
  cyclical: {state: string, probability: number, transition_probability: number}
  tactical: {priced_gap: number, catalysts: [string]}
  swing: {impulse: string, expected_half_life: string}
  daily: {permission: enum}
  event: {surprise_vector: object}
  microstructure: {liquidity_state: string}
priced_baseline: object
desk_distribution: object
scenarios:
  - {name: string, probability: number, path: [string], signposts: [string], payoff: object}
causal_leader: string
confirmations: [string]
contradictions: [string]
permission: {enum: [LONG_ONLY, SHORT_ONLY, TWO_WAY_REDUCED, NO_TRADE]}
confidence: {type: number, minimum: 0, maximum: 1}
size_ceiling: number
fundamental_invalidation: [string]
technical_handoff: object
expiry: datetime
source_claim_ids: [string]
model_versions: [string]
```

## Validation invariants

Scenario probabilities sum to one within tolerance; no source timestamp exceeds the cutoff; permission cannot be directional without an invalidation; confidence above a governance threshold requires independent confirmation; every model ID resolves to a model card.
