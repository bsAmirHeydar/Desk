---
title: "Bayesian Updating, Priors, Likelihoods and Model Comparison"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, probability]
---

# Bayesian Updating, Priors, Likelihoods and Model Comparison

> [!abstract] Canonical thesis
> Bayesian reasoning updates prior beliefs through the relative likelihood of evidence under competing hypotheses. Institutional use requires transparent priors, explicit likelihoods, model uncertainty and protection against repeated narrative redefinition.

## Beginner intuition

If two explanations predict the same data equally well, the new data do not distinguish them. If one explanation made the observation much more likely, belief should shift toward it. The amount of shift depends on prior plausibility and evidence strength.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Prior | Belief before incorporating the specified evidence. |
| Likelihood | Probability of observed evidence under a hypothesis or parameter. |
| Posterior | Updated belief after evidence. |
| Bayes factor | Relative evidence between models from their marginal likelihoods. |
| Posterior predictive | Distribution of future or replicated data integrating parameter uncertainty. |

## Mechanism map

1. Define mutually distinguishable hypotheses.
2. State priors and their source.
3. Specify likelihood and measurement model.
4. Update with evidence in publication order.
5. Test sensitivity to priors and alternative likelihoods.
6. Evaluate posterior predictions and revise the model set.

## Formal structure and notation

### Bayes theorem

$$
P(H\mid D)=\frac{P(D\mid H)P(H)}{\sum_j P(D\mid H_j)P(H_j)}
$$

The denominator ensures beliefs across the hypothesis set remain coherent; omitted hypotheses can create false certainty.

### Posterior predictive

$$
p(\tilde y\mid D)=\int p(\tilde y\mid\theta)p(\theta\mid D)d\theta
$$

Prediction integrates parameter uncertainty instead of substituting a single estimated coefficient.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Objective or weakly informative priors | Reduce overt subjectivity. | Can still encode scale and parameterization choices. |
| Expert priors | Use institutional knowledge and sparse historical evidence. | Vulnerable to overconfidence and group incentives. |
| Model averaging | Represents uncertainty across models. | Weights can reward in-sample fit and omit unknown models. |

## Historical and institutional cases

### Inflation persistence

Priors based on pre-pandemic dynamics should update when supply, fiscal and labor evidence becomes more likely under alternative models.

### Bank solvency

New deposit-flow and asset-valuation data update loss and run scenarios, but likelihoods depend on policy backstop assumptions.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Bayesian Updating, Priors, Likelihoods and Model Comparison**; begin with: Define mutually distinguishable hypotheses.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: State priors and their source.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Specify likelihood and measurement model.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Update with evidence in publication order.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Using posterior language without specifying priors or likelihood.
- Resetting the prior after observing evidence.
- Updating repeatedly on correlated evidence as if independent.
- Excluding a plausible model from the hypothesis set.
- Treating model probability as proof of literal truth.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Bayesian Updating, Priors, Likelihoods and Model Comparison**. The topic-specific sequence is:

1. Define mutually distinguishable hypotheses.
2. State priors and their source.
3. Specify likelihood and measurement model.
4. Update with evidence in publication order.
5. Test sensitivity to priors and alternative likelihoods.
6. Evaluate posterior predictions and revise the model set.

## Exercises and accreditation questions

1. Perform an odds-form update for two inflation models.
2. Design priors for a rare sovereign default and test sensitivity.
3. Show how correlated indicators can be double-counted in naive updating.

## Annotated source canon

- **Andrew Gelman et al., Bayesian Data Analysis.** Modern Bayesian modeling, diagnostics and posterior prediction.
- **Harold Jeffreys, Theory of Probability.** Bayesian evidence and model comparison.
- **Philip Tetlock, Expert Political Judgment.** Calibration and updating of expert beliefs.

## Related canon

- [[26 Epistemic Control and Decision Science/02 Bayesian Updating without False Precision]]
- [[68 Mathematical Econometric and Market Model Monographs/03 MIDAS U-MIDAS Bridge Equations and Forecast Combination]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/04 Probability Bayesian Forecasting and Decision/Probability as a Language of Fundamental Uncertainty]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/04 Probability Bayesian Forecasting and Decision/Base Rates, Reference Classes and Conditional Analogues]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
