---
title: "Edge Taxonomy and Qualification"
type: canonical-operational-standard
status: canonical
version: 15.1.0
---
# Edge Taxonomy and Qualification

## Product-facing classes
1. `EDGE_ACTIVE` — directly usable directional asymmetry **after both core qualification and temporal clearance**.
2. `EDGE_CONDITIONAL` — useful asymmetry exists but a core or timing blocker prevents immediate Active status.
3. `EDGE_RELATIVE` — relative-value edge; single-symbol executor receives NO_TRADE.
4. `BIAS_ONLY` — defensible direction without sufficient operational asymmetry.
5. `NO_EDGE` — no clean usable directional opportunity.
6. `EVENT_OR_FRAGMENTED` — live binary/discovery/contradictory state where forcing direction is inappropriate.
7. `INSUFFICIENT_EVIDENCE` — evidence/data quality inadequate.

## Stage 1 — Core Edge candidate
V11/V12/V13 create one internal state:
- `ACTIVE_CANDIDATE_BULL`;
- `ACTIVE_CANDIDATE_BEAR`;
- `CONDITIONAL_CANDIDATE`;
- `RELATIVE_CANDIDATE`;
- `BIAS_ONLY`;
- `NO_EDGE`;
- `FRAGMENTED`;
- `INSUFFICIENT_EVIDENCE`.

This stage uses direction, active-driver activation, transmission integrity, independent confirmation, remaining pressure, consumption, persistence, narrative state, reversal hazard, horizon conflict, evidence quality and invalidation clarity. It does **not** grant BUY/SELL permission.

## Stage 2 — V15.1 temporal clearance
Only `ACTIVE_CANDIDATE_BULL/BEAR` may proceed to the Temporal Clearance Gate. `CLEAR` or `CLEAR_WITH_CONSTRAINTS` is required for final `EDGE_ACTIVE`.

Timing can downgrade/hold/expire a core candidate; Timing cannot upgrade `BIAS_ONLY`, `NO_EDGE`, `EDGE_RELATIVE` or insufficient core evidence to Active.

Do not use a mechanical weighted score as a substitute for causal adjudication unless separately validated.
