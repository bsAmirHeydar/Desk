---
title: "27 Temporal Veto Validity Window and Edge Integration"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Temporal Veto, Validity Window and Edge Integration

Timing outputs one action: `NO_CHANGE`, `SHORTEN_VALIDITY`, `EARLY_REVIEW`, `VETO_NEW_ENTRY`, `TEMPORAL_FORCE_OVERLAY`, or `FRAGMENTED`.

A true veto requires material evidence of insufficient exploitable time, imminent binary reset inside the execution horizon, liquidity impairment, settlement/expiry dominance, unresolved clock conflict or critical timing-data failure.

A future high-impact event may simply set `valid_until` before its risk window. Event existence alone is not a veto.

For timing-caused `EDGE_CONDITIONAL`, `Why Not Active?` must name the exact clock, mechanism, transition time, veto/constraint class, upgrade condition, downgrade condition and next review.

Timing changes govern new entries only; open trades remain under mechanical exit unless a separately validated emergency protocol exists.
