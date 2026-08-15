---
title: "Alpha Desk V2 Phase 04 Latent Pressure Maturity and Release Engine"
type: development-moc
status: shadow-development
phase: "AD-V2-P04"
version: "0.4.0"
baseline: "V1 closed + P00 + P01 + P02 + P03"
---
# Alpha Desk V2 — Phase 04 Latent Pressure, Maturity and Release Engine

## Mission

P04 formalizes the market state that motivated Alpha Desk V2:

> Causal Pressure can remain strong while target Price moves against it. The system must estimate how much causal capacity remains unreleased, whether the opposing move is still gaining causal sponsorship or is maturing, and whether transmission is beginning to release — without turning price action into causal evidence or storytelling.

P04 consumes immutable P02 Pressure and valid P03 Transmission. It may additionally use independent evidence from flow, positioning, funding, mechanics, options/dealer state, physical balance, event state and market-liquidity research.

## P04 adds

- Unreleased Pressure as an ordinal latent-state estimate;
- Opposing-Move Maturity;
- Latent Causal Reserve / Stored Energy state;
- Transmission Inflection;
- Release Readiness;
- a conservative lifecycle: `PRESSURE_BUILDING -> DIVERGENCE -> OPPOSING_MOVE_ACTIVE -> PRE_RELEASE -> RELEASE_CANDIDATE -> RELEASE -> EXPANSION -> CONSUMPTION -> EXHAUSTION`;
- independent-evidence requirements for Release;
- P02 recomputation blockers when a genuinely new causal driver is discovered;
- event-reset vetoes;
- hypothesis support for absorption/liquidity states without definitive promotion.

## P04 does not add

- trade entry permission;
- technical trigger ownership;
- expected R or probability;
- broker/execution authority;
- target-price authority over P02 Pressure;
- definitive `liquidity grab`, `absorption`, `institutional accumulation` or `forced liquidation` labels from price alone;
- Gold-specific source calibration (P05 responsibility);
- empirical promotion of Release Readiness (later D4/true-forward responsibility).

## Deployment

`SHADOW_ONLY`.
