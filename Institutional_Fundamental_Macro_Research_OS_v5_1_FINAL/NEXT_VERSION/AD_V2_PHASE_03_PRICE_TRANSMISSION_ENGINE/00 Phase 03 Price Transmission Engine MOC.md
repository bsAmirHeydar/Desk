---
title: "Alpha Desk V2 Phase 03 Price Transmission Engine"
type: development-moc
status: shadow-development
phase: "AD-V2-P03"
version: "0.3.0"
baseline: "V1 closed + P00 + P01 + P02"
---
# Alpha Desk V2 — Phase 03 Price Transmission Engine

## Mission

P03 makes **Price Transmission** a first-class downstream diagnostic object.

P02 answers:

> What is the horizon-specific causal Directional Pressure, independent of target price?

P03 answers a different question:

> Given that frozen Pressure state, how is the target instrument actually responding, and how different is that response from the response that was declared ex ante?

The two questions are constitutionally separate.

## P03 adds

- frozen expected-response signatures tied to one P02 Pressure fingerprint;
- point-in-time response windows that begin only after the expectation was frozen;
- pressure-aligned target-response normalization;
- `ALIGNED`, `ALIGNED_INCOMPLETE`, `DELAYED`, `COMPRESSION`, `UNDER_TRANSMISSION`, `NEGATIVE_TRANSMISSION`, `OVER_TRANSMISSION`, and `UNDETERMINED` states;
- diagnostic Transmission Efficiency, never treated as probability;
- actual-minus-expected counterfactual residual intervals;
- pathway/coherence diagnostics for declared cross-asset or causal transmission channels;
- mechanically-linked proxy controls and independence groups;
- Model Disagreement / Unmodeled Driver Risk escalation;
- missing-driver research escalation without post-hoc story creation;
- strict proof that target price cannot mutate P02 Pressure.

## P03 does not add

P03 does **not** implement:

- Unreleased Pressure;
- Opposing-Move Maturity;
- Release Readiness;
- a `RELEASE` state;
- confirmed absorption, liquidity-grab or institutional-accumulation labels from price alone;
- Fundamental Direction changes;
- positive trade permission;
- broker/execution authority.

Those remain P04+ responsibilities.

## Core one-way graph

`CAUSAL EVIDENCE -> P02 PRESSURE (frozen) -> P03 EXPECTED SIGNATURE (frozen) -> ACTUAL PRICE/CROSS-ASSET RESPONSE -> TRANSMISSION DIAGNOSTIC`

There is no reverse edge from Price Transmission into P02 Pressure.

## Deployment

`SHADOW_ONLY`.
