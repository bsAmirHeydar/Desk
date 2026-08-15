---
title: "Alpha Desk V2 Phase 01 Runtime Semantic Repair"
type: development-moc
status: shadow-development
phase: "AD-V2-P01"
version: "0.1.0"
baseline: "V21.3.0 / R4.0.0"
---
# Alpha Desk V2 — Phase 01 Runtime Semantic Repair

## Mission

Phase 01 creates the **semantic runtime substrate** for Alpha Desk V2 without rewriting the closed V1 production runtime. It turns the lifecycle fields that V1 currently flattens ambiguously into typed, owner-bound, provenance-carrying V2 shadow objects.

Phase 01 is deliberately not the new Pressure Engine. It repairs the semantic plumbing first.

## Why this phase exists

Inspection of the closed V1 runtime found that the scientific Vault is richer than the final runtime adapter. The V1 scientific stack already has proper objects for Fundamental Force, Consumption, Remaining Fundamental Pressure, Persistence, horizon-specific reversal risk, cognitive consumption, Remaining Asymmetry and Driver Transition. The last-mile runtime currently collapses some of them through permissive fallbacks.

The most material defects are:

1. V1 `result.py::_lifecycle()` asks `research_intent` for force fields that its schema does not own;
2. if absent, it can fall back from Force to `driver_transition.state`, whose vocabulary is `STABLE/WEAKENING/TRANSFER/...`, not Force;
3. V1 consumption lookup ignores the schema-defined `consumption_state.lifecycle_state` and also ignores Module 89 `consumption_v2.summary_state`;
4. V1 `remaining_pressure` may fall back to `remaining_asymmetry`, although the Module 89 migration map explicitly says they are different objects;
5. V1 persistence lookup ignores Module 89 `persistence_v2` and the active horizon `persistence_class`;
6. report composition can again substitute Remaining Asymmetry when Remaining Pressure is absent;
7. `FORCE_STATE_INTEGRITY` checks key presence more strongly than semantic owner/provenance;
8. run-memory deltas compare flattened values and therefore cannot prove they came from legal owners.

## V2 repair principle

V2 uses **no semantic substitution across object classes**.

- Force is Force.
- Fundamental Consumption is Fundamental Consumption.
- Cognitive Consumption is Cognitive Consumption.
- Remaining Fundamental Pressure is Remaining Fundamental Pressure.
- Remaining Asymmetry is Remaining Asymmetry.
- Persistence is Persistence.
- Driver Transition is Driver Transition.
- Review timing is not pressure persistence.

Unknown remains unknown. A missing field is never repaired by borrowing a similarly named field from a different science object.

## Deployment

`SHADOW_ONLY`.

No V1 active production file is modified in this phase. P01 provides a V2 semantic adapter, schemas, provenance policy, attack tests and a machine-readable ownership registry. Later V2 phases may integrate this substrate after their own certification.

## Acceptance

P01 passes only when:

- P00 is present and passes;
- the closed V1 runtime fingerprints match;
- all semantic owner mappings resolve to legal V1 schema paths;
- no forbidden cross-object fallback is used;
- missing authoritative data fails closed rather than substituting;
- the legacy defect probe reproduces the known V1 ambiguity and the V2 adapter refuses it;
- active V1 R4 CORE remains PASS;
- rollback removes only P01.
