---
title: "Logs, Compounding, Index Numbers and Growth Decomposition"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, mathematics]
---

# Logs, Compounding, Index Numbers and Growth Decomposition

> [!abstract] Canonical thesis
> Compounding, logarithms and index-number conventions are foundational to interpreting growth, inflation, returns and cumulative change. Approximation error and base effects must be explicit.

## Analytical intuition

Ten percent up and ten percent down do not return you to the starting point. Monthly changes cannot simply be added unless you use a suitable log approximation or exact compounding.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Simple return | Change divided by initial value. |
| Log return | Logarithm of the gross return, additive across periods. |
| Annualization | Conversion of a periodic rate to an annual convention. |
| Index number | Constructed measure of relative change across items or time. |
| Base effect | Influence of the comparison period on measured growth. |

## Mechanism map

1. Choose simple or log changes by purpose.
2. Compound consistently across periods.
3. Separate contribution from weight and component change.
4. Document index formula and rebasing.
5. Identify base effects and carry-over.
6. Distinguish annual rate from year-over-year change.

## Formal structure and notation

### Compounding

$$
X_T=X_0\prod_{t=1}^{T}(1+r_t)
$$

Cumulative change is multiplicative.

### Log additivity

$$
\ln(X_T/X_0)=\sum_{t=1}^{T}\ln(1+r_t)
$$

Log changes aggregate exactly across time.

### Weighted contribution

$$
\Delta I\approx\sum_i w_i\Delta p_i
$$

Weights and substitution rules determine index contribution.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Laspeyres index | Uses base-period quantities and is intuitive. | Can overstate cost increases when substitution occurs. |
| Paasche index | Uses current quantities. | Requires current composition and can understate cost. |
| Chain indexes | Adapt weights through time. | Nonadditivity complicates component analysis. |

## Historical and institutional cases

### Inflation base effects

Year-over-year inflation can fall mechanically after a large prior-month increase exits the window.

### Drawdown recovery

A 50 percent loss requires a 100 percent gain to recover because returns compound asymmetrically.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Logs, Compounding, Index Numbers and Growth Decomposition**; begin with: Choose simple or log changes by purpose.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Compound consistently across periods.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Separate contribution from weight and component change.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Document index formula and rebasing.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Adding simple returns across periods.
- Confusing annualized monthly pace with year-over-year inflation.
- Ignoring index reweighting.
- Comparing rebased indexes as levels of welfare.
- Calling a base effect a change in underlying momentum.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Logs, Compounding, Index Numbers and Growth Decomposition**. The topic-specific sequence is:

1. Choose simple or log changes by purpose.
2. Compound consistently across periods.
3. Separate contribution from weight and component change.
4. Document index formula and rebasing.
5. Identify base effects and carry-over.
6. Distinguish annual rate from year-over-year change.

## Adversarial analytical checks and accreditation questions

1. Compound a sequence of monthly changes.
2. Calculate carry-over into annual average growth.
3. Compare Laspeyres and Paasche intuition.

## Annotated source canon

- **Irving Fisher, index-number theory.** Foundations of price and quantity indexes.
- **Statistical-agency price-index manuals.** Practical weighting and quality adjustment.
- **Standard finance mathematics.** Compounding and log returns.

## Related canon

- [[36 Inflation Microstructure and Price Formation/00 36 Inflation Microstructure and Price Formation MOC]]
- [[02 Macro State/02 Inflation]]

---

Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
