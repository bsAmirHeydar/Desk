---
title: "Temporal Clearance, Veto, Validity Window and Edge Interaction"
type: canonical-methodology
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, clearance-gate, edge, institutional]
---
# Temporal Clearance, Veto, Validity Window and Edge Interaction

This note is the canonical bridge between Module 93 and Module 92.

## Two-stage Edge architecture
Module 92 first constructs a `CORE_EDGE_CANDIDATE` from V11/V12/V13 evidence. Module 93 then determines temporal clearance. **Final `EDGE_ACTIVE` does not exist until both stages pass.**

## Gate states
### `CLEAR`
No material temporal blocker exists inside the expected exploit window. Timing does not improve the thesis; it merely certifies temporal usability.

### `CLEAR_WITH_CONSTRAINTS`
The Edge is usable now, but a known transition imposes a hard expiry/review boundary. Final Edge may still be Active, with `valid_until` set before the hazard boundary.

### `HOLD`
The core thesis may be valid, but timing does not currently certify a new entry. Use for marginal time budget, unresolved handoff/collision, pending material event discovery, or a material clock whose mechanism is not sufficiently resolved. Final Edge becomes `EDGE_CONDITIONAL`.

### `VETO`
A hard temporal condition makes new entry unusable now: market/venue closure; no safe exploit window before a known reset; product-specific expiry/final-settlement mechanics that dominate the expression; settlement/funding obstruction; material schedule uncertainty that cannot be bounded; or operational TTL/review failure. Permission is `NO_TRADE`.

### `UNDETERMINED_MATERIAL`
A material clock cannot be resolved with acceptable evidence. Do not guess. Final state is `INSUFFICIENT_EVIDENCE` or `EDGE_CONDITIONAL` depending on whether the missing timing evidence is essential to current usability.

### `CLOSED`
Relevant execution/reference market is closed or unavailable for the intended expression. Permission is `NO_TRADE`.

## Timing cannot upgrade weak core science
`CLEAR` cannot turn `BIAS_ONLY`, `NO_EDGE`, `EDGE_RELATIVE` or insufficient fundamental/narrative evidence into `EDGE_ACTIVE`. Timing is a necessary gate, not an independent source of directional edge.

## Veto hierarchy
Veto is deliberately narrow. Before `VETO`, test in order:
1. Can the clock be treated as non-decisive?
2. Can it be handled by `EARLY_REVIEW`?
3. Can it be handled by `CLEAR_WITH_CONSTRAINTS` and shorter `valid_until`?
4. Is `HOLD` sufficient?
5. Only then use `VETO` when new-entry usability is genuinely absent.

## Event rule
A future high-impact event is **not** a veto by existence. It becomes a hard blocker only when the pre-hazard safe window is too short for the execution profile, when the event is already in its information-discovery/hazard phase, or when product/calendar mechanics make the expression unsafe. Otherwise it sets `valid_until` and next review.

## Output requirement
Every non-CLEAR result must state the exact clock, mechanism, source, time boundary, hard/soft status, required evidence to clear, `valid_until`, and next review. Every `EDGE_CONDITIONAL` must expose this in `Why Not Active?`.
