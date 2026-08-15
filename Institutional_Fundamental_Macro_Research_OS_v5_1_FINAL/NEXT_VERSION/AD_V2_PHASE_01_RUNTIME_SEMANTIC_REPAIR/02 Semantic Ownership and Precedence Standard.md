---
title: "Semantic Ownership and Precedence Standard"
type: canonical-development-standard
status: shadow-development
---
# Semantic Ownership and Precedence Standard

## Fundamental lifecycle ownership

At the active strategy horizon, Module 89 `fundamental_state` is the legal scientific source for:

- Fundamental Direction;
- Fundamental Force raw aggregate/range;
- Fundamental Consumption lifecycle;
- Remaining Fundamental Pressure;
- Persistence class and survival metadata;
- active-horizon Reversal Risk;
- pressure/fundamental update triggers.

## Separate cognitive objects

Module 103 objects remain separate:

- `consumption_state.lifecycle_state` = cognitive/transmission consumption lifecycle;
- `consumption_state.remaining_asymmetry` = cognitive Remaining Asymmetry;
- `driver_transition.state` = identity/leadership transition of the dominant driver;
- `research_intent.remaining_asymmetry` = final research-intent asymmetry summary;
- `research_intent.review_trigger` = decision-review trigger;
- `research_intent.invalidation_triggers` = decision-level invalidation predicates.

They may inform later reasoning but may not impersonate Module 89 Force/Remaining Pressure/Persistence.

## Active-horizon rule

Horizon-specific fields must be selected by exact match to `active_horizon`. Structural or shorter-horizon rows may never silently substitute for a missing active-horizon row.

If the active horizon is absent: `FAIL_CLOSED`.

## Force-class rule

V11 carries an ordinal force aggregate and horizon `force_range`, while its JSON schema does not provide a canonical force-band threshold map. P01 therefore preserves raw Force ranges and values and **does not invent a HIGH/MEDIUM/LOW class**. P02 may introduce a versioned Pressure classification contract.

## No generic fallback rule

Forbidden examples:

- `driver_transition.state -> force`
- `remaining_asymmetry -> remaining_pressure`
- `elapsed price move -> consumption`
- `review_trigger -> persistence`
- `price direction -> fundamental direction`

Missing authoritative input remains explicit.
