---
title: "Decision Theory, Utility, Loss and Mandate Dependence"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, probability]
---

# Decision Theory, Utility, Loss and Mandate Dependence

> [!abstract] Canonical thesis
> Beliefs do not uniquely determine decisions. Institutional conclusions depend on utility, loss asymmetry, constraints, liquidity, horizon and mandate. Research must separate probability assessment from the decision rule.

## Analytical intuition

Two investors can agree on probabilities but act differently because one cannot tolerate a large loss, another has liabilities, and a third values liquidity. A forecast is not a decision until objectives and constraints are defined.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Utility | Representation of preferences over outcomes. |
| Loss function | Cost assigned to forecast or decision errors. |
| Risk aversion | Preference over uncertainty beyond expected payoff. |
| Constraint | Legal, liquidity, capital, liability, concentration or governance limit. |
| Value of information | Expected improvement in decision quality from additional information. |

## Mechanism map

1. Estimate the outcome distribution independently.
2. Specify mandate and loss asymmetry.
3. Add constraints and implementation frictions.
4. Compare actions across scenarios and model sets.
5. Measure value of additional information and delay.
6. Document why the conclusion follows from both beliefs and mandate.

## Formal structure and notation

### Expected utility

$$
a^*=\arg\max_a\sum_s p_s U(W(a,s))
$$

The optimal action depends on both probabilities and utility over state-contingent wealth or institutional outcomes.

### Expected value of perfect information

$$
EVPI=\mathbb E[\max_a U(a,\theta)]-\max_a\mathbb E[U(a,\theta)]
$$

EVPI bounds what perfect resolution of uncertainty could be worth; real research has partial information and cost.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Expected utility | Coherent benchmark for risk-based choice. | Observed behavior and institutional objectives may violate its assumptions. |
| Prospect theory | Captures reference dependence and loss aversion. | Parameters and reference points can be unstable. |
| Robust and satisficing rules | Prioritize survival and acceptable outcomes under ambiguity. | May sacrifice expected performance and complicate optimization. |

## Historical and institutional cases

### Pension fund

Duration and inflation exposure are evaluated relative to liabilities, not stand-alone return forecasts.

### Central bank

Forecast probabilities are filtered through asymmetric social losses from inflation, unemployment and financial instability.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Decision Theory, Utility, Loss and Mandate Dependence**; begin with: Estimate the outcome distribution independently.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Specify mandate and loss asymmetry.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Add constraints and implementation frictions.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Compare actions across scenarios and model sets.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Embedding preferences inside probability estimates.
- Comparing decisions with different mandates as if one is irrational.
- Ignoring liquidity and path-dependent constraints.
- Using expected value when tail loss threatens survival.
- Collecting information whose value is below its delay and attention cost.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Decision Theory, Utility, Loss and Mandate Dependence**. The topic-specific sequence is:

1. Estimate the outcome distribution independently.
2. Specify mandate and loss asymmetry.
3. Add constraints and implementation frictions.
4. Compare actions across scenarios and model sets.
5. Measure value of additional information and delay.
6. Document why the conclusion follows from both beliefs and mandate.

## Adversarial analytical checks and accreditation questions

1. Use the same distribution to derive decisions for a bank, pension fund and unlevered allocator.
2. Calculate a simple value-of-information example.
3. Write a loss matrix for inflation forecast errors.

## Annotated source canon

- **von Neumann and Morgenstern, Theory of Games and Economic Behavior.** Expected utility foundations.
- **Kahneman and Tversky, Prospect Theory.** Reference dependence and asymmetric loss.
- **Howard Raiffa, Decision Analysis.** Decision trees, information value and institutional choice.

## Related canon

- [[22 Portfolio Construction Risk and Governance/00 MOC]]
- [[50 Scenario Intelligence Wargaming and Tail Systems/00 MOC]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/04 Probability Bayesian Forecasting and Decision/Forecast Evaluation, Calibration and Proper Scoring Rules]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/04 Probability Bayesian Forecasting and Decision/Ambiguity, Robustness and Precautionary Conclusions]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
