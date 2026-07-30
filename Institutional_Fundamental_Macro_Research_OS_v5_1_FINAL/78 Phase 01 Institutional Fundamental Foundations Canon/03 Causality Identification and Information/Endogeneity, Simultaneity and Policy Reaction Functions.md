---
title: "Endogeneity, Simultaneity and Policy Reaction Functions"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, causality]
---

# Endogeneity, Simultaneity and Policy Reaction Functions

> [!abstract] Canonical thesis
> Most macro-financial variables are jointly determined. Policy, prices, credit and expectations respond to the same state and to one another, so observed coefficients usually combine structural response, anticipation and feedback.

## Analytical intuition

Central banks raise rates because inflation is high. If inflation later falls, simply correlating rate increases with inflation can mislead. You must account for why the rate changed and what was already expected.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Endogeneity | Correlation between a regressor and the structural error due to omitted causes, simultaneity, measurement error or selection. |
| Simultaneity | Variables are determined together within the relevant period. |
| Reaction function | A rule or behavior mapping perceived state and objectives into policy or institutional action. |
| Anticipation | Agents adjust before an announced action because they expect it. |
| Information effect | An action or communication reveals information about the institution’s private assessment. |

## Mechanism map

1. Write the institutional reaction function.
2. Measure expected and unexpected components.
3. Separate policy action from information revelation.
4. Use timing, instruments or restrictions tied to decision procedures.
5. Model feedback and delayed transmission.
6. Test whether the identified shock is orthogonal to pre-existing information.

## Formal structure and notation

### Policy rule

$$
i_t=\rho i_{t-1}+\phi_\pi(\pi_t-\pi^*)+\phi_y ygap_t+\nu_t
$$

The residual nu is not automatically an exogenous policy shock; omitted information and real-time measurement matter.

### Simultaneous system

$$
AY_t=BY_{t-1}+\varepsilon_t
$$

Reduced-form residuals are mixtures of structural shocks unless identifying restrictions recover A.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| High-frequency identification | Uses narrow windows around policy announcements. | Can mix policy and information shocks and miss anticipation. |
| Narrative shocks | Classifies decisions from records and stated motives. | Subjective coding and sparse episodes. |
| Structural models | Impose behavioral equations to separate shocks. | Results depend on restrictions and model specification. |

## Historical and institutional cases

### Federal Reserve announcements

Rate surprises and equity responses can reverse sign when announcements convey a stronger economic outlook.

### Foreign-exchange intervention

Authorities intervene in response to currency pressure, so naive regressions can imply intervention causes depreciation.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Endogeneity, Simultaneity and Policy Reaction Functions**; begin with: Write the institutional reaction function.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Measure expected and unexpected components.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Separate policy action from information revelation.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Use timing, instruments or restrictions tied to decision procedures.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Calling a regression residual a structural shock.
- Ignoring the policy institution’s information advantage.
- Using final data to estimate a real-time reaction function.
- Assuming announcement time equals information arrival.
- Failing to model anticipation and forward guidance.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Endogeneity, Simultaneity and Policy Reaction Functions**. The topic-specific sequence is:

1. Write the institutional reaction function.
2. Measure expected and unexpected components.
3. Separate policy action from information revelation.
4. Use timing, instruments or restrictions tied to decision procedures.
5. Model feedback and delayed transmission.
6. Test whether the identified shock is orthogonal to pre-existing information.

## Adversarial analytical checks and accreditation questions

1. Decompose a policy announcement into action, guidance and information components.
2. Propose an instrument for bank lending and defend exclusion.
3. Explain how simultaneity changes interpretation of inflation and wage regressions.

## Annotated source canon

- **Christopher Sims, Macroeconomics and Reality.** Simultaneous systems and VAR critique.
- **Christina and David Romer narrative policy research.** Historical identification of policy shocks.
- **High-frequency monetary-policy identification literature.** Market surprises, information effects and communication.

## Related canon

- [[30 Comparative Central Bank Reaction Functions/00 MOC]]
- [[68 Mathematical Econometric and Market Model Monographs/05 BVAR SVAR Identification and Historical Decomposition]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/03 Causality Identification and Information/Directed Acyclic Graphs and Institutional Causal Maps]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/03 Causality Identification and Information/Natural Experiments, Instruments and Quasi-Experimental Reasoning]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
