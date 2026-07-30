---
title: "Hard Data versus Surveys"
type: field-guide
status: supporting-legacy
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
retrieval_priority: 10
default_retrieval: false
canonical_registry: "[[82 Canonical Institutional Fundamental Research Library/00 Canonical Institutional Fundamental Research Library MOC]]"
tags:
  - 15-nowcasting-forecasting-and-data-interpretation
  - hard-data-versus-surveys
  - institutional-fundamental
---
# Hard Data versus Surveys

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Hard Data versus Surveys**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

**Hard Data versus Surveys** is a research object inside point-in-time measurement, forecasting, causal inference, model validation, data lineage, and research deployment. The analyst must isolate the measurable state, the expectation already embedded in prices, the mechanism connecting them, and the horizon on which that inference can survive.

For **Hard Data versus Surveys**, the relevant institutional domain is **nowcast**: point-in-time measurement, forecasting, causal inference, model validation, data lineage, and research deployment. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Hard Data versus Surveys** represent, in what unit, population, instrument, and convention?
2. Which **Hard Data versus Surveys** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Hard Data versus Surveys** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Hard Data versus Surveys** mechanism is active?
5. What rival model can create the same target move while **Hard Data versus Surveys** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Hard Data versus Surveys** decision?

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

For **Hard Data versus Surveys**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Hard Data versus Surveys:** release and vintage timestamps.
- **Measurement 2 for Hard Data versus Surveys:** feature availability and missingness.
- **Measurement 3 for Hard Data versus Surveys:** forecast errors and revisions.
- **Measurement 4 for Hard Data versus Surveys:** probability calibration.
- **Measurement 5 for Hard Data versus Surveys:** drift, stability, cost, and implementation diagnostics.

The **Hard Data versus Surveys** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Hard Data versus Surveys:** state-space models.
- **Model layer 2 for Hard Data versus Surveys:** MIDAS and bridge equations.
- **Model layer 3 for Hard Data versus Surveys:** Bayesian VARs and local projections.
- **Model layer 4 for Hard Data versus Surveys:** panel and quasi-experimental methods.
- **Model layer 5 for Hard Data versus Surveys:** walk-forward and pseudo-real-time validation.

Validate the **Hard Data versus Surveys** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Hard Data versus Surveys** research object, methodology and data-generating process define model validity. |
| Cyclical | In the **Hard Data versus Surveys** research object, state estimates integrate asynchronous releases and revisions. |
| Tactical/Swing | In the **Hard Data versus Surveys** research object, forecast changes and confidence bands determine catalysts. |
| Daily/Event | In the **Hard Data versus Surveys** research object, only information available at the timestamp may update the estimate. |

Conflicts involving **Hard Data versus Surveys** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Hard Data versus Surveys channel 1:** test `raw release → vintage-controlled feature`.
2. **Hard Data versus Surveys channel 2:** test `feature → state or forecast distribution`.
3. **Hard Data versus Surveys channel 3:** test `distribution → pricing-gap estimate`.
4. **Hard Data versus Surveys channel 4:** test `estimate → permission tested against a baseline`.

**Hard Data versus Surveys asset translation:** Research: compare every model with simple real-time benchmarks and store the full forecast vintage. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Hard Data versus Surveys** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Hard Data versus Surveys:** lookahead and revision leakage.
- **Failure test 2 for Hard Data versus Surveys:** target leakage.
- **Failure test 3 for Hard Data versus Surveys:** multiple testing.
- **Failure test 4 for Hard Data versus Surveys:** unstable transformations.
- **Failure test 5 for Hard Data versus Surveys:** production data differing from research data.

Score **Hard Data versus Surveys** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Hard Data versus Surveys

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
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
