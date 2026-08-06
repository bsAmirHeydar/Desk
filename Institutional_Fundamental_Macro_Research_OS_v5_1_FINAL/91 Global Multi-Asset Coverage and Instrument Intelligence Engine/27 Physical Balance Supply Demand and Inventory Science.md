---
title: "Physical Balance Supply Demand and Inventory Science"
type: canonical-note
status: canonical
version: 13.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v13, universal-multi-asset]
---
# Physical Balance Supply Demand and Inventory Science

## Mission

Operationalize **Physical Balance Supply Demand and Inventory Science** as a reusable V13 component for universal FX, commodity and global-index research.

## Governing doctrine

Commodity analysis is physical-first and contract-specific. Macro price beta cannot replace a balance, deliverability and curve analysis.

## Required state

The analyst must capture contract, month, grade, location, delivery, physical supply-demand, inventories, curves, basis, storage, logistics, weather, costs and policy. Every load-bearing field must include value or band, horizon, timestamp, vintage, provenance, confidence and next-update condition.

## Procedure

1. Resolve the exact instrument and implementation before interpreting any market observation.
2. Freeze UTC, local market time, metadata vintage and source availability.
3. Load Module 89 and Module 90 shared state, then select one primary V13 adapter.
4. Build the specialist evidence ledger and distinguish observed, market-implied, proxy, model-implied and unavailable inputs.
5. Evaluate competing mechanisms and rival narratives rather than forcing one explanation.
6. Produce a range or `UNDETERMINED` state when the evidence does not support a precise value.
7. Define reinforcement, expiry, invalidation and transition triggers.

## Required outputs

- `instrument_identity` and `metadata_vintage`
- `coverage_status` and `confidence_cap`
- `specialist_state_vector`
- `shared_v11_v12_mapping`
- `dominant_driver` and `rival_models`
- `fact_persistence`, `consumption`, and `remaining_pressure`
- `attention`, `narrative_validity`, and `narrative_dominance`
- `invalidation`, `expiry`, and `next_update_trigger`

## Failure modes

- **Generic-market substitution:** never replace specialist evidence with a broad risk-on/risk-off label.
- **Identity error:** never mix cash, future, CFD, ETF, index, grade, delivery point or return series.
- **Lookahead:** never use current constituents, revised releases or later contract knowledge at a historical cutoff.
- **False observability:** public proxies cannot be presented as direct dealer, reserve, inventory or institutional-flow observations.
- **Score conflation:** ordinal 0–100 communication scores are not probabilities.

## Canonical boundary

Module 89 remains authoritative for force, fact persistence, consumption, remaining pressure, reversal risk and fundamental asymmetry. Module 90 remains authoritative for attention, narrative validity, dominance, narrative persistence, reflexivity and transitions. Module 91 governs identity, adapters, metadata and universal reporting.
