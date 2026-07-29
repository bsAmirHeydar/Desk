---
title: "Natural Experiments, Instruments and Quasi-Experimental Reasoning"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, causality]
---

# Natural Experiments, Instruments and Quasi-Experimental Reasoning

> [!abstract] Canonical thesis
> Quasi-experimental methods can strengthen causal inference when institutional rules generate plausibly exogenous variation, but every design depends on narrow assumptions, local populations and careful timing.

## Beginner intuition

Sometimes a rule, threshold, lottery, court decision or administrative boundary changes exposure for some units but not comparable others. This can create a useful comparison—if the rule did not affect outcomes through other channels.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Instrument | A variable that changes treatment, is as-good-as-random conditional on controls, and affects outcome only through that treatment. |
| Regression discontinuity | Comparison around a threshold determining treatment. |
| Difference-in-differences | Comparison of changes across treated and comparison groups under a parallel-trends assumption. |
| Local average treatment effect | Effect for units whose treatment status is changed by the instrument. |
| Exclusion restriction | The instrument has no direct outcome channel outside treatment. |

## Mechanism map

1. Understand the institutional assignment rule.
2. Define treatment timing and eligible population.
3. Test manipulation, pre-trends and balance.
4. Defend exclusion and monotonicity.
5. Estimate local effects with appropriate uncertainty.
6. Limit external extrapolation and discuss equilibrium spillovers.

## Formal structure and notation

### Wald estimand

$$
LATE=\frac{\mathbb E[Y\mid Z=1]-\mathbb E[Y\mid Z=0]}{\mathbb E[D\mid Z=1]-\mathbb E[D\mid Z=0]}
$$

The ratio identifies the effect for compliers under instrument validity and monotonicity, not necessarily the population average.

### Difference-in-differences

$$
\tau=(\bar Y_{T,post}-\bar Y_{T,pre})-(\bar Y_{C,post}-\bar Y_{C,pre})
$$

Interpretation requires credible counterfactual trends, no differential anticipation and careful treatment of staggered adoption.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Credibility revolution | Prioritizes transparent research design over elaborate structural assumptions. | Can favor narrow questions and local effects. |
| Structural extrapolation | Uses economic models to generalize and run counterfactuals. | Model misspecification can dominate. |
| Triangulation | Combines designs and structural reasoning. | Disagreement among estimates requires principled synthesis. |

## Historical and institutional cases

### Bank-capital regulation thresholds

Administrative thresholds can identify effects on lending but may induce balance-sheet manipulation around cutoffs.

### Fiscal transfers across regions

Eligibility rules can identify consumption responses, while migration, spillovers and local price effects complicate aggregation.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Natural Experiments, Instruments and Quasi-Experimental Reasoning**; begin with: Understand the institutional assignment rule.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Define treatment timing and eligible population.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Test manipulation, pre-trends and balance.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Defend exclusion and monotonicity.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Weak instrument.
- Post-treatment controls.
- Differential pre-trends.
- Threshold manipulation.
- Generalizing a local effect to a national equilibrium without justification.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Natural Experiments, Instruments and Quasi-Experimental Reasoning**. The topic-specific sequence is:

1. Understand the institutional assignment rule.
2. Define treatment timing and eligible population.
3. Test manipulation, pre-trends and balance.
4. Defend exclusion and monotonicity.
5. Estimate local effects with appropriate uncertainty.
6. Limit external extrapolation and discuss equilibrium spillovers.

## Exercises and accreditation questions

1. Evaluate a proposed instrument for mortgage credit supply.
2. Design a DiD study for an energy subsidy and list threats.
3. Explain why a valid micro estimate need not equal the macro multiplier.

## Annotated source canon

- **Joshua Angrist and Jörn-Steffen Pischke, Mastering Metrics.** Applied quasi-experimental designs.
- **Guido Imbens and Thomas Lemieux on regression discontinuity.** Identification and implementation.
- **Modern staggered-adoption DiD literature.** Heterogeneous treatment timing and robust estimators.

## Related canon

- [[53 Research Statistics Forecasting and Causal Inference/04 Causal Identification Endogeneity and Information Shocks]]
- [[53 Research Statistics Forecasting and Causal Inference/04 Causal Identification Endogeneity and Information Shocks]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/03 Causality Identification and Information/Endogeneity, Simultaneity and Policy Reaction Functions]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/03 Causality Identification and Information/Mediation, Transmission Chains and Mechanism Evidence]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
