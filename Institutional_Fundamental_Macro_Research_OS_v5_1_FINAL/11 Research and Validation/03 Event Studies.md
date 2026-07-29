---
title: "Event Studies"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 11-research-and-validation
  - event-studies
  - institutional-fundamental
---
# Event Studies

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Event Studies**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

**Event Studies** is a research object inside point-in-time measurement, forecasting, causal inference, model validation, data lineage, and research deployment. The analyst must isolate the measurable state, the expectation already embedded in prices, the mechanism connecting them, and the horizon on which that inference can survive.

For **Event Studies**, the relevant institutional domain is **nowcast**: point-in-time measurement, forecasting, causal inference, model validation, data lineage, and research deployment. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Event Studies** represent, in what unit, population, instrument, and convention?
2. Which **Event Studies** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Event Studies** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Event Studies** mechanism is active?
5. What rival model can create the same target move while **Event Studies** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Event Studies** decision?

## Identities and model skeleton

$$
\widehat y_{t|t^-}=f(\mathcal I_{t^-})
$$

$$
OOSLoss=\frac1N\sum_t L(y_t,\widehat y_{t|t^-})
$$

$$
Feature_t=g(\{x_s^{(v)}:release(s,v)\le t\})
$$

For **Event Studies**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Event Studies:** release and vintage timestamps.
- **Measurement 2 for Event Studies:** feature availability and missingness.
- **Measurement 3 for Event Studies:** forecast errors and revisions.
- **Measurement 4 for Event Studies:** probability calibration.
- **Measurement 5 for Event Studies:** drift, stability, cost, and implementation diagnostics.

The **Event Studies** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Event Studies:** state-space models.
- **Model layer 2 for Event Studies:** MIDAS and bridge equations.
- **Model layer 3 for Event Studies:** Bayesian VARs and local projections.
- **Model layer 4 for Event Studies:** panel and quasi-experimental methods.
- **Model layer 5 for Event Studies:** walk-forward and pseudo-real-time validation.

Validate the **Event Studies** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Event Studies** research object, methodology and data-generating process define model validity. |
| Cyclical | In the **Event Studies** research object, state estimates integrate asynchronous releases and revisions. |
| Tactical/Swing | In the **Event Studies** research object, forecast changes and confidence bands determine catalysts. |
| Daily/Event | In the **Event Studies** research object, only information available at the timestamp may update the estimate. |

Conflicts involving **Event Studies** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Event Studies channel 1:** test `raw release → vintage-controlled feature`.
2. **Event Studies channel 2:** test `feature → state or forecast distribution`.
3. **Event Studies channel 3:** test `distribution → pricing-gap estimate`.
4. **Event Studies channel 4:** test `estimate → permission tested against a baseline`.

**Event Studies asset translation:** Research: compare every model with simple real-time benchmarks and store the full forecast vintage. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Event Studies** posterior or activate a rival explanation.

## Day-trading decision translation

- Identify the new **Event Studies** information since the prior close and its source timestamp.
- Reconstruct the priced **Event Studies** baseline before reading the target move.
- Name the liquid leader closest to the **Event Studies** mechanism and one independent confirmation.
- Compare observed transmission with the **Event Studies** event/quiet-day historical distribution.
- Assign a permission and a confidence cap; record the **Event Studies** cancellation condition.
- Pass only the permission, leader, invalidation, expiry, and size ceiling to technical execution.

For **Event Studies**, fundamentals restrict the allowed trade set; they do not supply the candle trigger or authorize widening a structural stop.

## Two-to-ten-day swing translation

- Define the still-open **Event Studies** pricing gap rather than the general narrative.
- Estimate the **Event Studies** impulse half-life and its uncertainty by regime.
- Map catalysts capable of confirming, reversing, or exhausting the **Event Studies** campaign.
- Compare outright and relative expressions for carry, convexity, gap, liquidity, and factor purity.
- Specify terminal realization, time expiry, and evidence-based invalidation for **Event Studies**.

A valid **Event Studies** thesis with no residual pricing gap, adverse carry beyond expected payoff, or an imminent dominating catalyst is not a deployable swing.

## Falsification and known failure modes

- **Failure test 1 for Event Studies:** lookahead and revision leakage.
- **Failure test 2 for Event Studies:** target leakage.
- **Failure test 3 for Event Studies:** multiple testing.
- **Failure test 4 for Event Studies:** unstable transformations.
- **Failure test 5 for Event Studies:** production data differing from research data.

Score **Event Studies** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required implementation record

Create a context object under [[00 Core Standards/17 Context Object and Permission Schema Standard]] containing the **Event Studies** target, cutoff, data vintages, model version, state/market distributions, rival models, leader, confirmations, horizon, half-life, permission, confidence cap, size ceiling, invalidation, technical handoff, expiry, and claim IDs.

## Preserved subject-specific foundation

This material survived consolidation because it contains subject-specific instruction for **Event Studies**, not the former repeated institutional wrapper.

Event studies estimate how markets react around identifiable information releases.

## Event Dataset

For each event store:

- type;
- exact timestamp;
- actual;
- consensus;
- prior and revision;
- component surprises;
- pre-event pricing;
- policy regime;
- growth/inflation regime;
- liquidity/session;
- returns and cross-asset changes across windows.

## Windows

Potential windows:

- \([-60,-5]\) minutes: positioning/concession;
- \([-5,+1]\): release boundary;
- \([0,+5]\): mechanical response;
- \([+5,+30]\): price discovery;
- \([+30,+120]\): persistence;
- close-to-close;
- multi-day swing.

Avoid overlapping events or label them explicitly.

## Surprise Normalization

\[
S_{i,t} = \frac{A_{i,t} - C_{i,t}}{\sigma_i}
\]

For multi-component releases, estimate factors such as:

- inflation surprise;
- growth surprise;
- policy-path surprise;
- information shock.

## State Dependence

Estimate interactions:

\[
R_t = \alpha + \beta S_t + \gamma Regime_t +
\delta(S_t \times Regime_t) + \epsilon_t
\]

The interaction is often more important than unconditional \(\beta\).

## Cross-Asset Identification

Use high-frequency movement in:

- short-rate futures;
- longer yields;
- FX;
- equity index futures;
- volatility;
- commodities.

This helps separate policy, growth, inflation, and risk shocks.

## Confounds

- simultaneous releases;
- revisions;
- leaks;
- speeches;
- auction times;
- market closure;
- daylight-saving errors;
- low liquidity;
- contract roll;
- options expiry;
- data latency.

## Robustness

- alternative windows;
- median and trimmed means;
- sign tests;
- bootstrap intervals;
- subperiods;
- leave-one-event-out;
- excluding crisis outliers;
- multiple-testing adjustment.

## Trading Translation

An average event response is not an entry strategy. It informs:

- likely direction conditional on state;
- expected volatility;
- no-trade window;
- confirmation market;
- persistence;
- suitable technical setup timing.

---

## Primary source routes for Event Studies

- [[65 Source Registry and Claim Lineage/ALFRED — Federal Reserve Bank of St. Louis ALFRED]]
- [[65 Source Registry and Claim Lineage/FRED — Federal Reserve Bank of St. Louis FRED]]
- [[65 Source Registry and Claim Lineage/PHIL_RTDS — Philadelphia Fed — Real-Time Data Set]]
- [[65 Source Registry and Claim Lineage/ATL_GDPNOW — Atlanta Fed — GDPNow]]
- [[65 Source Registry and Claim Lineage/BLS_CPI — US BLS — CPI]]
- [[65 Source Registry and Claim Lineage/BEA_GDP — US BEA — GDP]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Execution Handoff]]
