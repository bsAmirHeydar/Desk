---
title: "Fundamental Information, Expectations, Valuation and Risk Premia"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, ontology]
---

# Fundamental Information, Expectations, Valuation and Risk Premia

> [!abstract] Canonical thesis
> Observed prices jointly reflect expected fundamentals, discounting, risk premia, liquidity services, institutional constraints and positioning. Price-implied information must therefore be decomposed rather than treated as a direct forecast.

## Beginner intuition

A bond yield is not only the market’s forecast of future policy rates. It can also include term premium, inflation compensation, liquidity and balance-sheet effects. An equity multiple is not only a growth forecast. It also reflects discount rates, uncertainty, profitability and market structure.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Expected fundamental | A probability-weighted forecast of cash flows, default, scarcity, inflation or policy-relevant state. |
| Discount rate | The required compensation for time, risk, inflation and constraints. |
| Risk premium | Expected return above a benchmark required for bearing systematic or state-contingent risk. |
| Liquidity premium | Value or cost associated with ease of transaction, funding and collateral use. |
| Priced distribution | The distribution or moments inferred from prices under a model, not necessarily the physical probability distribution. |

## Mechanism map

1. Define the payoff being valued.
2. Separate cash-flow expectations from discounting.
3. Identify embedded optionality and non-cash-flow services.
4. Infer expectations from multiple instruments rather than a single price.
5. Compare survey, model and market-implied distributions.
6. Attribute residual differences to risk premia, constraints or model error with humility.

## Formal structure and notation

### Expected return decomposition

$$
\mathbb{E}_t[R_{t+1}]=R_{f,t}+\pi_t^{risk}+\pi_t^{liq}+\pi_t^{other}
$$

Expected returns combine the risk-free benchmark and compensation for systematic risk, liquidity and other priced services or constraints.

### Nominal yield decomposition

$$
y_t^{(n)}=\frac{1}{n}\sum_{j=1}^{n}\mathbb{E}_t[i_{t+j}]+TP_t^{(n)}+LP_t^{(n)}
$$

A maturity yield is not a pure policy forecast. Term and liquidity premia can move independently.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Efficient-markets interpretation | Prices aggregate dispersed information quickly. | Information aggregation can be distorted by limits to arbitrage and heterogeneous mandates. |
| Behavioral interpretation | Bias and extrapolation create predictable expectation errors. | Behavioral labels can be applied too loosely without a measurable benchmark. |
| Intermediary-constraint interpretation | Dealer and investor balance sheets affect risk premia and liquidity. | Constraint proxies can be endogenous and hard to observe. |

## Historical and institutional cases

### Taper tantrum

Long yields rose as policy expectations, term premium, duration supply and positioning interacted. A one-factor interpretation was inadequate.

### High-growth equity repricing

Expected cash flows can improve while valuation falls if real discount rates or risk premia rise more quickly.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Fundamental Information, Expectations, Valuation and Risk Premia**; begin with: Define the payoff being valued.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Separate cash-flow expectations from discounting.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Identify embedded optionality and non-cash-flow services.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Infer expectations from multiple instruments rather than a single price.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Equating option-implied probability with objective probability.
- Calling every unexplained price move a risk-premium change.
- Ignoring embedded leverage, convexity or collateral value.
- Using one instrument to infer a multidimensional expectation.
- Treating price as truth while simultaneously claiming systematic mispricing.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Fundamental Information, Expectations, Valuation and Risk Premia**. The topic-specific sequence is:

1. Define the payoff being valued.
2. Separate cash-flow expectations from discounting.
3. Identify embedded optionality and non-cash-flow services.
4. Infer expectations from multiple instruments rather than a single price.
5. Compare survey, model and market-implied distributions.
6. Attribute residual differences to risk premia, constraints or model error with humility.

## Exercises and accreditation questions

1. Decompose a ten-year yield into expected short rates and premia conceptually.
2. List at least five reasons an equity multiple can change with unchanged earnings forecasts.
3. Compare survey and market-implied probabilities for a policy event and explain the wedge.

## Annotated source canon

- **John Cochrane, Asset Pricing.** Stochastic discount factors, risk premia and valuation identities.
- **Antti Ilmanen, Expected Returns.** Cross-asset expected-return decomposition and empirical premia.
- **Federal Reserve term-premium research.** Institutional decomposition of yields into expected rates and term premium.

## Related canon

- [[03 Market Pricing/00 Market Pricing MOC]]
- [[16 Rates Fixed Income and Policy Pricing/00 MOC]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/01 Fundamental Science and Ontology/Stocks, Flows, Rates, Levels and Changes]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/01 Fundamental Science and Ontology/Fundamental Analysis Across Instruments, Sectors and Countries]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
