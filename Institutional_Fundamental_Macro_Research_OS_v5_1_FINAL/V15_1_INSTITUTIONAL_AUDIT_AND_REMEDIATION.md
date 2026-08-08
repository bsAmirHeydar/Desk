---
title: "V15.1 Institutional Audit and Remediation"
type: audit-report
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, audit, remediation]
---
# V15.1 Institutional Audit and Remediation

## Audit conclusion
V15.0 had broad institutional clock coverage, but its main weakness was **decision architecture**: timing could describe and constrain the Edge without a fully explicit independent certification gate. This left room for inconsistent Active classification, over-veto, fixed-window heuristics, clock double-counting, unclear time-to-exploit requirements and operational staleness.

## Remediated weaknesses
1. Added two-stage `CORE_EDGE_CANDIDATE → TEMPORAL_CLEARANCE → FINAL_EDGE` architecture.
2. Made V15.1 clearance mandatory for every final `EDGE_ACTIVE`.
3. Replaced loose actions with six mutually exclusive clearance states.
4. Prohibited Timing from upgrading weak core science.
5. Added adaptive event hazard severity; fixed T-minus times are sampling anchors only.
6. Added safe execution time-budget / time-to-exploit contract.
7. Added cold-start safe-margin logic to prevent universal no-trade starvation.
8. Added dependency graph to prevent SOQ/open/expiry/month-end double counting.
9. Tightened no-technical boundary: real-time price patterns are not needed for Timing clearance.
10. Separated structural participant/liquidity clocks from chart-derived liquidity analysis.
11. Added broker CFD vs reference-market clock mapping.
12. Added source freshness, tentative/TBD/revised schedule states and no-false-precision rules.
13. Added operational latency, TTL, clock drift and scheduler feasibility.
14. Added least-restrictive-correct-action hierarchy to reduce over-veto.
15. Added CORE_ONLY versus TIMING_GATED control arms and starvation metrics.
16. Expanded timing learning/error taxonomy and promotion governance.
17. Expanded benchmark suite to 42 adversarial cases and explicit 32 failure modes.

## Final institutional rule
Fundamental and narrative analysis can create an Active **candidate**. Timing is the independent usability certificate. Only a core Active candidate that receives Timing `CLEAR` or `CLEAR_WITH_CONSTRAINTS` can become product-facing `EDGE_ACTIVE` and therefore BUY/SELL permission.
