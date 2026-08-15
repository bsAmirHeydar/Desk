---
title: "Alpha Desk V2 Phase 02 Directional Pressure Engine 2.0"
type: development-moc
status: shadow-development
phase: "AD-V2-P02"
version: "0.2.0"
baseline: "V1 closed + P00 + P01"
---
# Alpha Desk V2 — Phase 02 Directional Pressure Engine 2.0

## Mission

P02 turns the legally-owned Module 89 lifecycle science exposed by P01 into an explicit **Directional Pressure** object without using the target instrument's own price as pressure evidence.

This is the first V2 phase that adds new scientific state rather than only constitutional or semantic infrastructure.

## What P02 adds

- signed pressure (`BUY`, `SELL`, `BALANCED/CONTESTED`, `UNKNOWN`);
- explicit ordinal pressure classes (`BUY_LOW` ... `BUY_EXTREME`, mirrored for SELL);
- pressure range and precision status;
- pressure trend and acceleration based only on pressure snapshots;
- causal-root ledger and root-independence control;
- driver freshness, TTL, expiry and half-life provenance;
- contradiction load separated from confidence;
- Fundamental Driver Consumption carried separately from price behavior;
- Remaining Causal Pressure carried separately from edge/asymmetry;
- provenance on every root and aggregate;
- target-price contamination attacks;
- a V1-compatible Module 89 wrap mode and a V2 explicit-root shadow aggregation mode.

## What P02 explicitly does not add

P02 does **not** implement:

- Price Transmission state machine;
- Unreleased Pressure;
- Opposing-Move Maturity;
- Release Readiness;
- liquidity-grab or absorption inference;
- Gold-specific probability calibration;
- trade permission authority;
- broker/execution authority.

Those belong to P03+.

## Scientific authority

Direction remains Module 89 Fundamental Direction at the exact active horizon. P02 creates a signed Pressure state from legal causal evidence but remains `SHADOW_ONLY`.

## Core law

`TARGET PRICE IS DOWNSTREAM OF PRESSURE.`

Target price may trigger a later missing-driver investigation, but it may not directly strengthen, weaken, reverse, consume or rescue Pressure.
