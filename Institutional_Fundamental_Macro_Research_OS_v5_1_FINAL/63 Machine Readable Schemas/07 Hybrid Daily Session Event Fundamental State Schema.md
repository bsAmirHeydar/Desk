---
title: "07 Hybrid Daily Session Event Fundamental State Schema"
type: schema
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [schema, hybrid-state, point-in-time]
---
# Hybrid Daily Session Event Fundamental State Schema

The canonical state object is defined in [[88 Hybrid Daily Session Event Fundamental State Engine/14 Hybrid Fundamental State Schema]]. Use stable record IDs, parent IDs for micro-windows, before/after scores, mandatory-checkpoint flags and immutable timestamps.

## Required record-type enum

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
