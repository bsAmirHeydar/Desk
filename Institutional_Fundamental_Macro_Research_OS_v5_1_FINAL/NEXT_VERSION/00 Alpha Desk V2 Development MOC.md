---
title: "Alpha Desk V2 Development"
type: development-moc
status: shadow-development
product_generation: "V2"
baseline_scientific_stack: "V21.3.0"
baseline_runtime: "R4.0.0"
phase: "P00"
created: 2026-08-15
language: en
---
# Alpha Desk V2 Development

## Purpose

Alpha Desk V1 is closed as the production reference. V2 development proceeds by **versioned extension with explicit precedence**, not by silently rewriting the meaning of the V1 scientific stack.

The V1 production baseline remains:

- scientific stack: `V21.3.0`;
- runtime certification baseline: `R4.0.0`;
- Fundamental Direction authority: Module 89 at the active strategy horizon;
- market/target price Direction authority: none;
- D3/D4 and operational safety authorities unchanged.

## Development law

Every V2 phase must declare:

1. the V1 authority it extends;
2. whether it changes active production authority;
3. backward-compatibility and migration behavior;
4. machine-verifiable invariants;
5. fail-closed conditions;
6. promotion state (`SHADOW_ONLY`, `RESEARCH_VALIDATED`, or `PROMOTED`).

V2 work is not allowed to acquire production authority merely by being present in the repository.

## Current phase

Start at:

- [[NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/00 Phase 00 Pressure Price Constitution MOC]]

Phase 00 establishes the constitutional separation between **Directional Pressure** and **Target Price behavior**. It changes no live V1 production decision semantics and grants no broker, permission, or Direction authority.
