---
title: "Timing Gate to Final Edge Transition Matrix"
type: canonical-operational-standard
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, edge, state-transition]
---
# Timing Gate to Final Edge Transition Matrix

## Non-negotiable principle
Timing can remove Active status; it cannot create Active status from an unqualified core thesis.

| Core state | Timing gate | Final Edge | Permission |
|---|---|---|---|
| `ACTIVE_CANDIDATE_BULL` | `CLEAR` | `EDGE_ACTIVE` | BUY |
| `ACTIVE_CANDIDATE_BULL` | `CLEAR_WITH_CONSTRAINTS` | `EDGE_ACTIVE` | BUY until valid_until |
| `ACTIVE_CANDIDATE_BEAR` | `CLEAR` | `EDGE_ACTIVE` | SELL |
| `ACTIVE_CANDIDATE_BEAR` | `CLEAR_WITH_CONSTRAINTS` | `EDGE_ACTIVE` | SELL until valid_until |
| any active candidate | `HOLD` | `EDGE_CONDITIONAL` | NO_TRADE |
| any active candidate | `VETO` | `EDGE_CONDITIONAL` or `EVENT_OR_FRAGMENTED` | NO_TRADE |
| any active candidate | `UNDETERMINED_MATERIAL` | `INSUFFICIENT_EVIDENCE` or `EDGE_CONDITIONAL` | NO_TRADE |
| any state | `CLOSED` | preserve thesis label internally; final permission blocked | NO_TRADE |
| `BIAS_ONLY` | any clear state | `BIAS_ONLY` | NO_TRADE |
| `NO_EDGE` | any clear state | `NO_EDGE` | NO_TRADE |
| `EDGE_RELATIVE` | any clear state | `EDGE_RELATIVE` | NO_TRADE single-symbol executor |

## Choosing Conditional vs Event/Fragmented
Use `EVENT_OR_FRAGMENTED` when timing uncertainty is itself a live binary/discovery state or multiple material clocks are unresolved. Use `EDGE_CONDITIONAL` when the thesis remains coherent but timing requires waiting for a known transition/clearance condition.

## Required disclosure
When Timing prevents Active, `Why Not Active?` must name the exact temporal gate state, hard blocker, next clearing event, earliest possible upgrade time, and source.
