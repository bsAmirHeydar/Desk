---
title: "Assumption Registers, Model Cards and the Unknown Ledger"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, research-practice]
---

# Assumption Registers, Model Cards and the Unknown Ledger

> [!abstract] Canonical thesis
> Institutional research distinguishes known inputs, estimated quantities, maintained assumptions, model choices and genuine unknowns. Hidden assumptions create false certainty and untraceable conclusion drift.

## Analytical intuition

A forecast can look precise because its assumptions are invisible. Writing them down—oil price, policy response, elasticity, accounting treatment—shows where the conclusion actually comes from.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Maintained assumption | Condition treated as given for the analysis but not established by the analysis. |
| Model card | Structured description of purpose, theory, inputs, domain, limitations and validation. |
| Unknown ledger | Register of material unresolved quantities or mechanisms. |
| Assumption sensitivity | Change in conclusion when an assumption varies over a defensible range. |
| Model risk | Risk that specification, estimation, implementation or use produces misleading conclusions. |

## Mechanism map

1. List assumptions before synthesis.
2. Classify each as institutional, behavioral, statistical or accounting.
3. Vary high-impact assumptions.
4. Document model domain and non-use cases.
5. Escalate unknowns that dominate the conclusion.
6. Retire conclusions when assumptions cease to hold.

## Formal structure and notation

### Local sensitivity

$$
S_j=\frac{\partial Conclusion}{\partial Assumption_j}
$$

Sensitivity identifies assumptions that require the strongest evidence and monitoring.

### Uncertainty decomposition

$$
Var(Y)=Data+Parameter+Model+Scenario+Unknown
$$

The decomposition is conceptual but prevents all uncertainty from being mislabeled as sampling error.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Single best model | Clarity and consistency. | Understates model uncertainty. |
| Model ensemble | Diversifies specification risk. | Shared omissions and incoherent combinations remain. |
| Robust range analysis | Focuses on conclusions surviving assumptions. | Can become too conservative or broad. |

## Historical and institutional cases

### Debt sustainability

Growth, interest rates, primary balances, currency and contingent liabilities dominate results.

### Commodity balance

Demand elasticity, substitution, inventory quality and unobserved production create large unknowns.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Assumption Registers, Model Cards and the Unknown Ledger**; begin with: List assumptions before synthesis.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Classify each as institutional, behavioral, statistical or accounting.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Vary high-impact assumptions.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Document model domain and non-use cases.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Assumptions scattered only in prose.
- Unknowns converted to point estimates without disclosure.
- Model used outside domain.
- Sensitivity only around convenient parameters.
- Model card describes method but not failure history.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Assumption Registers, Model Cards and the Unknown Ledger**. The topic-specific sequence is:

1. List assumptions before synthesis.
2. Classify each as institutional, behavioral, statistical or accounting.
3. Vary high-impact assumptions.
4. Document model domain and non-use cases.
5. Escalate unknowns that dominate the conclusion.
6. Retire conclusions when assumptions cease to hold.

## Adversarial analytical checks and accreditation questions

1. Create an assumption register for an inflation forecast.
2. Rank unknowns by decision impact.
3. Write a model card for a simple valuation model.

## Annotated source canon

- **Federal Reserve and SR 11-7 model-risk guidance.** Model governance and limitations.
- **NIST uncertainty and model documentation principles.** Transparent measurement and uncertainty.
- **Sensitivity-analysis literature.** Global and local assumption analysis.

## Related canon

- [[00 Core Standards/14 Model Card Standard]]
- [[26 Epistemic Control and Decision Science/01 Institutional Epistemology and the Difference Between Facts Models and Decisions]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/07 Research Practice and Adversarial Validation Laboratory/Claim–Evidence Matrices and Claim-Level Citation Practice]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/07 Research Practice and Adversarial Validation Laboratory/Historical Point-in-Time Case Reconstruction Standard]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
