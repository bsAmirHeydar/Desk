---
title: "Mandates, Utility, Constraints and the Institutional Decision Object"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, decision]
---

# Mandates, Utility, Constraints and the Institutional Decision Object

> [!abstract] Canonical thesis
> A fundamental conclusion becomes decision-relevant only after the mandate, liabilities, horizon, liquidity, legal constraints, tolerance for uncertainty and opportunity set are specified. There is no mandate-free “best” conclusion.

## Analytical intuition

The same economic outlook can be favorable for a long-horizon pension fund, unsuitable for a leveraged fund and irrelevant to a reserve manager. The facts may match while the decision differs.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Mandate | Authorized objective, instruments, risk limits, benchmark and horizon. |
| Decision object | The precise action-independent question being evaluated: valuation, exposure, allocation, hedge, funding or monitoring. |
| Utility or loss | Formal or qualitative representation of valued outcomes and penalties. |
| Constraint | Legal, liquidity, leverage, concentration, liability or governance boundary. |
| Opportunity cost | Value of the best feasible alternative forgone. |

## Mechanism map

1. Define the research conclusion before any action language.
2. Specify mandate and liability structure.
3. Translate scenarios into payoff distributions relevant to the mandate.
4. Apply constraints and liquidity considerations.
5. Compare alternatives and no-deployment.
6. Document how the conclusion changes under a different mandate.

## Formal structure and notation

### Constrained decision

$$
a^*=\arg\max_{a\in\mathcal A(C)}\mathbb E[U(W(a,S))]
$$

Actions are selected from a constraint-dependent feasible set; research supplies state and payoff distributions, not mandate-free certainty.

### Loss-sensitive forecast value

$$
Value(F)=\mathbb E[L(a_0,Y)-L(a_F,Y)]
$$

A forecast is useful when it improves decisions relative to a benchmark under the relevant loss function.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Universal valuation | Economic value can be estimated independently of holder. | Funding, taxes, regulation and liabilities affect realized value. |
| Mandate-relative value | Value depends on holder constraints and alternatives. | Can obscure common cash-flow anchors. |
| Robust no-deployment option | Abstention preserves capital under uncertainty. | Excessive abstention can create opportunity loss. |

## Historical and institutional cases

### Bank versus pension ownership of duration

Capital rules, deposit behavior and liabilities change the meaning of the same bond.

### Commodity producer hedge

A futures position can reduce business risk even when its standalone expected return is unattractive.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Mandates, Utility, Constraints and the Institutional Decision Object**; begin with: Define the research conclusion before any action language.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Specify mandate and liability structure.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Translate scenarios into payoff distributions relevant to the mandate.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Apply constraints and liquidity considerations.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Reporting a conclusion without its mandate.
- Treating benchmark-relative and absolute objectives as identical.
- Ignoring liabilities and funding.
- Converting uncertainty into directional confidence.
- Failing to compare no-deployment and alternative expressions.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Mandates, Utility, Constraints and the Institutional Decision Object**. The topic-specific sequence is:

1. Define the research conclusion before any action language.
2. Specify mandate and liability structure.
3. Translate scenarios into payoff distributions relevant to the mandate.
4. Apply constraints and liquidity considerations.
5. Compare alternatives and no-deployment.
6. Document how the conclusion changes under a different mandate.

## Adversarial analytical checks and accreditation questions

1. Write the same fundamental state for a reserve manager, pension fund and macro fund.
2. Define decision objects for valuation, hedge and monitoring.
3. Construct a loss function where calibration matters more than hit rate.

## Annotated source canon

- **Arrow and Debreu, decision under uncertainty foundations.** States, contingent claims and preferences.
- **Markowitz, portfolio selection.** Risk-return choice under constraints.
- **Institutional investment-policy statements.** Real mandates, benchmarks and governance constraints.

## Related canon

- [[22 Portfolio Construction Risk and Governance/00 MOC]]
- [[51 Portfolio Construction Factor Risk and Capital Allocation/00 MOC]]
- [[00 Core Standards/01 Research Object and Decision Contract]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Scenario Trees, Tail Asymmetry and Conditional Fundamental Conclusions]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Fundamental Conclusion Taxonomy, Confidence, Invalidation and Expiry]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
