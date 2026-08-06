---
title: "V11 Benchmark Scenarios and Acceptance Tests"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# V11 Benchmark Scenarios and Acceptance Tests

## Decision purpose

Provide adversarial frozen-information cases that test reasoning, provenance, confidence caps, horizon separation and V10.4 preservation rather than only file structure.

## Governing distinctions

- Benchmarks test expected reasoning ranges, not one magic answer.
- Future evidence is prohibited.
- Pass criteria include uncertainty handling.
- Flow and fundamental explanations may coexist.
- A valid `UNDETERMINED` can outperform false precision.

## Operating method

1. Freeze an information packet and cutoff.
2. List allowed and prohibited evidence.
3. Run the V11 production prompt independently.
4. Compare required fields, state ranges, rival models and caps.
5. Adjudicate failures by ontology, evidence, reasoning or schema class.
6. Store benchmark version and methodology version.

## Required outputs

- `benchmark_id`
- `frozen_cutoff`
- `allowed_evidence`
- `prohibited_evidence`
- `expected_reasoning`
- `acceptable_ranges`
- `required_caps`
- `pass_fail`

## Failure modes and controls

- **Failure:** Judging only by direction outcome  
  **Control:** Score state estimation and causal process separately.
- **Failure:** Leaking later revisions  
  **Control:** Use frozen packets.
- **Failure:** Overfitting benchmark wording  
  **Control:** Use paraphrased and held-out cases.

## Required benchmark catalogue

| ID | Scenario | Core acceptance condition |
|---|---|---|
| B01 | CPI surprise; full front-end repricing, incomplete equity transmission | Do not call equity consumption complete; rates channel mature, equity channel open. |
| B02 | Headline reversed by official clarification | Force collapses; flow may persist briefly; reversal hazard rises. |
| B03 | Quiet day with no headline | Consumption/remaining pressure may change with immutable no-change/delta record. |
| B04 | Mega-cap beat, weak forward revisions | Headline force high; durable cash-flow force low/moderate. |
| B05 | Nasdaq dealer/CTA rally, weak fundamentals | Flow propagation separated from fundamental confirmation. |
| B06 | S&P direction stable, edge falls | High consumption and valuation compression reduce edge. |
| B07 | Gold haven impulse then dollar liquidation | Slow thesis and fast liquidation regime coexist. |
| B08 | Gold central-bank demand | Low freshness can coexist with persistent slow pressure. |
| B09 | EURUSD divergence pre-priced | Statement direction and remaining pressure diverge. |
| B10 | EURUSD month-end flow | Flow model dominates intraday, fundamental state unchanged. |
| B11 | Treasury auction term-premium shock | Curve segment and channel correctly isolated. |
| B12 | Tariff social post, uncertain timestamp | Chronology and confidence cap mandatory. |
| B13 | Missing proprietary flow data | No high-confidence flow exhaustion claim. |
| B14 | Second independent release reinforces thesis | State is reopened/extended, not reset blindly. |
| B15 | Policy reaction reopens consumed catalyst | Repricing baseline and next-catalyst map updated. |
| B16 | Broad move, no causal leader | Direction may be observed; attribution remains undetermined. |
| B17 | Mechanically related confirmations | Independence discount applied. |
| B18 | Later revision contamination | Historical state uses first release only. |
| B19 | Regime shift breaks old mapping | Calibration status downgraded; model retirement considered. |
| B20 | Two analysts disagree on consumption | Adjudication and residual disagreement stored. |
| B21 | High direction/intensity/consumption, low remaining pressure | No contradiction; low new-entry edge. |
| B22 | Moderate intensity, low consumption, high persistence/asymmetry | High-quality slow-burn candidate. |
| B23 | Low price move before next event | Do not infer low force; event waiting model considered. |
| B24 | Overshoot and over-consumption | Reversal hazard and payoff compression rise. |
| B25 | Structural bull, tactical bearish event | Horizon states remain separate. |

Machine-readable fixtures live under `benchmarks/`. Each fixture must identify its expected semantic checks and must not embed future price outcomes in the input.

## Canonical dependencies

- [[23 Historical Point-in-Time Calibration Laboratory]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
