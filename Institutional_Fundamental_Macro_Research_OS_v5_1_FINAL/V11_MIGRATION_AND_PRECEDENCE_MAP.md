---
title: "V11 Migration and Precedence Map"
type: migration-map
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# V11 Migration and Precedence Map

# V11 Migration and Precedence Map

## Base and target

- Compatible operational base: Module 88 release `10.4.0`.
- Target methodology: `11.0.0`.
- Migration mode: additive and backward compatible.
- Historical V10.4 records remain immutable.
- No historical ordinal score is retroactively converted into a calibrated probability.

## Concept precedence

Module 89 is primary in V11 for:

- fundamental force/intensity decomposition;
- consumption lifecycle and counterfactual repricing;
- remaining-pressure residual decomposition;
- persistence and half-life;
- reversal hazard;
- fundamental path asymmetry and edge availability;
- field-level provenance;
- confidence caps;
- calibration status and model retirement.

Module 88 remains governing for hybrid daily/session/event record density, micro-windows, no-change reassessment, immutable-state audit and historical reconstruction unless Module 89 explicitly extends a field.

## Compatibility

See:

- `89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/V10_4_TO_V11_FIELD_MAP.csv`
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/36 Migration Precedence and Backward Compatibility]]
- `V11_CANONICAL_AUTHORITY_MAP.yaml`

## Non-inferable fields

V11 fields that were not contemporaneously observed must remain null, `UNAVAILABLE` or `UNDETERMINED`. They must not be reconstructed from later market outcomes.
