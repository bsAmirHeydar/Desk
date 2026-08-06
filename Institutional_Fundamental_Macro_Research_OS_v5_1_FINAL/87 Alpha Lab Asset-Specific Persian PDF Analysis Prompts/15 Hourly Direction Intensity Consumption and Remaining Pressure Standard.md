---
title: "Alpha Lab Hourly Direction Intensity Consumption and Remaining Pressure Standard"
type: hourly-scoring-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [alpha-lab, direction, intensity, consumption, remaining-pressure, scoring]
---
# Alpha Lab Hourly Direction Intensity Consumption and Remaining Pressure Standard

## Purpose

This standard ensures that practical hourly outputs use consistent meanings. Direction, intensity, confidence, consumption and remaining pressure are different objects and must never be collapsed into one score.

## Direction

Direction answers: **If the current fundamental information set were the only relevant force, which directional pressure does it create for the specified instrument over the selected horizon?**

Direction does not answer how large the move will be or whether the market will move immediately.

## Intensity

Intensity answers: **How powerful is the currently active information, policy, earnings, physical-balance, risk-premium or institutional-constraint impulse?**

Intensity is high when the shock changes an economically important state variable and transmits broadly. It is not confidence.

## Confidence

Confidence answers: **How reliable is the evidence and causal interpretation?**

A state can be high intensity and low confidence. Example: a violent move during thin liquidity with incomplete confirmation.

## Consumption

Consumption answers: **How much of the identifiable catalyst and its expected transmission appears already absorbed?**

Consumption has multiple dimensions and must be reported as a vector. A single aggregate consumption label may be shown only as a plain-language summary after the components are disclosed.

## Remaining pressure

Remaining pressure answers: **After accounting for absorption, repricing, flow exhaustion, contradictions, valuation, the next catalyst and time decay, how much directional fundamental force appears to remain?**

Remaining pressure is not `100 - price move`. It is a residual analytical state.

## Suggested qualitative bands

| Score | Persian interpretation |
|---:|---|
| 0–19 | بسیار کم |
| 20–39 | کم |
| 40–59 | متوسط |
| 60–79 | زیاد |
| 80–100 | بسیار زیاد |

Use the bands as communication aids, not calibrated probabilities.

## Consumption summary labels

After presenting the vector, select one summary:

- `BARELY_CONSUMED`
- `PARTIALLY_CONSUMED`
- `MOSTLY_CONSUMED`
- `FULLY_OR_OVER_CONSUMED`
- `REINFORCED_AND_REOPENED`
- `UNDETERMINED`

Persian labels:

- `BARELY_CONSUMED` → `محرک هنوز عمدتاً مصرف نشده است`
- `PARTIALLY_CONSUMED` → `بخشی از محرک مصرف شده است`
- `MOSTLY_CONSUMED` → `بخش عمده محرک مصرف شده است`
- `FULLY_OR_OVER_CONSUMED` → `محرک تقریباً کامل یا بیش‌ازحد مصرف شده است`
- `REINFORCED_AND_REOPENED` → `اطلاعات جدید ظرفیت حرکت را دوباره افزایش داده است`
- `UNDETERMINED` → `میزان مصرف قابل‌تشخیص نیست`

## Practical synthesis matrix

| Direction | Intensity | Consumption | Remaining pressure | Practical interpretation |
|---|---|---|---|---|
| Positive | High | Low | High | fresh positive fundamental impulse |
| Positive | High | High | Low | strong move but increasingly mature or saturated |
| Positive | Low | High | Very low | residual positive narrative with little remaining force |
| Negative | High | Low | High | fresh negative fundamental impulse |
| Negative | High | High | Low | mature negative repricing with rising reversal sensitivity |
| Neutral | Any | Any | Low | no clear directional fundamental advantage |
| Unresolved | High | Unknown | Unknown | binary or contradictory event state; avoid false precision |

## Score construction discipline

Each score must be supported by a short component ledger. Do not create a hidden black-box number.

Suggested components for direction and intensity:

- surprise magnitude;
- policy-path revision;
- cash-flow or earnings revision;
- valuation/risk-premium revision;
- physical-balance revision;
- funding or collateral change;
- cross-asset confirmation;
- institutional amplification;
- contradiction penalty;
- freshness penalty.

Suggested components for consumption and remaining pressure:

- elapsed time since catalyst;
- information absorption;
- market-implied repricing;
- breadth of transmission;
- positioning/flow completion;
- narrative saturation;
- valuation stretch;
- liquidity distortion;
- next catalyst proximity;
- reinforcing information;
- unresolved opposing evidence.

## State transition logic

A state normally evolves through:

`FORMING → STRENGTHENING → MATURE → CONSUMING → EXHAUSTED`

Possible alternative transitions:

- `FORMING → REVERSING` when initial interpretation fails;
- `MATURE → STRENGTHENING` after reinforcing evidence;
- `CONSUMING → REINFORCED_AND_REOPENED` after a new catalyst;
- any phase → `UNRESOLVED` when contradictions become material.

## Consumption traps

Avoid these errors:

- assuming a large price move means a fully consumed catalyst;
- treating elapsed time as the only consumption variable;
- confusing low freshness with full repricing;
- ignoring an upcoming event that may reopen the thesis;
- calling a flow-driven squeeze a fundamental underreaction;
- treating consensus narrative saturation as economic-state completion;
- assigning precise percentages when key flow data are unavailable.
## V10.4 adaptive thresholds

Mandatory checkpoints are recorded regardless of score change. Additional material records use 5-point thresholds for direction, intensity and confidence and 10-point thresholds for absorption, repricing completion, flow exhaustion, freshness, saturation, remaining pressure, confirmation and reversal risk. Any categorical change in direction, leader, model, persistence, move quality, edge, confirmation or thesis status is always material.

---

## V11 governing extension

For methodology version `11.0.0`, the definitions above remain valid and are extended—not replaced—by Module 89:

- force components and applicability: [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/03 Fundamental Force and Intensity Decomposition]];
- consumption lifecycle: [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/07 Consumption Vector and Lifecycle]];
- counterfactual repricing: [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/09 Repricing Completion and Counterfactual Baselines]];
- remaining pressure: [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/13 Remaining Fundamental Pressure Decomposition]];
- provenance and false precision: [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/21 Score Provenance Intervals and False-Precision Control]].

V10.4 numeric values remain ordinal. They become calibrated estimands only under explicitly declared `EMPIRICALLY_CALIBRATED_MODE` with out-of-sample evidence.
