---
title: "Legacy Read Mapping and Fail-Closed Rules"
type: migration-contract
status: shadow-development
---
# Legacy Read Mapping and Fail-Closed Rules

P01 reads the closed V1 artifact vocabulary but writes only the V2 shadow semantic contract.

## Legal V1 read paths

- `fundamental_state.v11_fundamental_state.horizon_states[active_horizon].direction`
- `...force_range`
- `fundamental_state.v11_fundamental_state.force.aggregate_value`
- `...force.aggregate_range`
- `...force.aggregate_provenance`
- `...consumption_v2.summary_state`
- `...remaining_pressure_v2.aggregate_class`
- `...remaining_pressure_v2.aggregate_range`
- `...persistence_v2.*`
- active-horizon `persistence_class`, `reversal_risk`, `next_update_trigger`
- `consumption_state.lifecycle_state`
- `consumption_state.remaining_asymmetry`
- `research_intent.remaining_asymmetry`
- `research_intent.review_trigger`
- `research_intent.invalidation_triggers`
- `driver_transition.state/current_driver/strongest_challenger`

## Fail-closed cases

- missing `fundamental_state`;
- malformed V11 envelope;
- no exact active-horizon row;
- missing active-horizon direction/force range/persistence/reversal;
- missing Module 89 Remaining Pressure aggregate;
- any attempt to use a forbidden fallback.

A fail-closed normalized object may still preserve non-authoritative diagnostics, but it cannot claim complete semantic lifecycle integrity.
