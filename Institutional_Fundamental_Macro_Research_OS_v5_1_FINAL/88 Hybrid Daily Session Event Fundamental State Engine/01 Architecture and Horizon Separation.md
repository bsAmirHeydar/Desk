---
title: "Architecture and Horizon Separation"
type: canonical-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [multihorizon, state-engine, point-in-time]
---
# Architecture and Horizon Separation

## Governing hierarchy

Maintain separate immutable state objects:

1. `STRUCTURAL_PRIOR`
2. `CYCLICAL_REGIME`
3. `TACTICAL_STATE`
4. `MULTI_DAY_2_10D_STATE`
5. `DAILY_INHERITED_STATE`
6. `OVERNIGHT_CHANGE`
7. `SESSION_STATE`
8. `EVENT_STATE`
9. `EVENT_REACTION_STATE`
10. `STATE_DECAY`
11. `END_OF_DAY_ATTRIBUTION`

A lower-horizon update does not rewrite the higher-horizon record. It may change the conditional interpretation, confidence, transmission or usable edge for the lower horizon. A higher-horizon prior may constrain but cannot veto evidence of an intraday reversal.

## Attention allocation

For day-horizon work:

- 50–65%: current session, releases, policy pricing, rates, FX, credit, volatility, earnings, physical information, flow and liquidity;
- 20–30%: daily inherited and 2–10-day states;
- 10–20%: cyclical and structural constraints.

Exceed the structural allocation only for regime breaks, systemic events or evidence that directly changes long-horizon state.

## State inheritance

Every daily baseline must identify:

- prior-session end state;
- unresolved drivers and contradictions;
- information already absorbed;
- unfinished repricing;
- active multi-day bridge;
- known next catalysts;
- expiry conditions.

Inheritance is explicit. Never recreate the prior from the later day's outcome.

## Conflict matrix

| Higher horizon | Intraday evidence | Required treatment |
|---|---|---|
| bullish | negative and independently confirmed | retain bullish higher prior; issue negative session state and raise reversal/bridge risk |
| bearish | positive but flow-only | retain bearish prior; label temporary flow and cap persistence |
| neutral | strong event repricing | allow event/session directional state; wait for multi-day confirmation before upgrading tactical state |
| strong prior | contradictory causal leader | reduce confidence and edge availability; do not average scores mechanically |

## Output discipline

Every record must say which layer changed and which layers did not. A state transition without a named horizon fails the architecture gate.
