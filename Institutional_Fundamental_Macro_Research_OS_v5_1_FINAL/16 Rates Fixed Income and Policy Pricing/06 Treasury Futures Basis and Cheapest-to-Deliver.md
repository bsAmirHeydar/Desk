---
title: "Treasury Futures Basis and Cheapest-to-Deliver"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 16-rates-fixed-income-and-policy-pricing
  - treasury-futures-basis-and-cheapest-to-deliver
  - institutional-fundamental
---
# Treasury Futures Basis and Cheapest-to-Deliver

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Treasury Futures Basis and Cheapest-to-Deliver**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Treasury futures delivery economics compare eligible cash bonds after conversion factors, financing, coupon cash flows, delivery options, and hedge ratios. Sovereign-bond analysis combines expected policy, inflation compensation, term premium, fiscal supply, investor base, collateral value, and market liquidity.

For **Treasury Futures Basis and Cheapest-to-Deliver**, the relevant institutional domain is **rates**: the path of policy rates, sovereign cash flows, duration supply, inflation compensation, collateral, funding, and term risk. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Treasury Futures Basis and Cheapest-to-Deliver** represent, in what unit, population, instrument, and convention?
2. Which **Treasury Futures Basis and Cheapest-to-Deliver** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Treasury Futures Basis and Cheapest-to-Deliver** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Treasury Futures Basis and Cheapest-to-Deliver** mechanism is active?
5. What rival model can create the same target move while **Treasury Futures Basis and Cheapest-to-Deliver** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Treasury Futures Basis and Cheapest-to-Deliver** decision?

## Identities and model skeleton

$$
InvoicePrice=FuturesPrice\times CF+AccruedInterest
$$

$$
GrossBasis=CashCleanPrice-FuturesPrice\times CF
$$

$$
NetBasis=GrossBasis-Carry
$$

$$
HR_{DV01}=\frac{DV01_{cash}}{DV01_{futures,CTD}}
$$

$$
y^{(n)}=\overline{E(i)}+TP^{(n)}
$$

$$
Return\approx-Duration\Delta y+\tfrac12Convexity(\Delta y)^2+Carry+Roll
$$

For **Treasury Futures Basis and Cheapest-to-Deliver**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Treasury Futures Basis and Cheapest-to-Deliver:** deliverable basket and conversion factors.
- **Measurement 2 for Treasury Futures Basis and Cheapest-to-Deliver:** cash prices and accrued interest.
- **Measurement 3 for Treasury Futures Basis and Cheapest-to-Deliver:** repo rate and specialness.
- **Measurement 4 for Treasury Futures Basis and Cheapest-to-Deliver:** delivery date and coupon flows.
- **Measurement 5 for Treasury Futures Basis and Cheapest-to-Deliver:** CTD switch probabilities and futures DV01.
- **Measurement 6 for Treasury Futures Basis and Cheapest-to-Deliver:** policy curve.
- **Measurement 7 for Treasury Futures Basis and Cheapest-to-Deliver:** nominal/real/breakeven curves.
- **Measurement 8 for Treasury Futures Basis and Cheapest-to-Deliver:** issuance and duration supply.
- **Measurement 9 for Treasury Futures Basis and Cheapest-to-Deliver:** auction and investor absorption.
- **Measurement 10 for Treasury Futures Basis and Cheapest-to-Deliver:** repo, swap spreads, and volatility.

The **Treasury Futures Basis and Cheapest-to-Deliver** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Treasury Futures Basis and Cheapest-to-Deliver:** implied-repo ranking.
- **Model layer 2 for Treasury Futures Basis and Cheapest-to-Deliver:** net-basis decomposition.
- **Model layer 3 for Treasury Futures Basis and Cheapest-to-Deliver:** delivery-option valuation.
- **Model layer 4 for Treasury Futures Basis and Cheapest-to-Deliver:** DV01-neutral hedge construction.
- **Model layer 5 for Treasury Futures Basis and Cheapest-to-Deliver:** financing and balance-sheet stress scenarios.
- **Model layer 6 for Treasury Futures Basis and Cheapest-to-Deliver:** curve decomposition.
- **Model layer 7 for Treasury Futures Basis and Cheapest-to-Deliver:** debt and issuance scenarios.
- **Model layer 8 for Treasury Futures Basis and Cheapest-to-Deliver:** investor-base flow model.
- **Model layer 9 for Treasury Futures Basis and Cheapest-to-Deliver:** relative-value and carry analysis.
- **Model layer 10 for Treasury Futures Basis and Cheapest-to-Deliver:** liquidity stress.

Validate the **Treasury Futures Basis and Cheapest-to-Deliver** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Treasury Futures Basis and Cheapest-to-Deliver** research object, neutral rate, debt structure, inflation regime, and investor base anchor the curve. |
| Cyclical | In the **Treasury Futures Basis and Cheapest-to-Deliver** research object, policy path, inflation compensation, credit, and term premium evolve. |
| Tactical/Swing | In the **Treasury Futures Basis and Cheapest-to-Deliver** research object, issuance, auctions, positioning, carry, and relative value dominate. |
| Daily/Event | In the **Treasury Futures Basis and Cheapest-to-Deliver** research object, meeting pricing, WI levels, funding, and liquid futures lead the response. |

Conflicts involving **Treasury Futures Basis and Cheapest-to-Deliver** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Treasury Futures Basis and Cheapest-to-Deliver channel 1:** test `data and policy → expected short rates`.
2. **Treasury Futures Basis and Cheapest-to-Deliver channel 2:** test `fiscal supply and risk appetite → term premium`.
3. **Treasury Futures Basis and Cheapest-to-Deliver channel 3:** test `collateral and balance sheet → repo/basis`.
4. **Treasury Futures Basis and Cheapest-to-Deliver channel 4:** test `rates → FX, equity duration, credit, housing, and gold`.

**Treasury Futures Basis and Cheapest-to-Deliver asset translation:** Rates: separate expected short-rate changes, term premium, inflation compensation, carry/roll, and funding. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Treasury Futures Basis and Cheapest-to-Deliver** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Treasury Futures Basis and Cheapest-to-Deliver:** using gross instead of net basis.
- **Failure test 2 for Treasury Futures Basis and Cheapest-to-Deliver:** ignoring special repo.
- **Failure test 3 for Treasury Futures Basis and Cheapest-to-Deliver:** assuming CTD is fixed.
- **Failure test 4 for Treasury Futures Basis and Cheapest-to-Deliver:** wrong accrued interest or delivery date.
- **Failure test 5 for Treasury Futures Basis and Cheapest-to-Deliver:** omitting margin and balance-sheet cost.
- **Failure test 6 for Treasury Futures Basis and Cheapest-to-Deliver:** one-factor yield stories.
- **Failure test 7 for Treasury Futures Basis and Cheapest-to-Deliver:** notional sizing.
- **Failure test 8 for Treasury Futures Basis and Cheapest-to-Deliver:** ignoring currency/fiscal regime.
- **Failure test 9 for Treasury Futures Basis and Cheapest-to-Deliver:** omitting funding.
- **Failure test 10 for Treasury Futures Basis and Cheapest-to-Deliver:** using generic duration for callable/inflation-linked bonds.

Score **Treasury Futures Basis and Cheapest-to-Deliver** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Treasury Futures Basis and Cheapest-to-Deliver

- [[65 Source Registry and Claim Lineage/CME_RATES — CME Interest Rate Products]]
- [[65 Source Registry and Claim Lineage/TREASURY_DIRECT — TreasuryDirect Marketable Securities]]
- [[65 Source Registry and Claim Lineage/NYFED_SOFR — New York Fed — SOFR]]
- [[65 Source Registry and Claim Lineage/DTCC_UST — DTCC Fixed Income Clearing]]
- [[65 Source Registry and Claim Lineage/UST_AUCTIONS — U.S. Treasury Auction Data]]
- [[65 Source Registry and Claim Lineage/UST_REFUNDING — U.S. Treasury Quarterly Refunding]]
- [[65 Source Registry and Claim Lineage/NYFED_TERM_PREMIA — New York Fed — Term Premia]]
- [[65 Source Registry and Claim Lineage/BIS — Bank for International Settlements]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
