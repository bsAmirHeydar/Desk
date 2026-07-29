---
title: "Inflation"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 02-macro-state
  - inflation
  - institutional-fundamental
---
# Inflation

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Inflation**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Inflation analysis separates level, momentum, breadth, persistence, relative-price shocks, margins, wages, rents, and policy-relevant underlying pressure.

For **Inflation**, the relevant institutional domain is **macro**: the economy as linked stocks, flows, prices, quantities, income, financing, and sector balance sheets. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Inflation** represent, in what unit, population, instrument, and convention?
2. Which **Inflation** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Inflation** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Inflation** mechanism is active?
5. What rival model can create the same target move while **Inflation** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Inflation** decision?

## Identities and model skeleton

$$
\pi_{ann,m}=1200\ln(P_t/P_{t-1})
$$

$$
Contribution_i=w_i\Delta \ln P_i
$$

$$
\pi_t^{core}=Trend_t+PersistentBreadth_t+Idiosyncratic_t
$$

For **Inflation**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Inflation:** headline/core and trimmed measures.
- **Measurement 2 for Inflation:** three- and six-month annualized momentum.
- **Measurement 3 for Inflation:** diffusion and contribution breadth.
- **Measurement 4 for Inflation:** shelter, wages, margins, imports, and commodities.
- **Measurement 5 for Inflation:** seasonal factors, weights, revisions, and base effects.

The **Inflation** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Inflation:** bottom-up component nowcast.
- **Model layer 2 for Inflation:** Phillips-curve variants.
- **Model layer 3 for Inflation:** pass-through distributed lags.
- **Model layer 4 for Inflation:** trimmed/winsorized measures.
- **Model layer 5 for Inflation:** density and scenario forecast.

Validate the **Inflation** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Inflation** research object, capacity, demographics, productivity, and institutions determine feasible trends. |
| Cyclical | In the **Inflation** research object, levels, momentum, breadth, and financing determine the business-cycle state. |
| Tactical/Swing | In the **Inflation** research object, forecast revisions and policy repricing drive multi-day campaigns. |
| Daily/Event | In the **Inflation** research object, release composition changes the state estimate; the market trades the gap to expectations. |

Conflicts involving **Inflation** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Inflation channel 1:** test `income and credit → demand`.
2. **Inflation channel 2:** test `demand and constraints → prices and margins`.
3. **Inflation channel 3:** test `policy and financing → activity`.
4. **Inflation channel 4:** test `activity and inflation → rates, earnings, FX, and credit`.

**Inflation asset translation:** Cross-asset: rates normally reveal policy/inflation repricing; FX, credit, equities, and commodities test transmission. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Inflation** posterior or activate a rival explanation.

## Day-trading decision translation

- Identify the new **Inflation** information since the prior close and its source timestamp.
- Reconstruct the priced **Inflation** baseline before reading the target move.
- Name the liquid leader closest to the **Inflation** mechanism and one independent confirmation.
- Compare observed transmission with the **Inflation** event/quiet-day historical distribution.
- Assign a permission and a confidence cap; record the **Inflation** cancellation condition.
- Pass only the permission, leader, invalidation, expiry, and size ceiling to technical execution.

For **Inflation**, fundamentals restrict the allowed trade set; they do not supply the candle trigger or authorize widening a structural stop.

## Two-to-ten-day swing translation

- Define the still-open **Inflation** pricing gap rather than the general narrative.
- Estimate the **Inflation** impulse half-life and its uncertainty by regime.
- Map catalysts capable of confirming, reversing, or exhausting the **Inflation** campaign.
- Compare outright and relative expressions for carry, convexity, gap, liquidity, and factor purity.
- Specify terminal realization, time expiry, and evidence-based invalidation for **Inflation**.

A valid **Inflation** thesis with no residual pricing gap, adverse carry beyond expected payoff, or an imminent dominating catalyst is not a deployable swing.

## Falsification and known failure modes

- **Failure test 1 for Inflation:** annual-rate base effects.
- **Failure test 2 for Inflation:** headline-only interpretation.
- **Failure test 3 for Inflation:** mixing CPI and PCE weights.
- **Failure test 4 for Inflation:** ignoring seasonal-factor revisions.
- **Failure test 5 for Inflation:** assuming one hot print changes persistence.

Score **Inflation** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required implementation record

Create a context object under [[00 Core Standards/17 Context Object and Permission Schema Standard]] containing the **Inflation** target, cutoff, data vintages, model version, state/market distributions, rival models, leader, confirmations, horizon, half-life, permission, confidence cap, size ceiling, invalidation, technical handoff, expiry, and claim IDs.

## Preserved subject-specific foundation

This material survived consolidation because it contains subject-specific instruction for **Inflation**, not the former repeated institutional wrapper.

## What It Is

Inflation is the change in the general price level, but markets care about its source, breadth, persistence, expectations, and policy consequences. Headline, core, goods, services, housing, wages, import prices, producer prices, and inflation expectations are distinct objects.

## Why Markets Care

The market does not trade the variable in isolation. It trades how the variable changes expected policy, cash flows, default risk, risk premia, and relative returns.

## Driver Map

- Demand pressure relative to productive capacity.
- Wage growth relative to productivity.
- Housing rents and measurement lags.
- Energy, food, and commodity prices.
- Supply-chain pressure, shipping, and delivery times.
- Exchange-rate pass-through and import prices.
- Fiscal demand and regulated prices.
- Inflation expectations, indexation, and pricing behavior.
- Margins and firms’ ability to pass through costs.

## Indicator Hierarchy

### Leading and High-Frequency

- Commodity and energy prices.
- Shipping costs and supply-chain pressure indices.
- Rent measures and new-lease data.
- Wage trackers and labor-market tightness.
- Import prices and currency trends.
- Business pricing plans and paid-price surveys.
- Inflation nowcasts.

### Coincident

- CPI and PCE components.
- PPI and import/export prices.
- Average hourly earnings and Employment Cost Index.
- Trimmed-mean, median, and sticky-price measures.

### Lagging or Confirming

- Shelter components with long measurement lags.
- Annual inflation after base effects dominate.
- Long-term contract resets.

### Market-Implied or Financial

- Breakeven inflation and inflation swaps.
- Real yields versus nominal yields.
- Inflation option skew.
- Commodity curve behavior.
- Central-bank pricing.

## Interpretation Framework

For every update, separate:

1. **Level** — where the variable stands.
2. **Momentum** — whether it is improving or deteriorating.
3. **Breadth** — how widely the change is distributed.
4. **Quality** — whether the composition is durable.
5. **Revision risk** — how much history may change.
6. **Expectation gap** — what was already priced.
7. **Policy relevance** — whether the reaction function changes.
8. **Horizon** — when the impact should appear.

## Transmission to Markets

- Higher persistent inflation tends to raise expected policy rates and real yields.
- Higher inflation compensation can lift nominal yields even if real growth is unchanged.
- Inflation can initially support nominal revenues but compress valuation multiples and real incomes.
- Currency response depends on whether the central bank is expected to react credibly.
- Gold response depends on real yields, dollar, credibility, risk, and physical demand—not CPI alone.
- Oil can cause inflation and also respond to growth and supply conditions, creating two-way causality.

## Day-Trading Translation

Before inflation data, define the market’s focus: headline, core, services, shelter, wages, or revisions. The first confirmation is usually the front end of the rates curve. Then decompose nominal-yield movement into real-yield and inflation-compensation components. For Nasdaq, a hot print with higher real yields is more directly adverse than a breakeven-led move with stable real yields. For gold, real yields and the dollar usually matter more intraday than the word “inflation.”

The daily objective is not to forecast the next data print from scratch. It is to know which outcome would force the largest repricing and which cross-asset market should confirm first.

## Short-Swing Translation

A swing inflation thesis requires persistence evidence: breadth, sequential monthly rates, wages/productivity, rent pipeline, supply conditions, and expectations. Track whether the market’s expected policy path is converging toward or diverging from that evidence.

A swing thesis should survive normal intraday noise. It needs a multi-session pricing gap, a catalyst sequence, and a clearly separate overnight invalidation.

## Common Traps

- Comparing year-over-year rates without base effects.
- Treating all inflation as demand-driven.
- Using headline CPI alone.
- Ignoring revisions and seasonal adjustment.
- Assuming gold always rises with inflation.
- Assuming a hot print is currency-positive when policy credibility is weak.
- Failing to distinguish disinflation from outright deflation.
- Overweighting one noisy monthly observation.

## Diagnostic Questions

- Which components produced the surprise?
- Is the monthly pace consistent with the target over time?
- Is inflation broadening or narrowing?
- Are wages outrunning productivity?
- Are expectations anchored?
- Is the central bank more sensitive to inflation or growth now?
- Did real yields, breakevens, or both move?
- Was the surprise already embedded in positioning?

## Primary source routes for Inflation

- [[65 Source Registry and Claim Lineage/BLS_CPI — US BLS — CPI]]
- [[65 Source Registry and Claim Lineage/BLS_PPI — US BLS — PPI]]
- [[65 Source Registry and Claim Lineage/BEA_PCE — US BEA — PCE Price Index]]
- [[65 Source Registry and Claim Lineage/CLE_INFLATION_NOWCAST — Cleveland Fed — Inflation Nowcasting]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Execution Handoff]]
