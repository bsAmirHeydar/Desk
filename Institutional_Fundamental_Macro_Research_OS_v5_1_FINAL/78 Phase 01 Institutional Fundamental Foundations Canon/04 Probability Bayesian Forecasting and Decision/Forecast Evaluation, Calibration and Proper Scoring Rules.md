---
title: "Forecast Evaluation, Calibration and Proper Scoring Rules"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, probability]
---

# Forecast Evaluation, Calibration and Proper Scoring Rules

> [!abstract] Canonical thesis
> Forecast quality must be evaluated out of sample with definitions fixed in advance. Accuracy, calibration, sharpness, discrimination, economic relevance and stability answer different questions.

## Beginner intuition

A forecaster can be well calibrated but vague, or sharp but overconfident. A model can have low average error while missing every turning point. Evaluation needs several metrics and honest samples.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Calibration | Agreement between probabilities and frequencies. |
| Sharpness | Concentration of predictive distributions, judged subject to calibration. |
| Discrimination | Ability to assign higher probabilities to outcomes that occur. |
| Proper scoring rule | A score optimized by reporting true beliefs. |
| Benchmark | A simple or incumbent forecast that the model must improve upon. |

## Mechanism map

1. Freeze target, horizon and information set.
2. Select naive, survey and model benchmarks.
3. Use rolling or expanding out-of-sample evaluation.
4. Score point and density forecasts appropriately.
5. Analyze regimes, tails and turning points.
6. Test whether gains survive revisions, costs and model selection.

## Formal structure and notation

### Brier score

$$
BS=\frac{1}{N}\sum_{t=1}^{N}(p_t-y_t)^2
$$

Lower scores are better. Decomposition separates reliability, resolution and uncertainty.

### Log score

$$
LS=-\frac{1}{N}\sum_{t=1}^{N}\log p_t(y_t)
$$

The log score strongly penalizes assigning tiny probability to realized outcomes and therefore exposes overconfidence.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Statistical accuracy | Uses generic loss functions and formal tests. | May not align with institutional decision value. |
| Economic-value evaluation | Weights outcomes by mandate and consequences. | Can reward unstable tailoring and complicate comparison. |
| Forecast-combination evaluation | Focuses on robust ensembles. | Combination can hide weak models and correlated errors. |

## Historical and institutional cases

### Recession models

A model can forecast normal periods accurately yet fail at rare turning points; event discrimination and lead time matter.

### Inflation forecasts

Survey, market and model errors differ across stable and supply-shock regimes, requiring regime-conditional evaluation.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Forecast Evaluation, Calibration and Proper Scoring Rules**; begin with: Freeze target, horizon and information set.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Select naive, survey and model benchmarks.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Use rolling or expanding out-of-sample evaluation.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Score point and density forecasts appropriately.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Evaluating on revised data not available at forecast time.
- Choosing metrics after seeing results.
- Ignoring model-search and multiple-testing bias.
- Comparing forecasts with different horizons or cutoffs.
- Using tiny samples to claim calibration.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Forecast Evaluation, Calibration and Proper Scoring Rules**. The topic-specific sequence is:

1. Freeze target, horizon and information set.
2. Select naive, survey and model benchmarks.
3. Use rolling or expanding out-of-sample evaluation.
4. Score point and density forecasts appropriately.
5. Analyze regimes, tails and turning points.
6. Test whether gains survive revisions, costs and model selection.

## Exercises and accreditation questions

1. Evaluate two binary forecasts using Brier and log scores.
2. Design a pseudo-real-time comparison for inflation forecasts.
3. Explain when a statistically better forecast may have lower decision value.

## Annotated source canon

- **Diebold and Mariano forecast-comparison research.** Predictive accuracy tests and loss differentials.
- **Gneiting and Raftery.** Proper scoring rules and probabilistic forecast evaluation.
- **Mincer and Zarnowitz.** Forecast efficiency and calibration regressions.

## Related canon

- [[72 Historical Research Permission and Alpha Validation Laboratory/15 Forecast Probability Calibration and Confidence Caps]]
- [[53 Research Statistics Forecasting and Causal Inference/08 Multiple Testing False Discovery and Research Budget]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/04 Probability Bayesian Forecasting and Decision/Forecast Distributions, Scenarios and Density Thinking]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/04 Probability Bayesian Forecasting and Decision/Decision Theory, Utility, Loss and Mandate Dependence]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
