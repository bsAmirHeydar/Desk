---
title: "Horizon Inheritance, Conflict Resolution and Double-Counting Control"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, multihorizon]
---

# Horizon Inheritance, Conflict Resolution and Double-Counting Control

> [!abstract] Canonical thesis
> Multihorizon synthesis requires explicit inheritance rules, conflict types and dependence control. A conclusion is not strengthened merely because correlated indicators repeat the same information at several horizons.

## Beginner intuition

If long-run productivity is strong but current growth is slowing, the answer is not to choose whichever story feels better. You state both, identify which decision horizon matters, and show how the shorter process interacts with the longer constraint.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Inheritance rule | A rule defining which higher-horizon assumptions or constraints enter a lower-horizon conclusion. |
| Horizon conflict | A documented divergence between states, mechanisms or implications at different horizons. |
| Double counting | Assigning multiple evidence weights to indicators that share the same underlying information. |
| Dominance condition | A condition under which one horizon legitimately overrides another for a defined question. |
| Bridge variable | A variable linking slow state to faster observations, such as policy expectations, financing conditions or earnings revisions. |

## Mechanism map

1. Build a dependency graph before scoring evidence.
2. Identify shared sources and latent drivers.
3. Separate prior, likelihood and payoff implications.
4. Classify conflict as timing, mechanism, measurement or valuation conflict.
5. Select dominance rules conditional on mandate and horizon.
6. Lower confidence when conflict cannot be resolved rather than averaging mechanically.

## Formal structure and notation

### Dependence-adjusted evidence

$$
I_{effective}=\mathbf w^\top\Sigma^{-1}\mathbf s
$$

Signals s receive less combined weight when covariance Sigma shows that they carry duplicated information.

### Hierarchical update

$$
p(S^{short}\mid D,S^{long})\propto p(D\mid S^{short},S^{long})p(S^{short}\mid S^{long})
$$

The long-horizon state acts as a prior or constraint, not an automatic short-horizon forecast.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Top-down dominance | Structural and cyclical states constrain all lower conclusions. | Can miss discontinuities and fast policy shifts. |
| Bottom-up aggregation | High-frequency evidence reveals turning points first. | Can overreact to noise and revisions. |
| Hierarchical Bayesian synthesis | Combines horizons through conditional distributions. | Requires careful model specification and dependence estimates. |

## Historical and institutional cases

### Taper tantrum

Stable long-run growth beliefs did not prevent a tactical term-premium and duration repricing.

### Pandemic reopening

Structural digitalization, cyclical recovery, supply constraints and event news produced different implications across assets and horizons.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Horizon Inheritance, Conflict Resolution and Double-Counting Control**; begin with: Build a dependency graph before scoring evidence.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Identify shared sources and latent drivers.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Separate prior, likelihood and payoff implications.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Classify conflict as timing, mechanism, measurement or valuation conflict.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Adding correlated indicators as independent confirmations.
- Resolving conflict by majority vote.
- Letting a slow prior block all evidence of transition.
- Allowing a single event to erase a durable stock constraint.
- Failing to state which horizon the final conclusion serves.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Horizon Inheritance, Conflict Resolution and Double-Counting Control**. The topic-specific sequence is:

1. Build a dependency graph before scoring evidence.
2. Identify shared sources and latent drivers.
3. Separate prior, likelihood and payoff implications.
4. Classify conflict as timing, mechanism, measurement or valuation conflict.
5. Select dominance rules conditional on mandate and horizon.
6. Lower confidence when conflict cannot be resolved rather than averaging mechanically.

## Exercises and accreditation questions

1. Draw a dependency graph for growth indicators.
2. Resolve a structural-bullish/cyclical-bearish case for four mandates.
3. Identify double counting in a dashboard containing PMI, new orders and industrial surveys.

## Annotated source canon

- **Gelman et al., Bayesian Data Analysis.** Hierarchical modeling and partial pooling.
- **Granger and Newbold, Spurious Regressions.** Dependence, persistence and false confirmation.
- **BIS and central-bank cross-asset research.** Examples of common-factor and transmission analysis.

## Related canon

- [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]
- [[27 Macro Regime Ontology and State Machines/03 Structural Cyclical Tactical and Intraday State Separation]]
- [[53 Research Statistics Forecasting and Causal Inference/00 MOC]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Temporal Ontology — Structural, Cyclical, Tactical, Event and Market-Formation Horizons]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Information Half-Life, Shock Decay, Persistence and Thesis Expiry]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
