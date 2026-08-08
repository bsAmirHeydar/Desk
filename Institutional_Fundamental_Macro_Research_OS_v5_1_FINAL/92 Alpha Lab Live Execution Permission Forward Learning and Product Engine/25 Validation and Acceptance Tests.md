---
title: "Validation and Acceptance Tests"
type: qa-standard
status: canonical-operational
version: 15.1.0
---
# Validation and Acceptance Tests

A production run fails if any of these fail:
- six markets freshly adjudicated;
- V11/V12/V13 authority preserved;
- consumption not inferred mechanically from time/price distance;
- remaining pressure independent of consumption;
- narrative dominance separate from validity;
- core Edge candidate explicitly separated from final Edge;
- no final `EDGE_ACTIVE` before V15.1 clearance;
- Timing cannot upgrade weak core state;
- every Active has `valid_until` and sufficient safe window;
- every Conditional exposes failed stage and exact blocker;
- future event distinguished between constraint/HOLD/VETO using adaptive hazard logic;
- source calendars current enough for material clocks;
- tentative/TBD/revised schedules preserved honestly;
- exact product/series/reference-market mapping where material;
- no generic OpEx/expiry assumptions;
- dependency graph prevents same-root clock double counting;
- no technical price analysis used by Timing;
- no unsourced directional sign from session/month-end/expiry/calendar label;
- scheduler/TTL/latency feasibility respected;
- expired/stale permission fail-closed;
- forward learning uses matured horizons and hindsight firewall;
- timing control-arm statistics maintained once sufficient sample exists.

See [[93 Temporal Market Structure Timing and Calendar Intelligence Engine/56 Institutional Adversarial QA Failure Modes]].
