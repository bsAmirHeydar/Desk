---
title: "AD V2 Phase 00 — Pressure / Price Constitution"
type: constitutional-foundation
status: shadow-development
phase_id: "AD-V2-P00"
version: "0.1.0"
created: 2026-08-15
language: en
---
# AD V2 Phase 00 — Pressure / Price Constitution

## Mission

Phase 00 freezes the conceptual boundary required for the next Alpha Desk generation:

> **Directional Pressure is a causal state. Target Price is a downstream response state.**

The target asset's price path may diagnose transmission, timing, model disagreement, liquidity hypotheses, and trade quality. It must not directly create, flip, strengthen, weaken, consume, or tie-break Directional Pressure.

This phase is deliberately constitutional. It does not implement the new Pressure engine, Transmission engine, latent-state engine, Gold specialization, UI, or D4 calibration. Those later phases must conform to the laws defined here.

## V1 preservation

Alpha Desk V1 is the closed baseline. Phase 00:

- does **not** edit `CURRENT_PRODUCTION_MANIFEST.*`;
- does **not** edit the V21.3 production prompt;
- does **not** edit Module 89, Module 103, D3, D4, or R4 runtime code;
- does **not** alter Direction or permission authority;
- does **not** mutate promotion registries;
- does **not** add broker-write authority;
- installs only a new `NEXT_VERSION` development surface.

## Canonical owner map for V2 growth

Phase 00 does not create a new market-science module. Future implementation must extend existing owners:

- Module 89 → Directional Pressure and its causal component ledger;
- Modules 95–100 → evidence, observability, positioning, actual flow, funding, mechanics and capacity;
- Module 103 → Price Transmission, model disagreement, missing-driver escalation, multi-hypothesis reasoning and latent-state adjudication;
- Module 101 → edge/permission modulation only;
- Module 102 / D4 → forward validation, calibration and empirical promotion;
- RUN2/R4 → orchestration, quality gates and certification;
- product UI → faithful rendering of separated states.

## Required reading order

1. [[NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/01 V1 Freeze and V2 Development Boundary]]
2. [[NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/02 Directional Pressure Authority Constitution]]
3. [[NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/03 Target Price Transmission Constitution]]
4. [[NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/04 Authority Provenance and One-Way Causal Graph]]
5. [[NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/05 Counterfactual Residual and Missing Driver Escalation]]
6. [[NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/06 Latent State and Anti-Storytelling Boundary]]
7. [[NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/07 Trade Permission Timing and Technical Boundary]]
8. [[NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/08 Semantic Attack and Certification Standard]]
9. [[NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/09 Migration Backward Compatibility and Non-Promotion]]
10. [[NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/10 Phase 01 Runtime Repair Handoff]]

## Phase 00 acceptance

Phase 00 is accepted only if the machine validator proves:

- V1 critical production files still match the uploaded closed baseline;
- target price is forbidden as Directional Pressure authority;
- target price is permitted only in explicitly downstream diagnostic/timing roles;
- price disagreement can trigger research escalation but cannot directly mutate Pressure;
- hidden-state labels such as `ABSORPTION` or `LIQUIDITY_SWEEP` require independent evidence and may not be asserted from price shape alone;
- no precise latent-pressure probability is authorized without D4 calibration;
- all adversarial cases in `tests/pressure_price_attack_cases.json` pass;
- Phase 00 remains `SHADOW_ONLY` and changes no active production manifest.
