---
title: "Analyst Reproducibility and Adjudication Protocol"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Analyst Reproducibility and Adjudication Protocol

## Decision purpose

Make force and consumption scores reproducible enough to audit by measuring where analysts agree, disagree and select different evidence.

## Governing distinctions

- Agreement is not validity.
- Disagreement can reveal ontology or evidence defects.
- Numeric agreement without shared reasoning can be spurious.
- Adjudication must preserve original records.

## Operating method

1. Freeze evidence packet and rubric version.
2. Run independent scoring.
3. Measure categorical, numeric and source disagreement.
4. Classify disagreement before adjudication.
5. Revise anchors only through a versioned method change.

## Required outputs

- `analyst_scores`
- `agreement_metrics`
- `disagreement_class`
- `adjudicated_state`
- `residual_disagreement`
- `rubric_version`

## Failure modes and controls

- **Failure:** Analysts discuss before scoring  
  **Control:** Use blinded first pass.
- **Failure:** Only final consensus stored  
  **Control:** Preserve both initial records.
- **Failure:** ICC reported without assumptions or sample  
  **Control:** Use simpler diagnostics or disclose limitations.

## Double-blind protocol

1. Freeze the identical evidence packet and cutoff.
2. Analysts score independently without seeing each other's output.
3. Compare categorical state, numeric bands, sources and causal models.
4. Classify disagreements as evidence selection, definition, causal interpretation, horizon, weighting or arithmetic.
5. Adjudicate with a third reviewer or predeclared rule.
6. Store original scores, adjudicated result and residual disagreement.

Suggested diagnostics include weighted kappa for categories, ICC only when assumptions are defensible, median absolute disagreement, direction-sign agreement, edge-state agreement and source-selection divergence. They are diagnostics, not truth metrics.

## Canonical dependencies

- [[81 Scientific QA and Certification Framework/22 Weighted Review Rubric and Inter-Rater Protocol]]
- [[24 Research Engineering Source Library and Alpha Lab/00 24 Research Engineering Source Library and Alpha Lab MOC]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
