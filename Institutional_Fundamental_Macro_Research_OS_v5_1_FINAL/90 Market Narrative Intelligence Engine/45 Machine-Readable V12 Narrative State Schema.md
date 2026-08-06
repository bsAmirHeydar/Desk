---
title: "Machine-Readable V12 Narrative State Schema"
type: canonical-method
status: canonical
version: 12.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v12, market-narrative, daily-intelligence]
---
# Machine-Readable V12 Narrative State Schema

The authoritative JSON Schema is stored at `90 Market Narrative Intelligence Engine/v12_market_intelligence_state.schema.json`.

## Top-level objects

- `methodology` freezes version, timestamps, cutoff and scoring mode.
- `inherited_v11_state` preserves force, fact persistence, consumption, remaining pressure, reversal risk and asymmetry.
- `fact_universe` stores facts, clusters and ignored facts.
- `attention` stores asset/horizon maps and evidence.
- `narratives` stores candidates, dominance states, challengers, dormant narratives and transition watch.
- `leaders` separates causal, attention, price, flow and media leadership.
- `reflexivity` stores active loops and break conditions.
- `daily_state` stores the executive market map, watchlist and update triggers.
- `provenance` stores field-level evidence, unavailable inputs and confidence caps.
- `validation` records point-in-time, no-lookahead, V11 regression and V12 validation status.

Null means unknown only when accompanied by a reason. Use `UNAVAILABLE` when the input cannot be observed and `UNDETERMINED` when available evidence does not discriminate among states.
