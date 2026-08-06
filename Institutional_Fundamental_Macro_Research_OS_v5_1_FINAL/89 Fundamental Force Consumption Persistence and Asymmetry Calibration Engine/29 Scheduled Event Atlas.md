---
title: "Scheduled Event Atlas"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Scheduled Event Atlas

## Decision purpose

Standardize how recurring releases, central-bank decisions, auctions and earnings are frozen, interpreted, rescored and expired without forcing dissimilar events into one response template.

## Governing distinctions

- Release surprise differs from economic materiality.
- First release differs from revision.
- Policy communication is a path distribution, not one headline.
- Event consumption may complete in one market before another.
- The next scheduled catalyst can cap current edge.

## Operating method

1. Create a pre-event frozen record with consensus vintage and expectation distribution.
2. Specify event-family components and asset transmission map.
3. Record T-60, T-15, T0, T+5, T+15, T+30 and T+60 where data exist.
4. Separate initial surprise recognition from later causal adjudication.
5. Update consumption and remaining pressure even when direction does not change.
6. Publish expiry, next-event risk and unresolved evidence.

## Required outputs

- `event_family`
- `consensus_vintage`
- `release_vintage`
- `surprise_vector`
- `event_force`
- `micro_window_states`
- `consumption_transition`
- `remaining_pressure_transition`
- `expiry`

## Failure modes and controls

- **Failure:** Using revised data in the frozen event record  
  **Control:** Bind first-release vintage.
- **Failure:** Using one timestamp for embargoed and public release  
  **Control:** Store earliest lawful availability.
- **Failure:** Treating the first price move as causal proof  
  **Control:** Require driver discrimination.
- **Failure:** Omitting no-change records  
  **Control:** Persist reassessment even without direction change.

## Event-family minimums

- Inflation: headline/core, breadth, housing/services/goods, revisions, policy-path consequence.
- Labor: payrolls, unemployment, participation, wages, hours, revisions and composition.
- Growth/activity: level, composition, inventories, prices and leading implications.
- Central banks: decision, statement, projections, press conference, balance-sheet and reaction function.
- Treasury auctions: tail, bid composition, dealer take, curve and term-premium transmission.
- Earnings: headline, quality, guidance, revisions, margins, capex and index weight.

Each family receives its own applicability map; non-applicable components must be `NOT_APPLICABLE`, never zero.

## Canonical dependencies

- [[23 Historical Point-in-Time Calibration Laboratory]]
- [[17 Horizon-Specific State Vectors]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
