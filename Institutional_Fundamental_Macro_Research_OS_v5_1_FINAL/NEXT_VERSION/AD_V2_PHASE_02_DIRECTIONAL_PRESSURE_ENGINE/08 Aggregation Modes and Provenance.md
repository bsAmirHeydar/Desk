---
title: "P02 Aggregation Modes and Provenance"
type: runtime-contract
status: shadow-development
---
# Aggregation Modes

P02 has two modes.

## Mode A — `LEGACY_MODULE89_WRAP`

Purpose: backward-compatible bridge from closed V1 science.

Authority inputs:

- Module 89 exact-horizon Direction through P01;
- Module 89 exact-horizon Force range through P01;
- Module 89 Fundamental Consumption, Remaining Pressure and Persistence through P01.

This mode does not recompute the V1 Force ledger. It signs and classifies it under the V2 Pressure vocabulary.

## Mode B — `EXPLICIT_ROOT_LEDGER`

Purpose: V2 shadow research.

Independent roots carry disclosed analytical weights. Dependent signals are nested and non-additive. Applicable unavailable roots widen the interval rather than being deleted.

The aggregation is a disclosed weighted ordinal interval, not a probability and not an arithmetic truth claim.

## Root interval rule

- BUY root: positive interval.
- SELL root: negative interval.
- NEUTRAL root: zero interval.
- unknown/unavailable applicable root: full negative-to-positive uncertainty interval.

After `NOT_APPLICABLE` roots are removed, the remaining declared weights are normalized to one.

## Provenance

Every root and aggregate records mode, horizon, cutoff, source kind, locator, mechanism, confidence and freshness.
