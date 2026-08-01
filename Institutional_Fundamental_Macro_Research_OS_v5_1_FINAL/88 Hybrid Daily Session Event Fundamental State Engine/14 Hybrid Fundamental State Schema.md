---
title: "Hybrid Fundamental State Schema"
type: schema-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [schema, state, csv, yaml]
---
# Hybrid Fundamental State Schema

```yaml
hybrid_fundamental_state:
  identity:
    record_id:
    record_type:
    market:
    reference_instrument:
    trading_date:
    event_time_utc:
    event_time_local:
    timezone:
    session:
    session_stage:
    market_status:
  information_boundary:
    analysis_cutoff:
    earliest_verified_source_time:
    timestamp_confidence:
    no_lookahead_status:
    first_release_or_revision:
    data_availability:
  hierarchy:
    structural_prior:
    cyclical_regime:
    tactical_state:
    multi_day_state:
    daily_inherited_state:
    session_state:
    event_state:
  direction:
    direction_code:
    direction_score_before:
    direction_score_after:
    intensity_before:
    intensity_after:
    confidence_before:
    confidence_after:
    probability_type:
  consumption:
    catalyst_freshness_before:
    catalyst_freshness_after:
    information_absorption_before:
    information_absorption_after:
    repricing_completion_before:
    repricing_completion_after:
    flow_exhaustion_before:
    flow_exhaustion_after:
    narrative_saturation_before:
    narrative_saturation_after:
    remaining_pressure_before:
    remaining_pressure_after:
  usability:
    state_phase:
    move_quality:
    persistence_class:
    estimated_half_life:
    reversal_risk_before:
    reversal_risk_after:
    path_asymmetry:
    edge_availability:
  causal_stack:
    dominant_driver:
    secondary_drivers: []
    winning_model:
    rival_model:
    causal_leader:
    causal_leader_changed:
    cross_asset_confirmation_before:
    cross_asset_confirmation_after:
    confirmation_break:
    contradictory_evidence: []
  catalyst:
    event_type:
    event_category:
    event_summary:
    scheduled_or_unscheduled:
    surprise_vector:
    next_catalyst:
    next_update_trigger:
    next_mandatory_update:
  controls:
    mandatory_checkpoint:
    checkpoint_completed:
    missing_window_reason:
    state_decay_basis:
    unavailable_inputs: []
    evidence_ledger: []
    analyst_notes:
```


## Record-type enum

```yaml
record_type:
  - INITIAL_WINDOW_STATE
  - DAILY_BASELINE
  - OVERNIGHT_UPDATE
  - SESSION_HANDOFF
  - PRE_EVENT_BASELINE
  - SCHEDULED_EVENT_T0
  - UNSCHEDULED_EVENT_T0
  - EVENT_T_PLUS_5
  - EVENT_T_PLUS_15
  - EVENT_T_PLUS_30
  - EVENT_T_PLUS_60
  - POST_OPEN_REASSESSMENT
  - MIDDAY_REASSESSMENT
  - AFTERNOON_REASSESSMENT
  - STATE_DECAY_UPDATE
  - CAUSAL_LEADER_CHANGE
  - CONFIRMATION_BREAK
  - FUNDAMENTAL_TO_FLOW_TRANSITION
  - FLOW_TO_FUNDAMENTAL_TRANSITION
  - THESIS_REINFORCEMENT
  - THESIS_EXHAUSTION
  - THESIS_INVALIDATION
  - END_OF_DAY_STATE
  - POST_MARKET_EARNINGS_UPDATE
  - NO_MATERIAL_DIRECTION_CHANGE
```

## CSV minimum columns

Use flattened equivalents of every load-bearing field. Store before/after values; do not overwrite prior state. Include a stable `record_id` and `parent_record_id` for event micro-windows and session chains.
