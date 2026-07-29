---
title: "Carry Roll Convexity and Funding Budget"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 49-cross-asset-relative-value-and-trade-expression
  - carry-roll-convexity-and-funding-budget
  - institutional-fundamental
---
# Carry Roll Convexity and Funding Budget

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Carry Roll Convexity and Funding Budget**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Secured funding prices cash, collateral scarcity, counterparty balance sheet, settlement demand, and regulatory capacity. Fixed-income risk must be represented as price sensitivity to localized curve shocks rather than by notional or maturity alone.

For **Carry Roll Convexity and Funding Budget**, the relevant institutional domain is **portfolio**: capital allocation across uncertain scenarios, correlated drivers, liquidity constraints, convex payoffs, and institutional survival limits. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Carry Roll Convexity and Funding Budget** represent, in what unit, population, instrument, and convention?
2. Which **Carry Roll Convexity and Funding Budget** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Carry Roll Convexity and Funding Budget** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Carry Roll Convexity and Funding Budget** mechanism is active?
5. What rival model can create the same target move while **Carry Roll Convexity and Funding Budget** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Carry Roll Convexity and Funding Budget** decision?

## Identities and model skeleton

$$
RepoInterest=CashPrincipal\times RepoRate\times \frac{Days}{360}
$$

$$
Haircut=1-\frac{CashLent}{CollateralMarketValue}
$$

$$
BasisPnL=CashReturn-FuturesHedge-Funding-CapitalCost
$$

$$
DV01=-\frac{\partial P}{\partial y}\times 10^{-4}
$$

$$
\Delta P\approx-DV01\,\Delta y_{bp}+\tfrac12 Convexity\,(\Delta y)^2P
$$

$$
PortfolioDV01=\sum_i q_i DV01_i
$$

For **Carry Roll Convexity and Funding Budget**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Carry Roll Convexity and Funding Budget:** SOFR distribution and volumes.
- **Measurement 2 for Carry Roll Convexity and Funding Budget:** general collateral and specials.
- **Measurement 3 for Carry Roll Convexity and Funding Budget:** haircuts and fails.
- **Measurement 4 for Carry Roll Convexity and Funding Budget:** dealer inventories and Treasury settlement.
- **Measurement 5 for Carry Roll Convexity and Funding Budget:** sponsored repo and balance-sheet dates.
- **Measurement 6 for Carry Roll Convexity and Funding Budget:** cash flows and yield convention.
- **Measurement 7 for Carry Roll Convexity and Funding Budget:** modified and effective duration.
- **Measurement 8 for Carry Roll Convexity and Funding Budget:** key-rate durations.
- **Measurement 9 for Carry Roll Convexity and Funding Budget:** convexity and embedded options.
- **Measurement 10 for Carry Roll Convexity and Funding Budget:** carry, roll, financing, and hedge basis.

The **Carry Roll Convexity and Funding Budget** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Carry Roll Convexity and Funding Budget:** funding-spread decomposition.
- **Model layer 2 for Carry Roll Convexity and Funding Budget:** collateral-specialness map.
- **Model layer 3 for Carry Roll Convexity and Funding Budget:** settlement-flow forecast.
- **Model layer 4 for Carry Roll Convexity and Funding Budget:** basis stress test.
- **Model layer 5 for Carry Roll Convexity and Funding Budget:** liquidity ladder.
- **Model layer 6 for Carry Roll Convexity and Funding Budget:** cash-flow discounting.
- **Model layer 7 for Carry Roll Convexity and Funding Budget:** key-rate decomposition.
- **Model layer 8 for Carry Roll Convexity and Funding Budget:** scenario P&L.
- **Model layer 9 for Carry Roll Convexity and Funding Budget:** option-adjusted risk.
- **Model layer 10 for Carry Roll Convexity and Funding Budget:** DV01-neutral relative value.

Validate the **Carry Roll Convexity and Funding Budget** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Strategic | In the **Carry Roll Convexity and Funding Budget** research object, mandate, risk tolerance, capital base, and liabilities constrain allocation. |
| Cyclical | In the **Carry Roll Convexity and Funding Budget** research object, factor correlations, vol, liquidity, and opportunity set change. |
| Tactical/Swing | In the **Carry Roll Convexity and Funding Budget** research object, scenario concentration, carry, convexity, and hedging determine expression. |
| Daily/Event | In the **Carry Roll Convexity and Funding Budget** research object, gap, margin, execution capacity, and kill switches govern survival. |

Conflicts involving **Carry Roll Convexity and Funding Budget** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Carry Roll Convexity and Funding Budget channel 1:** test `research confidence → risk budget`.
2. **Carry Roll Convexity and Funding Budget channel 2:** test `portfolio interactions → effective exposure`.
3. **Carry Roll Convexity and Funding Budget channel 3:** test `volatility/liquidity → size and exits`.
4. **Carry Roll Convexity and Funding Budget channel 4:** test `loss/attribution → limits and model retirement`.

**Carry Roll Convexity and Funding Budget asset translation:** Portfolio: map the view to shared drivers and scenario losses before adding notional. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Carry Roll Convexity and Funding Budget** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Carry Roll Convexity and Funding Budget:** treating SOFR as one frictionless rate.
- **Failure test 2 for Carry Roll Convexity and Funding Budget:** ignoring collateral identity.
- **Failure test 3 for Carry Roll Convexity and Funding Budget:** omitting haircut and margin liquidity.
- **Failure test 4 for Carry Roll Convexity and Funding Budget:** using overnight funding for term exposure.
- **Failure test 5 for Carry Roll Convexity and Funding Budget:** missing quarter-end balance-sheet effects.
- **Failure test 6 for Carry Roll Convexity and Funding Budget:** sizing by notional.
- **Failure test 7 for Carry Roll Convexity and Funding Budget:** mixing price value and yield sensitivity.
- **Failure test 8 for Carry Roll Convexity and Funding Budget:** linearizing large shocks.
- **Failure test 9 for Carry Roll Convexity and Funding Budget:** ignoring option convexity.
- **Failure test 10 for Carry Roll Convexity and Funding Budget:** hedging one point while retaining curve risk.

Score **Carry Roll Convexity and Funding Budget** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Carry Roll Convexity and Funding Budget

- [[65 Source Registry and Claim Lineage/NYFED_SOFR — New York Fed — SOFR]]
- [[65 Source Registry and Claim Lineage/NYFED_DEALERS — New York Fed — Primary Dealer Statistics]]
- [[65 Source Registry and Claim Lineage/DTCC_UST — DTCC Fixed Income Clearing]]
- [[65 Source Registry and Claim Lineage/UST_AUCTIONS — U.S. Treasury Auction Data]]
- [[65 Source Registry and Claim Lineage/CME_RATES — CME Interest Rate Products]]
- [[65 Source Registry and Claim Lineage/TREASURY_DIRECT — TreasuryDirect Marketable Securities]]
- [[65 Source Registry and Claim Lineage/BOE_YIELD_CURVES — Bank of England Yield Curves]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
