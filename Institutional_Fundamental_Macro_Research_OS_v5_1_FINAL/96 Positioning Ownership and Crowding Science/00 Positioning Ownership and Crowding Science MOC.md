# 96 — Positioning, Ownership and Crowding Science

**Release:** V18.0 / D2  
**Authority mode:** `CANONICAL_SHADOW`  
**Decision authority:** none until D3 promotion.

## Mission
Create an auditable institutional state model for **who owns or is exposed to what, through which instrument, on which horizon, with what identification quality, and how crowded or fragile that state is**.

This module is governed by Module 95 Fact Constitution. It never converts an estimate into an identified position and never creates Fundamental Direction.

## Canonical distinctions
`OWNERSHIP != POSITIONING != EXPOSURE != FLOW != ACTIVITY`

- **Ownership**: legally/economically held units or disclosed holdings.
- **Positioning**: directional or hedged risk state for an identified participant universe.
- **Exposure**: sensitivity to underlying risk, which may arise from cash, futures, options, swaps, or embedded balance-sheet risk.
- **Crowding**: concentration/one-sidedness relative to an explicitly declared reference class.
- **Flow**: change caused by transactions; owned by Module 97.

## Contents
1. Scope and non-goals
2. Participant universe ontology
3. Instrument and economic-exposure normalization
4. Futures and COT contract
5. Options/dealer inference contract
6. ETF/fund/filing ownership contract
7. Systematic strategy estimation contract
8. Crowding and fragility model
9. Point-in-time and lag doctrine
10. Cross-market positioning graph
11. Asset-specific mappings
12. Production shadow state contract
13. Validation and D3 promotion gates

## Hard boundaries
- COT is not live intraday positioning.
- Open interest is not directional net flow.
- Options open interest is not dealer inventory without a defensible counterparty mapping/model.
- CTA, vol-control, risk-parity and passive demand estimates remain `MODEL_INFERENCE` unless directly identified.
- No positioning state may invert or originate Fundamental Direction in V18.

## V21.3 observability completion
- [[96 Positioning Ownership and Crowding Science/14 Securities Lending Short Interest and Borrow Ecology]]
