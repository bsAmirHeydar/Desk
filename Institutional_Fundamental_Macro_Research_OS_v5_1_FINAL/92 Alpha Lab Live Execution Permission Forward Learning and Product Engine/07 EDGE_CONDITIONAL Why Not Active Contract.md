---
title: "EDGE_CONDITIONAL Why Not Active Contract"
type: mandatory-output-contract
status: canonical-operational
version: 14.1.0
---
# EDGE_CONDITIONAL — Why Not Active?

A conditional Edge is never allowed to be a vague label such as “needs confirmation.” The deep report and HTML must include a dedicated `Why Not Active?` block with:

1. why the state is not `EDGE_ACTIVE` now;
2. decisive blockers ranked by importance;
3. non-decisive caution factors separately;
4. exact missing or insufficient evidence;
5. exact upgrade triggers to `EDGE_ACTIVE`;
6. exact downgrade triggers to `BIAS_ONLY`, `NO_EDGE` or `EVENT_OR_FRAGMENTED`;
7. whether each scheduled event is a true veto or only a validity-window constraint;
8. current usable time window and `valid_until` logic;
9. the specific live evidence that would remove each blocker;
10. whether a pre-event directional opportunity may exist but is withheld because evidence quality remains below Active threshold.

Each “confirmation” must name the causal channel, evidence and state transition it would create.


<!-- ALPHALAB_V15_TIMING_BEGIN -->
## Timing-specific Why Not Active?
If Timing is a blocker, name the exact clock, mechanism, transition time, true-veto vs validity-constraint class, missing evidence, upgrade trigger, downgrade trigger and `valid_until`. “Timing is bad” is invalid.
<!-- ALPHALAB_V15_TIMING_END -->

