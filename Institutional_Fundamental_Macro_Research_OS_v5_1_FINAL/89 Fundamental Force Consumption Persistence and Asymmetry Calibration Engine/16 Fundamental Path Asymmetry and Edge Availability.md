---
title: "Fundamental Path Asymmetry and Edge Availability"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Fundamental Path Asymmetry and Edge Availability

## Decision purpose

Define asymmetry in fundamental state space: limited, observable thesis invalidation versus a materially larger unresolved repricing distribution, conditional on persistence, liquidity and event risk.

## Governing distinctions

- Asymmetry is not direction alone.
- A small technical stop is outside the fundamental model.
- High expected move with unbounded event gap is not clean asymmetry.
- Edge availability depends on consumption and timing.

## Operating method

1. Define fundamental invalidation boundary.
2. Estimate favorable and adverse repricing ranges.
3. Condition on persistence, consumption and remaining pressure.
4. Add event-gap and liquidity-path risks.
5. Assign asymmetry class and execution-handoff status.

## Required outputs

- `fundamental_downside_boundary`
- `invalidation_trigger`
- `expected_repricing_range`
- `adverse_path_range`
- `event_gap_risk`
- `liquidity_path_risk`
- `path_asymmetry_class`
- `execution_handoff_status`

## Failure modes and controls

- **Failure:** Direction score used as asymmetry score  
  **Control:** Build two-sided payoff ranges.
- **Failure:** Price-based stop embedded in the canon  
  **Control:** Return only fundamental boundaries to execution.
- **Failure:** Unknown binary risk ignored  
  **Control:** Use `UNTRADEABLE_BINARY` or cap edge availability.

## Fundamental asymmetry test

A state is asymmetrically attractive only when the fundamental downside boundary is explicit, unresolved repricing is materially larger than the adverse path, the thesis has survival capacity, and the next-catalyst/liquidity map does not hide unbounded gap risk.

The output is a handoff to execution. It must not prescribe chart patterns, indicators or technical stop placement.

| Class | Interpretation |
|---|---|
| `HIGH_POSITIVE_ASYMMETRY` | narrow invalidation, large unresolved positive repricing |
| `MODERATE_POSITIVE_ASYMMETRY` | positive residual with material event/path risk |
| `SYMMETRIC_OR_UNCLEAR` | payoff ranges overlap or evidence is insufficient |
| `MODERATE_NEGATIVE_ASYMMETRY` | negative residual with bounded positive risk |
| `HIGH_NEGATIVE_ASYMMETRY` | narrow invalidation, large unresolved negative repricing |
| `UNTRADEABLE_BINARY` | edge cannot be bounded before a binary catalyst |

## Canonical dependencies

- [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]
- [[62 Institutional Templates Schemas and Control Checklists/08 Execution Handoff and Permission Template]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
