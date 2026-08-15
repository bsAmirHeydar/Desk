---
title: "Alpha Desk V2 Phase 05 Gold Intelligence Specialization"
type: development-moc
status: shadow-development
phase: "AD-V2-P05"
version: "0.5.0"
baseline: "V1 closed + P00 + P01 + P02 + P03 + P04"
---
# Alpha Desk V2 — P05 Gold Intelligence Specialization

## Mission

P05 binds the generic V2 scientific stack to **Gold / XAUUSD** without granting price, momentum, one venue or one proxy authority over the upstream causal state.

P05 answers a narrower institutional question:

> For Gold, exactly which observations are causal Pressure roots, dependent causal-pathway signals, target-price transmission observations, positioning/flow/funding/mechanics evidence, event-reset clocks, structural background or unavailable/private gaps — and how may each observation legally enter P02, P03 and P04?

## Core design

Gold is not one venue. It is simultaneously:

- London OTC monetary gold;
- COMEX futures/options;
- physically backed ETFs;
- official-sector reserve demand;
- regional physical markets;
- a USD/real-rate-sensitive monetary asset;
- a safe-haven / credibility-risk asset.

Therefore P05 specializes **roles and observability**, not a single magic Gold indicator.

## P05 adds

- Gold instrument/venue ontology;
- source and metric registry with cadence, access and hard boundaries;
- Pressure-root dependency graph;
- target-price and cross-asset Transmission map;
- Gold-specific adapters into P02/P03/P04;
- explicit evidence independence groups;
- event-reset and session-window registry;
- Gold-specific missing-driver search order;
- public/licensed/private observability accounting;
- fail-closed controls against COMEX=global-gold, volume=flow, OI=direction, ETF AUM=flow, options OI=dealer inventory, and target-price contamination.

## P05 does not add

- a new Direction authority;
- a new Pressure formula;
- a new Transmission state machine;
- a new Release formula;
- trade-entry permission or technical trigger authority;
- broker authority;
- empirical probabilities;
- automatic institutional identity inference;
- automatic absorption/liquidity-grab confirmation.

P02, P03 and P04 remain the scientific authorities. P05 is a Gold-specific **adapter and evidence constitution**.

Deployment: `SHADOW_ONLY`.
