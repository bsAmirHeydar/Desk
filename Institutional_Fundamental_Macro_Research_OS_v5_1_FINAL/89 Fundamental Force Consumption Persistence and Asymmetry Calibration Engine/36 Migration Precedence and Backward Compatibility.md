---
title: "Migration Precedence and Backward Compatibility"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Migration Precedence and Backward Compatibility

## Decision purpose

Define how V10.4 records and notes coexist with V11 without silent reinterpretation, broken links or destructive replacement.

## Governing distinctions

- Backward readable does not mean semantically identical.
- V11 enriches V10.4 fields; it does not retroactively calibrate them.
- Canonical precedence is concept-specific.
- Historical records retain their original methodology version.
- Migration maps must be reversible.

## Operating method

1. Preserve V10.4 field names under `legacy_v10_4` or direct compatibility mappings.
2. Map each old field to one or more V11 fields with transformation type.
3. Mark lossless, lossy, contextual and unmappable transformations.
4. Keep old records immutable unless a new derived view is explicitly generated.
5. Use the authority map when notes conflict.
6. Run regression and manifest validators before release.

## Required outputs

- `base_release`
- `target_release`
- `field_map`
- `authority_map`
- `modified_paths`
- `precondition_hashes`
- `rollback_plan`

## Failure modes and controls

- **Failure:** Treating old 0–100 values as calibrated  
  **Control:** Keep scoring mode ordinal unless proven.
- **Failure:** Backfilling new fields from hindsight  
  **Control:** Use null/unavailable unless contemporaneous evidence exists.
- **Failure:** Deleting old canonical paths  
  **Control:** Use redirects or additive references.

## Precedence rule

For `force`, `consumption`, `remaining pressure`, `persistence`, `reversal risk`, `fundamental asymmetry`, `field-level provenance`, `confidence caps` and `calibration status`, Module 89 is primary for methodology version 11.0.0. Earlier notes remain authoritative for non-conflicting asset, source and operational detail.

## Transformation classes

- `LOSSLESS_ALIAS`
- `LOSSLESS_EXPANSION`
- `CONTEXT_REQUIRED`
- `LOSSY_SUMMARY`
- `NOT_INFERABLE`
- `DEPRECATED_SEMANTIC`

No migration process may transform `NOT_INFERABLE` into a guessed value.

## Canonical dependencies

- [[32 Machine-Readable V11 State Schema]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
