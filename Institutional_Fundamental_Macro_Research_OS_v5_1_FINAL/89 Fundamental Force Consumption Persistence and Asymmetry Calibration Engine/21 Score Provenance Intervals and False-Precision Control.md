---
title: "Score Provenance Intervals and False-Precision Control"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Score Provenance Intervals and False-Precision Control

## Decision purpose

Stop false precision by attaching semantics and provenance to every number, interval and scenario weight.

## Governing distinctions

- A 70/100 ordinal score is not a 70% probability.
- A model-implied probability is not empirically calibrated.
- A range can be more honest than a point.
- The same scale cannot represent different estimands silently.

## Operating method

1. Declare scoring mode and estimand.
2. Attach field-level provenance and units.
3. Use intervals when mapping uncertainty is material.
4. Validate probability language against calibration metadata.
5. Version every methodology and comparison.

## Required outputs

- `scoring_mode`
- `estimand`
- `unit`
- `field_level_ledger`
- `interval`
- `calibration_reference`
- `methodology_version`

## Failure modes and controls

- **Failure:** Percent sign attached to ordinal score  
  **Control:** Block with false-probability validator.
- **Failure:** Scenario weight called win probability  
  **Control:** Label as judgmental/model-implied unless calibrated.
- **Failure:** Method changed but score compared directly  
  **Control:** Require migration or non-comparability flag.

## Required provenance enum

`OBSERVED`, `OFFICIAL_FIRST_RELEASE`, `OFFICIAL_REVISION`, `DERIVED_DETERMINISTIC`, `MARKET_IMPLIED`, `EMPIRICALLY_CALIBRATED`, `MODEL_IMPLIED`, `PUBLIC_PROXY`, `LICENSED_DATA`, `PROPRIETARY_DATA`, `STRUCTURED_JUDGMENT`, `UNAVAILABLE`.

Every load-bearing field records value/range, unit, provenance, locator, vintage, methodology version, confidence, missing-input penalty, rationale and next-update condition.

## Numeric semantics

- Ordinal scores communicate rank or band within a rubric.
- Percentiles require a declared reference distribution.
- Probabilities require a defined event, horizon, sample and calibration report.
- Expected moves require units and conditioning set.
- Scenario weights may be judgmental but must say so.

## Canonical dependencies

- [[81 Scientific QA and Certification Framework/14 Confidence Calibration and False-Precision Gate]]
- [[84 Canonical Retrieval Evidence and Version Control/05 Prompt and Analysis Version Ledger]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
