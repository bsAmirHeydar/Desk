---
title: "Directed Acyclic Graphs and Institutional Causal Maps"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, causality]
---

# Directed Acyclic Graphs and Institutional Causal Maps

> [!abstract] Canonical thesis
> A causal graph is a disciplined statement of assumed direction, confounding, mediation and selection. In macro-finance it must include institutions, anticipation, policy reaction and balance-sheet feedback rather than a simplistic chain of indicators.

## Analytical intuition

A graph helps you ask whether you should control for a variable. Controlling for the wrong variable can remove part of the mechanism or create a false relationship. The graph makes these choices visible.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Parent and child | Direct assumed cause and effect in the graph. |
| Backdoor path | A non-causal path creating association through common causes. |
| Mediator | A variable through which part of a causal effect operates. |
| Collider | A common effect; conditioning on it can create spurious association. |
| Feedback approximation | A representation of dynamic loops using time-indexed nodes so the graph remains acyclic. |

## Mechanism map

1. Define nodes at explicit times.
2. Include policy rules and expectations as endogenous nodes.
3. Mark observed, latent and selected variables.
4. Identify backdoor paths and prohibited controls.
5. Represent mediation separately from total effects.
6. Use the map to derive data requirements and falsification tests.

## Formal structure and notation

### Factorization

$$
P(X_1,\ldots,X_n)=\prod_i P(X_i\mid Pa_i)
$$

A DAG encodes conditional factorization given the stated parent sets; the graph is an assumption, not a discovery from correlation alone.

### Intervention distribution

$$
P(Y\mid do(X=x))
$$

The do-operator represents an intervention that breaks the ordinary mechanism determining X.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Expert-designed graphs | Use institutional and theoretical knowledge. | Can encode expert bias and omitted variables. |
| Causal discovery | Searches graph structures from statistical independencies. | Strong assumptions and instability limit macro-financial interpretation. |
| System-dynamics loops | Represent feedback naturally. | Harder to map to standard identification criteria without time indexing. |

## Historical and institutional cases

### Bank stress and lending

Capital losses affect lending, but weak borrowers also cause losses, policy backstops respond to stress, and selection into surviving banks matters.

### Inflation expectations

Expectations affect wage and pricing behavior while current inflation affects expectations; a time-indexed map prevents circular verbal reasoning.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Directed Acyclic Graphs and Institutional Causal Maps**; begin with: Define nodes at explicit times.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Include policy rules and expectations as endogenous nodes.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Mark observed, latent and selected variables.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Identify backdoor paths and prohibited controls.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Drawing arrows that mean association rather than cause.
- Controlling for a mediator when estimating total effect.
- Conditioning on market survival or policy response colliders.
- Ignoring anticipation and expectations.
- Using a timeless graph for dynamic feedback.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Directed Acyclic Graphs and Institutional Causal Maps**. The topic-specific sequence is:

1. Define nodes at explicit times.
2. Include policy rules and expectations as endogenous nodes.
3. Mark observed, latent and selected variables.
4. Identify backdoor paths and prohibited controls.
5. Represent mediation separately from total effects.
6. Use the map to derive data requirements and falsification tests.

## Adversarial analytical checks and accreditation questions

1. Draw a time-indexed DAG for a central-bank tightening cycle.
2. Identify colliders in a study of corporate default using only surviving issuers.
3. Create separate graphs for the total and direct effects of fiscal transfers on inflation.

## Annotated source canon

- **Judea Pearl, Causality.** Graphical criteria and interventions.
- **Miguel Hernán and James Robins, Causal Inference: What If.** Time-varying treatments, selection and practical DAG use.
- **Macro-financial network literature.** Dynamic feedback, balance sheets and systemic transmission.

## Related canon

- [[53 Research Statistics Forecasting and Causal Inference/04 Causal Identification Endogeneity and Information Shocks]]
- [[39 Credit Markets Default and Recovery Cycle/00 MOC]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/03 Causality Identification and Information/Causal Questions, Counterfactuals and Identification]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/03 Causality Identification and Information/Endogeneity, Simultaneity and Policy Reaction Functions]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
