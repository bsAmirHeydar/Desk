---
title: "V2 Shadow Semantic Lifecycle Contract"
type: runtime-contract
status: shadow-development
---
# V2 Shadow Semantic Lifecycle Contract

P01 emits `AlphaDesk_V2_SemanticLifecycle`.

It contains seven separated domains.

## 1. Fundamental Direction
Exact active-horizon Module 89 direction plus source path.

## 2. Fundamental Force
Raw active-horizon force range plus Module 89 aggregate value/range/provenance. P01 does not fabricate a force class.

## 3. Consumption
Two parallel fields:

- `fundamental_consumption` from Module 89 `consumption_v2.summary_state`;
- `cognitive_consumption` from Module 103 `consumption_state.lifecycle_state`.

Neither overwrites the other.

## 4. Remaining Fundamental Pressure
From Module 89 `remaining_pressure_v2.aggregate_class` and `aggregate_range` only.

## 5. Remaining Asymmetry
Stored separately from Research Intent and/or cognitive consumption. It is never a fallback for Remaining Pressure.

## 6. Persistence and Reversal
Active-horizon `persistence_class` and `reversal_risk` are bound to the exact active horizon. Detailed Module 89 survival/half-life metadata is preserved separately.

## 7. Driver Transition / Decision Timing
Driver transition and decision-review triggers are carried in separate namespaces with explicit non-authority declarations.

## Semantic integrity state

Every normalized result includes:

- `substitutions_used` — must always be empty in P01;
- `illegal_substitutions_detected`;
- `missing_authoritative_fields`;
- `status = PASS | FAIL_CLOSED`.

No silent best-effort synthesis is allowed for a load-bearing field.
