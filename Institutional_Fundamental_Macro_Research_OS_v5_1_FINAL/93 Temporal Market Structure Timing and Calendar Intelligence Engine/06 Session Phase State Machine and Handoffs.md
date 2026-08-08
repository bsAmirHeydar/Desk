---
title: "Session Phase State Machine and Handoffs"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Session Phase State Machine and Handoffs

A session is decomposed into states rather than a single label.

`PRE_OPEN -> OPEN_DISCOVERY -> POST_OPEN_STABILIZATION -> CONTINUOUS -> MIDDAY/LOWER_PARTICIPATION -> PRE_CLOSE -> CLOSE_AUCTION -> POST_CLOSE -> OVERNIGHT`

FX additionally uses regional handoffs: `ASIA -> LONDON -> LONDON_NY_OVERLAP -> NY -> LATE_NY`.

## Handoff hypothesis
A thesis that survived one participant set has not automatically survived the next. At a handoff, V15 asks whether the next dominant group has the same information, inventory constraints and benchmark obligations. The engine schedules a review around major handoffs when the active Edge depends on participation that may disappear.

## No automatic veto
A session transition is not automatically `NO_TRADE`. It can be:
- `CONTINUITY_EXPECTED`;
- `DISCOVERY_RESET`;
- `LIQUIDITY_DEGRADATION`;
- `MECHANICAL_FLOW_WINDOW`;
- `UNDETERMINED`.

## Validation
Forward learning must compare pre-handoff calls with post-handoff outcomes, controlling for new information. The goal is to learn when handoffs matter for each asset, not to hard-code folklore such as “London always reverses Asia.”
