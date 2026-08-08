---
title: "Scheduled Event Veto versus Expiry Constraint"
type: canonical-operational-methodology
status: canonical
version: 15.1.0
---
# Scheduled Event Veto versus Expiry Constraint

## Canonical decision rule
The **existence** of a later scheduled event is never sufficient by itself to veto a currently qualified core Edge. V15.1 must apply adaptive event-reset severity and the execution time-budget test.

- If safe time is sufficient → `CLEAR_WITH_CONSTRAINTS`, expire before pre-hazard boundary.
- If time budget is marginal or mechanism unresolved → `HOLD`.
- If no safe new-entry window remains or event discovery/reset is already active → `VETO` / `EVENT_OR_FRAGMENTED`.

The claim that any particular buffer or event rule improves P&L remains subject to forward validation. No fixed NFP/CPI/FOMC T-minus threshold is canonical without evidence.
