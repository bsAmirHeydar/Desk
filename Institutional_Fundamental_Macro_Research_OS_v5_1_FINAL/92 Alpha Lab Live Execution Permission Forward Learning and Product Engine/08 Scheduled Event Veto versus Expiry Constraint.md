---
title: "Scheduled Event Veto versus Expiry Constraint"
type: provisional-methodology-candidate
status: CANDIDATE
version: 14.1.0
---
# Scheduled Event Veto versus Expiry Constraint

> [!warning] Candidate, not canonical science
> This rule was generated from live pre-NFP review and has not yet passed enough independent forward cases for canonical promotion.

A high-impact event several hours ahead must not automatically downgrade an otherwise tradable state from `EDGE_ACTIVE` to `EDGE_CONDITIONAL`.

## EVENT_AS_EXPIRY_CONSTRAINT
The present edge may remain Active, but `valid_until` must expire safely before the event-risk window and a fresh review must occur before expiry.

## EVENT_AS_VETO
Use only when event proximity is already causing one or more of:
- material fragmentation;
- unstable price control;
- transmission failure;
- liquidity deterioration;
- unfavorable path asymmetry;
- an execution window too short to justify a new trade.

## Validation
Track `OVER_VETO`, `UNDER_VETO`, pre-event continuation quality, state stability and whether the chosen expiry would have protected the system before the event reset across independent NFP/CPI/FOMC and cross-asset cases.
