---
title: "Temporal Unknowns, TBD and Schedule Revision Handling"
type: canonical-methodology
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, unknowns, revisions]
---
# Temporal Unknowns, TBD and Schedule Revision Handling

## Schedule states
Every material calendar item is one of: `CONFIRMED`, `TENTATIVE`, `TBD_TIME`, `REVISED`, `CANCELLED`, `UNSCHEDULED`.

## TBD
If an official source confirms the date but not the time, do not insert a habitual or previous-cycle release time. Use a date-level hazard and shorten confidence/validity according to materiality.

## Tentative schedules
Treasury issuance schedules, special exchange sessions and corporate-event times can change. A tentative schedule is useful for horizon planning but must be refreshed before it becomes a hard intraday blocker.

## Revision
Store both previous and current schedule observations with `retrieved_at`. In live mode use the latest authoritative schedule. In historical point-in-time review use only the schedule version known at that historical cutoff.

## Unscheduled shocks
Timing records detection time, not an invented event timestamp before the public information existed. Unscheduled events are handled as new information-state transitions, not retroactively scheduled clocks.
