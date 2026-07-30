---
title: "Causal Questions, Counterfactuals and Identification"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, causality]
---

# Causal Questions, Counterfactuals and Identification

> [!abstract] Canonical thesis
> Causal analysis asks what would differ under a specified intervention or alternative history, not merely which variables move together. Identification is the bridge from an unobserved counterfactual question to evidence under explicit assumptions.

## Analytical intuition

If rates rise when inflation rises, that does not tell you whether inflation caused rates, policy caused both, or a third factor changed them together. A causal question specifies the change of interest and the comparison world.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Causal estimand | The precise effect to be learned: average, local, distributional, dynamic or state-dependent. |
| Counterfactual | The outcome that would have occurred for the same unit or system under an alternative intervention. |
| Identification | Conditions under which the estimand is uniquely linked to the observable distribution. |
| Confounder | A variable affecting both treatment or exposure and outcome. |
| Intervention | A defined change in policy, information, contract or state, distinct from passive observation. |

## Mechanism map

1. Define treatment, outcome, unit and horizon.
2. State the counterfactual comparison.
3. Draw the causal ordering and possible confounders.
4. Choose an identification strategy tied to institutional timing or design.
5. Test observable implications and sensitivity to violated assumptions.
6. Separate identified effects from extrapolation to other regimes or populations.

## Formal structure and notation

### Potential outcomes

$$
\tau_i=Y_i(1)-Y_i(0)
$$

Only one potential outcome is observed for each unit. Research design seeks credible comparisons for the missing counterfactual.

### Average treatment effect

$$
ATE=\mathbb E[Y(1)-Y(0)]
$$

The average effect may hide distributional, state-dependent and local effects relevant to financial systems.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Structural causal modeling | Represents mechanisms and interventions explicitly. | Sensitive to functional form and unobserved structure. |
| Design-based identification | Prioritizes natural experiments and quasi-random variation. | Often identifies local effects in unusual samples. |
| Narrative identification | Uses institutional records and timing to isolate shocks. | Depends on historical interpretation and classification. |

## Historical and institutional cases

### Monetary-policy shock

Observed rate changes are endogenous responses to the economy. Identification separates the unexpected policy component from information the central bank reveals about growth and inflation.

### Fiscal multiplier

Government spending tends to rise in weak conditions. Estimating its effect requires separating policy response from exogenous variation and conditioning on monetary regime and slack.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Causal Questions, Counterfactuals and Identification**; begin with: Define treatment, outcome, unit and horizon.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: State the counterfactual comparison.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Draw the causal ordering and possible confounders.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Choose an identification strategy tied to institutional timing or design.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Using correlation language as causal proof.
- Changing the estimand after seeing results.
- Treating a local natural experiment as universal.
- Ignoring anticipation and delayed effects.
- Failing to distinguish policy action from policy information.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Causal Questions, Counterfactuals and Identification**. The topic-specific sequence is:

1. Define treatment, outcome, unit and horizon.
2. State the counterfactual comparison.
3. Draw the causal ordering and possible confounders.
4. Choose an identification strategy tied to institutional timing or design.
5. Test observable implications and sensitivity to violated assumptions.
6. Separate identified effects from extrapolation to other regimes or populations.

## Adversarial analytical checks and accreditation questions

1. Write three different causal estimands for the effect of policy tightening.
2. Draw confounders in the relationship between credit growth and GDP.
3. Explain why an event-window response is not automatically a causal macro effect.

## Annotated source canon

- **Judea Pearl, Causality.** Structural causal models, interventions and graphical reasoning.
- **Guido Imbens and Donald Rubin, Causal Inference.** Potential outcomes and design-based identification.
- **Angrist and Pischke, Mostly Harmless Econometrics.** Applied identification strategies and limitations.

## Related canon

- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[53 Research Statistics Forecasting and Causal Inference/00 MOC]]

---

Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/03 Causality Identification and Information/Directed Acyclic Graphs and Institutional Causal Maps]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
