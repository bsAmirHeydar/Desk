---
title: "EDGE_ACTIVE Definition and Validity Window"
type: canonical-operational-standard
status: canonical
version: 15.1.0
---
# EDGE_ACTIVE Definition and Validity Window

`EDGE_ACTIVE` is now a **two-key state**.

## Key A — Core asymmetry
V11/V12/V13 must independently establish an `ACTIVE_CANDIDATE_BULL` or `ACTIVE_CANDIDATE_BEAR` with coherent execution-horizon direction, active causal driver, intact transmission, adequate independent confirmation, meaningful remaining pressure, acceptable consumption/reversal risk and explicit invalidation.

## Key B — Temporal clearance
V15.1 must return `CLEAR` or `CLEAR_WITH_CONSTRAINTS`, with no hard timing blocker and a sufficient safe execution window.

If either key fails, the state is not Active.

## Validity
Every Active state carries `valid_from` and `valid_until`. `valid_until` is the earliest of:
- core thesis/narrative/data expiry;
- V15.1 hard hazard boundary;
- required review boundary when review cannot occur sooner;
- permission staleness/TTL constraint.

A later scheduled event may shorten validity without preventing Active status now.

## What Active does not mean
No certainty, no guaranteed win rate, no all-day validity, no permission to ignore later events, and no technical-chart confirmation requirement. Entry remains the external M1 Donchian execution profile.
