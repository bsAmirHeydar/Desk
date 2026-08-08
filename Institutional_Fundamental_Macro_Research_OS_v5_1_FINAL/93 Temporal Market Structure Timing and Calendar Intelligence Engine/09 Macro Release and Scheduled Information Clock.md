---
title: "Macro Release and Scheduled Information Clock"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Macro Release and Scheduled Information Clock

The event clock is a **state machine around information arrival**, not a static economic calendar.

## Event object
For every material release store: official source, scheduled timestamp, timezone, release family, expected consensus source if licensed/available, first-release/revision status, affected causal channels, likely horizon, publication latency risk and rescheduling status.

## Observation grid
Default research checkpoints: `T-240, T-120, T-60, T-30, T-15, T-5, T0, T+5, T+15, T+30, T+60, T+240`. These are review points, not universal trade bans. Adapt them to event importance and market structure.

## Event phases
`PRE_EVENT_NORMAL`, `PRE_EVENT_POSITIONING`, `PRE_EVENT_LIQUIDITY_WITHDRAWAL`, `RELEASE`, `FIRST_REACTION`, `CROSS_ASSET_CONFIRMATION`, `NARRATIVE_SELECTION`, `PERSISTENCE_TEST`, `CONSUMPTION_REASSESSMENT`.

## Official schedules
BLS and BEA schedules are primary sources for US labor/inflation/GDP/PCE events (`SRC-BLS-CALENDAR`, `SRC-BEA-CALENDAR`). The engine must retrieve the current schedule rather than assume a recurring day/time forever.

## Core rule
Proximity alone does not decide Edge. The engine separately determines whether the event is a `VALIDITY_CONSTRAINT`, `TRUE_VETO`, or merely `NEXT_REVIEW_TRIGGER`.
