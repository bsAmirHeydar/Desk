---
title: "V1 Runtime Semantic Defect Census"
type: defect-census
status: frozen-baseline-observation
---
# V1 Runtime Semantic Defect Census

This document describes defects in the **last-mile V1 runtime adapter**, not defects in the underlying V1 scientific Vault.

## D01 — Force source category violation

Current V1 adapter logic searches `research_intent.force / force_state / directional_force / force_tier`. Those fields do not exist in the V21.2 Research Intent schema. It can then fall back to `driver_transition.force / strength / state`; the Driver Transition schema only owns a transition `state` such as `STABLE`, `TRANSFER` or `TAKEOVER`.

Therefore `TAKEOVER` can occupy the runtime slot named `force` even though it is not a Force measurement.

## D02 — Fundamental Force owner bypassed

W31 produces `fundamental_state` from Module 89 using the V11 schema. That object already contains `force`, horizon-specific `force_range`, `consumption_v2`, `remaining_pressure_v2`, `persistence_v2`, horizon-specific `persistence_class`, `reversal_risk` and update triggers. V1 lifecycle construction does not read this authoritative object.

## D03 — Consumption vocabulary mismatch

Module 103 cognitive `consumption_state` owns `lifecycle_state`; the V1 adapter searches generic keys such as `consumption`, `consumption_state`, `state`, `status` and can therefore return UNKNOWN despite a valid artifact.

More importantly, Module 89 also owns **Fundamental Consumption** as `fundamental_state.v11_fundamental_state.consumption_v2.summary_state`. P01 separates these two objects instead of flattening them.

## D04 — Remaining Pressure / Remaining Asymmetry conflation

V1 can map `research_intent.remaining_asymmetry` or `consumption_state.remaining_asymmetry` into `remaining_pressure`. Module 89's own migration map explicitly says Remaining Pressure is not an arithmetic or semantic synonym for Remaining Asymmetry.

## D05 — Persistence owner bypassed

Module 89 owns `persistence_v2` and active-horizon `persistence_class`. V1 lifecycle construction instead searches fields not present in Research Intent or Driver Transition.

## D06 — Reversal object ambiguity

Research Intent owns `reversal_hazard`; Module 89 active-horizon state owns `reversal_risk`, while Remaining Pressure contains a `reversal_hazard` score. These need provenance and horizon, not a generic fallback chain.

## D07 — Report-level fallback reintroduces conflation

`report_model.py` uses `remaining_asymmetry` as a fallback if lifecycle Remaining Pressure is absent. P01 forbids this in V2.

## D08 — Presence-only semantic gate

`FORCE_STATE_INTEGRITY` currently verifies required keys exist. A wrong semantic value can still pass if the key is present. P01 creates `SEMANTIC_OWNERSHIP_INTEGRITY` in shadow acceptance.

## D09 — Delta lineage loss

V1 run-memory compares flattened lifecycle values without retaining their legal owner/source path. P01 requires provenance on every load-bearing field.

## D10 — Canonical schema is structurally permissive

The V1 Canonical Scientific Result permits an open `science` object. This is compatible with flexible evolution, but it cannot alone enforce lifecycle ownership. P01 adds a V2 shadow schema rather than tightening the closed V1 schema.
