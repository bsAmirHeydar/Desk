---
title: "Adaptive Hazard Window and Event Reset Severity"
type: canonical-methodology
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, events, hazard-window]
---
# Adaptive Hazard Window and Event Reset Severity

## Problem with fixed windows
Fixed rules such as `T-60 = no trade` are not institutional timing science. Different events, assets, regimes, expression vehicles and execution profiles have different reset risks. V15.1 keeps T-240/T-120/T-60/... only as **research sampling anchors**, never as automatic veto thresholds.

## Event reset severity
Classify from non-price facts:
- `LOW`: routine information with limited potential to reset the active causal distribution;
- `MODERATE`: relevant event that may alter one driver but usually does not invalidate the full state;
- `HIGH`: material event capable of changing policy/rates/growth/earnings/flow assumptions;
- `BINARY_RESET`: event whose outcome can rapidly replace the active driver/narrative distribution;
- `UNKNOWN_MATERIAL`: timing/terms/outcome structure insufficiently resolved.

## Adaptive pre-hazard boundary
The pre-hazard buffer is a function of:
1. reset severity;
2. target asset sensitivity and core driver linkage;
3. whether the event is first release/revision/communication stage;
4. whether multiple clocks collide;
5. reference/execution market state and settlement obligations;
6. empirical or qualitative time-to-exploit requirement;
7. operational latency and next-review feasibility.

## Post-event state
Elapsed minutes alone do not prove assimilation. Timing identifies stages: `RELEASE`, `INITIAL_DISCOVERY`, `SECONDARY_COMMUNICATION`, `ASSIMILATION_WINDOW`, `POST_EVENT_NORMALIZATION`. Fundamental/Narrative modules decide whether the new information is actually understood and persistent; Timing does not read a chart to declare assimilation.

## Event as constraint vs veto
If sufficient safe time remains before `PRE_HAZARD`, return `CLEAR_WITH_CONSTRAINTS`. If safe time is marginal, return `HOLD`. Use `VETO` only once the intended new-entry horizon is not safely exploitable or the event reset is already active.
