---
title: "Uncertainty Taxonomy — Risk, Ambiguity, Ignorance and Model Error"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, epistemology]
---

# Uncertainty Taxonomy — Risk, Ambiguity, Ignorance and Model Error

> [!abstract] Canonical thesis
> Uncertainty is not one number. Sampling error, measurement error, parameter uncertainty, state uncertainty, model uncertainty, ambiguity, structural breaks and unknown unknowns require different responses.

## Beginner intuition

A narrow statistical confidence interval can coexist with huge model uncertainty. You might know precisely what a survey sampled while being unsure whether the survey still measures the relevant economy after a structural change.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Risk | Uncertainty represented by a sufficiently credible probability distribution. |
| Ambiguity | Uncertainty about which distribution or model should be used. |
| Ignorance | Relevant possibilities or mechanisms are not yet recognized or measurable. |
| Parameter uncertainty | Uncertainty about coefficients within a model. |
| State uncertainty | Uncertainty about the current latent condition. |
| Structural uncertainty | Uncertainty about whether relationships and institutions have changed. |

## Mechanism map

1. Classify the source of uncertainty.
2. Avoid collapsing heterogeneous uncertainties into one confidence score.
3. Use sensitivity across parameters, models and definitions.
4. Apply robust or minimax reasoning when probabilities are weak.
5. Maintain explicit unknown and missing-evidence registers.
6. Update the uncertainty taxonomy after surprises.

## Formal structure and notation

### Total predictive variance

$$
Var(Y)=\mathbb E[Var(Y\mid M,\theta)]+Var(\mathbb E[Y\mid M,\theta])
$$

Predictive uncertainty combines within-model noise and uncertainty about models or parameters; the latter is often omitted.

### Robust decision skeleton

$$
a^*=\arg\max_a\min_{P\in\mathcal P}\mathbb E_P[U(a,\theta)]
$$

When several distributions are plausible, robust decision rules evaluate performance across a set rather than a single fitted probability.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Expected-utility approach | Provides coherent choice under a known distribution. | Understates ambiguity and model misspecification. |
| Knightian uncertainty | Distinguishes measurable risk from unmeasurable uncertainty. | Can be hard to operationalize. |
| Robust-control approach | Chooses actions resilient to model error. | Can become excessively conservative and sensitive to the ambiguity set. |

## Historical and institutional cases

### Early pandemic

Epidemiology, policy response, behavioral adaptation and financial transmission were all uncertain; tight historical error bands were misleading.

### Inflation persistence

Uncertainty concerned not just the inflation forecast but the model: supply normalization, wage dynamics, housing lags and policy credibility.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Uncertainty Taxonomy — Risk, Ambiguity, Ignorance and Model Error**; begin with: Classify the source of uncertainty.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Avoid collapsing heterogeneous uncertainties into one confidence score.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Use sensitivity across parameters, models and definitions.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Apply robust or minimax reasoning when probabilities are weak.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Reporting only standard errors.
- Assigning a probability to an event whose definition is unstable.
- Using false precision to make communication appear rigorous.
- Treating model disagreement as noise to average away.
- Failing to distinguish unavailable evidence from genuinely low probability.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Uncertainty Taxonomy — Risk, Ambiguity, Ignorance and Model Error**. The topic-specific sequence is:

1. Classify the source of uncertainty.
2. Avoid collapsing heterogeneous uncertainties into one confidence score.
3. Use sensitivity across parameters, models and definitions.
4. Apply robust or minimax reasoning when probabilities are weak.
5. Maintain explicit unknown and missing-evidence registers.
6. Update the uncertainty taxonomy after surprises.

## Exercises and accreditation questions

1. Create an uncertainty register for a country debt-sustainability assessment.
2. Compare sensitivity analysis, scenario analysis and probability distributions.
3. Identify which uncertainties can be reduced by more data and which require rival models.

## Annotated source canon

- **Frank Knight, Risk, Uncertainty and Profit.** Foundational distinction between measurable risk and uncertainty.
- **Lars Hansen and Thomas Sargent, Robustness.** Decision-making under model misspecification.
- **Nassim Nicholas Taleb, The Black Swan.** Limits of thin-tailed models and retrospective explanation, used critically rather than as a complete framework.

## Related canon

- [[26 Epistemic Control and Decision Science/01 Institutional Epistemology and the Difference Between Facts Models and Decisions]]
- [[00 Core Standards/08 Confidence Calibration and Bayesian Updating]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/02 Epistemology Measurement and Evidence/Time, Publication, Vintage and the Information Set]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/02 Epistemology Measurement and Evidence/Revision, Missingness, Selection and Survivorship Bias]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
