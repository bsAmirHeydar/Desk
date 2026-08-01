---
title: "Record Types and Mandatory Coverage"
type: canonical-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [record-types, coverage, intraday]
---
# Record Types and Mandatory Coverage

## Supported record types

- `INITIAL_WINDOW_STATE`
- `DAILY_BASELINE`
- `OVERNIGHT_UPDATE`
- `SESSION_HANDOFF`
- `PRE_EVENT_BASELINE`
- `SCHEDULED_EVENT_T0`
- `UNSCHEDULED_EVENT_T0`
- `EVENT_T_PLUS_5`
- `EVENT_T_PLUS_15`
- `EVENT_T_PLUS_30`
- `EVENT_T_PLUS_60`
- `POST_OPEN_REASSESSMENT`
- `MIDDAY_REASSESSMENT`
- `AFTERNOON_REASSESSMENT`
- `STATE_DECAY_UPDATE`
- `CAUSAL_LEADER_CHANGE`
- `CONFIRMATION_BREAK`
- `FUNDAMENTAL_TO_FLOW_TRANSITION`
- `FLOW_TO_FUNDAMENTAL_TRANSITION`
- `THESIS_REINFORCEMENT`
- `THESIS_EXHAUSTION`
- `THESIS_INVALIDATION`
- `END_OF_DAY_STATE`
- `POST_MARKET_EARNINGS_UPDATE`
- `NO_MATERIAL_DIRECTION_CHANGE`

## Mandatory records on every open trading day

For each market, create at minimum:

1. one `DAILY_BASELINE` before the principal liquid session;
2. one `OVERNIGHT_UPDATE` or documented overnight no-change assessment;
3. required `SESSION_HANDOFF` records;
4. one post-open reassessment;
5. one midday reassessment;
6. one afternoon reassessment;
7. one `END_OF_DAY_STATE`;
8. event and micro-window records for every material catalyst.

A mandatory reassessment may use `NO_MATERIAL_DIRECTION_CHANGE`. It must still update subordinate state variables and explain why direction did not change.

## No-change record

Use `NO_MATERIAL_DIRECTION_CHANGE` when the directional label and score remain materially stable but another practical dimension changes. Required fields include before/after intensity, freshness, absorption, repricing completion, flow exhaustion, remaining pressure, confirmation, persistence, reversal risk and edge availability.

Example:

```yaml
record_type: NO_MATERIAL_DIRECTION_CHANGE
direction: BULLISH
direction_score_before: 55
direction_score_after: 55
intensity_before: 70
intensity_after: 55
catalyst_freshness_before: 85
catalyst_freshness_after: 60
repricing_completion_before: 35
repricing_completion_after: 60
remaining_pressure_before: 75
remaining_pressure_after: 45
reversal_risk_before: 25
reversal_risk_after: 45
reason: "No new negative information, but the catalyst was increasingly absorbed and independent confirmation weakened."
```

## Closed-market and holiday treatment

Do not invent session records for closed venues. Record market status in the next baseline and carry only admissible global information that could affect the next open. Weekend events receive unscheduled-event records with the exact publication clock and a conditional transmission state until a relevant market opens.
