---
title: "Machine-Readable V11 State Schema"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Machine-Readable V11 State Schema

## Decision purpose

Define the backward-compatible data contract for recording V11 states, provenance, horizons, calibration status and validation results.

## Governing distinctions

- Schema validity is not scientific truth.
- Null, unavailable and not-applicable are different.
- A score’s numeric range does not define its meaning.
- V10.4 fields remain readable.
- Every load-bearing value needs provenance.

## Operating method

1. Validate records with `v11_fundamental_state.schema.json`.
2. Declare scoring mode and estimand before interpreting numeric values.
3. Populate field-level provenance and confidence caps.
4. Store horizon states separately.
5. Run schema, provenance, confidence, false-probability and horizon validators.
6. Preserve the V10.4 compatibility envelope.

## Required outputs

- `schema_version`
- `methodology`
- `legacy_v10_4`
- `force`
- `expectations`
- `consumption_v2`
- `remaining_pressure_v2`
- `persistence_v2`
- `asymmetry_v2`
- `horizon_states`
- `provenance`
- `validation`

## Failure modes and controls

- **Failure:** Using zero for unavailable  
  **Control:** Use explicit null plus provenance status.
- **Failure:** Calling a schema-valid record calibrated  
  **Control:** Calibration status is independent.
- **Failure:** Reusing score meanings across models  
  **Control:** Bind estimand and methodology version.
- **Failure:** Flattening horizon records  
  **Control:** Use one row per record-horizon in CSV.

## Companion artifacts

- `v11_fundamental_state.schema.json`
- `V11_FLATTENED_STATE_CONTRACT.csv`
- `V10_4_TO_V11_FIELD_MAP.csv`
- `examples/`
- `tools/validate_v11_state_schema.py`

The JSON Schema is intentionally conservative. Semantic validators enforce constraints that are awkward or misleading to express in JSON Schema alone.

## Canonical dependencies

- [[36 Migration Precedence and Backward Compatibility]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
