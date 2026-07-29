---
title: "Forecast Distributions, Scenarios and Density Thinking"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, probability]
---

# Forecast Distributions, Scenarios and Density Thinking

> [!abstract] Canonical thesis
> Institutional forecasting should represent a distribution of outcomes, not a single path. Scenarios organize mechanisms and tails; density forecasts quantify uncertainty where probabilities are defensible.

## Beginner intuition

A single GDP or inflation number hides asymmetry and tails. A useful forecast asks what outcomes are plausible, how likely they are, what causes them, and how the distribution changes with new evidence.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Point forecast | A single summary such as mean, median or mode. |
| Density forecast | A full probability distribution for future outcomes. |
| Scenario | A coherent conditional path with mechanisms and assumptions. |
| Fan chart | Visual representation of forecast uncertainty across horizons. |
| Tail scenario | Low-frequency or ambiguous outcome with material consequences. |

## Mechanism map

1. Define target and horizon.
2. Construct baseline and rival mechanisms.
3. Estimate central distribution and tail asymmetry.
4. Separate conditional scenario paths from unconditional probabilities.
5. Update weights and distributions as evidence arrives.
6. Score both calibration and sharpness.

## Formal structure and notation

### Mixture distribution

$$
p(y)=\sum_{k=1}^{K}w_k p(y\mid Scenario_k)
$$

Scenario weights and within-scenario densities jointly determine the overall forecast.

### Continuous ranked probability score

$$
CRPS(F,y)=\int_{-\infty}^{\infty}[F(z)-\mathbf 1\{y\le z\}]^2dz
$$

CRPS evaluates the entire predictive distribution and rewards calibration with useful sharpness.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Model density forecasts | Provide coherent quantitative distributions. | Tail and regime behavior may be misspecified. |
| Narrative scenarios | Represent institutional discontinuities and causal pathways. | Probabilities can be arbitrary and scenarios non-exhaustive. |
| Hybrid scenario densities | Combine model core and expert tails. | Requires safeguards against double counting and political weighting. |

## Historical and institutional cases

### Central-bank projections

Median paths can hide committee dispersion, conditionality and asymmetric risks.

### Energy shock

Baseline supply normalization, prolonged disruption and policy-rationing scenarios require different inflation and growth distributions.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Forecast Distributions, Scenarios and Density Thinking**; begin with: Define target and horizon.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Construct baseline and rival mechanisms.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Estimate central distribution and tail asymmetry.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Separate conditional scenario paths from unconditional probabilities.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Assigning scenario probabilities that do not sum coherently.
- Confusing a conditional scenario with a forecast.
- Using symmetric intervals in a skewed regime.
- Optimizing sharpness while losing calibration.
- Ignoring joint dependence among variables.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Forecast Distributions, Scenarios and Density Thinking**. The topic-specific sequence is:

1. Define target and horizon.
2. Construct baseline and rival mechanisms.
3. Estimate central distribution and tail asymmetry.
4. Separate conditional scenario paths from unconditional probabilities.
5. Update weights and distributions as evidence arrives.
6. Score both calibration and sharpness.

## Exercises and accreditation questions

1. Build a three-scenario inflation density.
2. Convert conditional scenarios into an unconditional mixture.
3. Compare point, interval and density scoring.

## Annotated source canon

- **Bank of England fan-chart methodology.** Institutional representation of forecast uncertainty and skew.
- **Gneiting and Katzfuss on probabilistic forecasting.** Calibration, sharpness and scoring.
- **Scenario-planning literature.** Mechanism-based uncertainty and strategic discontinuities.

## Related canon

- [[50 Scenario Intelligence Wargaming and Tail Systems/00 MOC]]
- [[68 Mathematical Econometric and Market Model Monographs/09 Forecast Densities Fan Charts Quantiles and Calibration]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/04 Probability Bayesian Forecasting and Decision/Base Rates, Reference Classes and Conditional Analogues]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/04 Probability Bayesian Forecasting and Decision/Forecast Evaluation, Calibration and Proper Scoring Rules]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
