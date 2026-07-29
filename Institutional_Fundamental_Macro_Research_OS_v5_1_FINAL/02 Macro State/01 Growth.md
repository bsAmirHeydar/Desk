---
title: "Growth"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 02-macro-state
  - growth
  - institutional-fundamental
---
# Growth

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Growth**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Growth analysis decomposes real final demand, inventories, trade, government, income, production, and sector breadth across release vintages.

For **Growth**, the relevant institutional domain is **macro**: the economy as linked stocks, flows, prices, quantities, income, financing, and sector balance sheets. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Growth** represent, in what unit, population, instrument, and convention?
2. Which **Growth** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Growth** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Growth** mechanism is active?
5. What rival model can create the same target move while **Growth** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Growth** decision?

## Identities and model skeleton

$$
GDP=C+I+G+X-M
$$

$$
FinalSales=GDP-\Delta Inventories
$$

$$
NominalGrowth\approx RealGrowth+Inflation
$$

For **Growth**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Growth:** real final sales and domestic demand.
- **Measurement 2 for Growth:** consumption income and saving.
- **Measurement 3 for Growth:** business investment and orders.
- **Measurement 4 for Growth:** inventories and net exports.
- **Measurement 5 for Growth:** production, services, housing, and diffusion.

The **Growth** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Growth:** expenditure and income bridges.
- **Model layer 2 for Growth:** nowcast contribution accounting.
- **Model layer 3 for Growth:** survey-hard-data reconciliation.
- **Model layer 4 for Growth:** leading/coincident diffusion.
- **Model layer 5 for Growth:** recession hazard model.

Validate the **Growth** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Growth** research object, capacity, demographics, productivity, and institutions determine feasible trends. |
| Cyclical | In the **Growth** research object, levels, momentum, breadth, and financing determine the business-cycle state. |
| Tactical/Swing | In the **Growth** research object, forecast revisions and policy repricing drive multi-day campaigns. |
| Daily/Event | In the **Growth** research object, release composition changes the state estimate; the market trades the gap to expectations. |

Conflicts involving **Growth** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Growth channel 1:** test `income and credit → demand`.
2. **Growth channel 2:** test `demand and constraints → prices and margins`.
3. **Growth channel 3:** test `policy and financing → activity`.
4. **Growth channel 4:** test `activity and inflation → rates, earnings, FX, and credit`.

**Growth asset translation:** Cross-asset: rates normally reveal policy/inflation repricing; FX, credit, equities, and commodities test transmission. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Growth** posterior or activate a rival explanation.

## Day-trading decision translation

- Identify the new **Growth** information since the prior close and its source timestamp.
- Reconstruct the priced **Growth** baseline before reading the target move.
- Name the liquid leader closest to the **Growth** mechanism and one independent confirmation.
- Compare observed transmission with the **Growth** event/quiet-day historical distribution.
- Assign a permission and a confidence cap; record the **Growth** cancellation condition.
- Pass only the permission, leader, invalidation, expiry, and size ceiling to technical execution.

For **Growth**, fundamentals restrict the allowed trade set; they do not supply the candle trigger or authorize widening a structural stop.

## Two-to-ten-day swing translation

- Define the still-open **Growth** pricing gap rather than the general narrative.
- Estimate the **Growth** impulse half-life and its uncertainty by regime.
- Map catalysts capable of confirming, reversing, or exhausting the **Growth** campaign.
- Compare outright and relative expressions for carry, convexity, gap, liquidity, and factor purity.
- Specify terminal realization, time expiry, and evidence-based invalidation for **Growth**.

A valid **Growth** thesis with no residual pricing gap, adverse carry beyond expected payoff, or an imminent dominating catalyst is not a deployable swing.

## Falsification and known failure modes

- **Failure test 1 for Growth:** trading headline GDP without composition.
- **Failure test 2 for Growth:** treating inventories as durable demand.
- **Failure test 3 for Growth:** ignoring real versus nominal.
- **Failure test 4 for Growth:** mixing monthly and quarterly annualization.
- **Failure test 5 for Growth:** using revised history in live tests.

Score **Growth** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required implementation record

Create a context object under [[00 Core Standards/17 Context Object and Permission Schema Standard]] containing the **Growth** target, cutoff, data vintages, model version, state/market distributions, rival models, leader, confirmations, horizon, half-life, permission, confidence cap, size ceiling, invalidation, technical handoff, expiry, and claim IDs.

## Preserved subject-specific foundation

This material survived consolidation because it contains subject-specific instruction for **Growth**, not the former repeated institutional wrapper.

## What It Is

Growth is the rate and composition of expansion in real economic activity. For trading, the important objects are not only GDP but the trajectory of demand, production, income, consumption, investment, inventories, trade, and corporate revenue.

## Why Markets Care

The market does not trade the variable in isolation. It trades how the variable changes expected policy, cash flows, default risk, risk premia, and relative returns.

## Driver Map

- Real household income, consumption, and savings behavior.
- Business investment, orders, capital expenditure, and inventory plans.
- Housing activity and interest-sensitive demand.
- Government demand and fiscal transfers.
- Net exports and external demand.
- Credit availability and debt-service burden.
- Productivity, labor supply, and capacity utilization.
- Confidence and uncertainty, especially when they change hiring or spending.

## Indicator Hierarchy

### Leading and High-Frequency

- New orders and order-to-inventory ratios.
- PMI/ISM new orders, supplier deliveries, and employment components.
- Building permits, mortgage applications, and housing affordability.
- Initial jobless claims and temporary-help employment.
- OECD Composite Leading Indicators.
- Financial conditions, yield curve, credit spreads, and bank lending standards.

### Coincident

- Industrial production and capacity utilization.
- Retail sales and real consumption.
- Personal income and aggregate hours worked.
- Business sales, shipments, and trade volumes.
- Atlanta Fed GDPNow or equivalent nowcasts.

### Lagging or Confirming

- Quarterly GDP and revisions.
- Unemployment rate after the cycle turns.
- Corporate defaults and loan losses.
- Final productivity and income revisions.

### Market-Implied or Financial

- Cyclical versus defensive equity performance.
- Oil and industrial commodity demand signals.
- Credit-spread behavior.
- Curve steepening or flattening decomposition.
- Earnings revision breadth.

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

- Stronger growth can lift expected earnings and commodity demand.
- Stronger growth can also lift expected rates and real yields, hurting duration assets.
- Weaker growth can support bonds through easing expectations but damage equities through cash flows and credit.
- Growth differentials influence FX through relative policy and capital flows.
- Growth shocks alter oil more directly than gold, while gold depends on the associated rates, dollar, and risk response.

## Day-Trading Translation

Classify the day as **growth-positive**, **growth-negative**, or **growth-ambiguous**. Then ask whether the market is in a growth-sensitive or inflation-sensitive regime. Watch the two-year yield, credit, oil, cyclicals, small caps, and equity breadth. A growth-positive release with rising yields but stable credit may help broad equities while pressuring Nasdaq duration. A growth-negative release with falling yields and widening credit is not a clean equity-long signal.

The daily objective is not to forecast the next data print from scratch. It is to know which outcome would force the largest repricing and which cross-asset market should confirm first.

## Short-Swing Translation

For a two-to-ten-day position, focus on a sequence: surprise trend, nowcast revisions, earnings revisions, credit behavior, and policy repricing. One release rarely creates a durable growth thesis unless it changes a central narrative or crosses a policy threshold.

A swing thesis should survive normal intraday noise. It needs a multi-session pricing gap, a catalyst sequence, and a clearly separate overnight invalidation.

## Common Traps

- Using nominal data without adjusting for inflation.
- Treating GDP as timely when it is backward-looking and revised.
- Confusing inventory accumulation with final demand.
- Reading soft surveys without checking hard data.
- Assuming weak data is bullish because it implies cuts.
- Ignoring per-capita or real-income dynamics.
- Using one country’s growth level instead of relative growth for FX.

## Diagnostic Questions

- Is growth above or below trend, and is momentum changing?
- Which component—consumption, investment, housing, government, or trade—is driving the change?
- Is the surprise broad or concentrated?
- Are earnings revisions confirming the macro signal?
- Are credit spreads calm or signaling stress?
- Does the data change the policy path more than the cash-flow path?
- What is the market already pricing about recession or reacceleration?

## Primary source routes for Growth

- [[65 Source Registry and Claim Lineage/BEA_GDP — US BEA — GDP]]
- [[65 Source Registry and Claim Lineage/BEA_NIPA — US BEA — NIPA Handbook]]
- [[65 Source Registry and Claim Lineage/CENSUS_RETAIL — US Census — Retail Trade]]
- [[65 Source Registry and Claim Lineage/CENSUS_M3 — US Census — M3]]
- [[65 Source Registry and Claim Lineage/ATL_GDPNOW — Atlanta Fed — GDPNow]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Execution Handoff]]
