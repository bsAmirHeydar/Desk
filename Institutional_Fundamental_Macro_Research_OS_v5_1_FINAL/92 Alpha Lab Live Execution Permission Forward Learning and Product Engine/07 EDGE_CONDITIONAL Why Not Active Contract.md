---
title: "EDGE_CONDITIONAL Why Not Active Contract"
type: mandatory-output-contract
status: canonical-operational
version: 15.1.0
---
# EDGE_CONDITIONAL — Why Not Active?

Every Conditional state must identify **which gate failed**.

## Required fields
1. `failed_stage`: `CORE`, `TIMING`, or `BOTH`;
2. why it is not Active now;
3. decisive blockers ranked by importance;
4. caution factors separately;
5. exact missing/insufficient evidence;
6. exact upgrade condition into a core Active Candidate and/or Timing CLEAR;
7. downgrade triggers;
8. if Timing blocks: exact clock, root mechanism, source, gate state, hard vs soft blocker, next clearing transition, safe-window status, and `valid_until` logic;
9. whether the future event is only a validity constraint or a current HOLD/VETO;
10. earliest plausible re-evaluation time.

“Needs confirmation” and “timing is bad” are invalid without the exact evidence object and state transition required.
