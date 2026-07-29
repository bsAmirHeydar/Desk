---
title: "Default Probability Recovery and Distress Ratios"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 39-credit-markets-default-and-recovery-cycle
  - default-probability-recovery-and-distress-ratios
  - institutional-fundamental
---
# Default Probability Recovery and Distress Ratios

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Default Probability Recovery and Distress Ratios**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Credit pricing combines expected default loss, recovery uncertainty, downgrade/migration, liquidity, risk premium, implementation supply, and embedded options. Probabilistic research requires explicit priors, likelihoods, posterior distributions, calibration, resolution, and decision utility.

For **Default Probability Recovery and Distress Ratios**, the relevant institutional domain is **banking**: intermediation capacity, liability stability, asset quality, leverage, maturity transformation, and default/recovery dynamics. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Default Probability Recovery and Distress Ratios** represent, in what unit, population, instrument, and convention?
2. Which **Default Probability Recovery and Distress Ratios** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Default Probability Recovery and Distress Ratios** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Default Probability Recovery and Distress Ratios** mechanism is active?
5. What rival model can create the same target move while **Default Probability Recovery and Distress Ratios** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Default Probability Recovery and Distress Ratios** decision?

## Identities and model skeleton

$$
ExpectedLoss\approx PD\times LGD
$$

$$
Spread\approx ExpectedLoss+LiquidityPremium+RiskPremium+OptionCost
$$

$$
Hazard\approx \frac{Spread}{1-Recovery}\quad\mathrm{under\ simplifying\ assumptions}
$$

$$
P(H|E)=\frac{P(E|H)P(H)}{P(E)}
$$

$$
Brier=\frac1N\sum_{i=1}^{N}(p_i-y_i)^2
$$

$$
EV(a)=\sum_s P(s|I)\,U(a,s)
$$

For **Default Probability Recovery and Distress Ratios**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Default Probability Recovery and Distress Ratios:** spreads and excess spread.
- **Measurement 2 for Default Probability Recovery and Distress Ratios:** default, downgrade, and distress ratios.
- **Measurement 3 for Default Probability Recovery and Distress Ratios:** recovery and capital-structure seniority.
- **Measurement 4 for Default Probability Recovery and Distress Ratios:** issuance, fund flows, dealer inventory, and liquidity.
- **Measurement 5 for Default Probability Recovery and Distress Ratios:** earnings, leverage, interest coverage, and maturity wall.
- **Measurement 6 for Default Probability Recovery and Distress Ratios:** prior and posterior probabilities.
- **Measurement 7 for Default Probability Recovery and Distress Ratios:** forecast bins and realized frequencies.
- **Measurement 8 for Default Probability Recovery and Distress Ratios:** likelihood ratios.
- **Measurement 9 for Default Probability Recovery and Distress Ratios:** base rates by regime.
- **Measurement 10 for Default Probability Recovery and Distress Ratios:** utility, loss, and action threshold.

The **Default Probability Recovery and Distress Ratios** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Default Probability Recovery and Distress Ratios:** hazard and survival model.
- **Model layer 2 for Default Probability Recovery and Distress Ratios:** rating migration matrix.
- **Model layer 3 for Default Probability Recovery and Distress Ratios:** recovery waterfall.
- **Model layer 4 for Default Probability Recovery and Distress Ratios:** Merton-style distance to default.
- **Model layer 5 for Default Probability Recovery and Distress Ratios:** spread decomposition and stress.
- **Model layer 6 for Default Probability Recovery and Distress Ratios:** Bayesian updating.
- **Model layer 7 for Default Probability Recovery and Distress Ratios:** reliability diagrams.
- **Model layer 8 for Default Probability Recovery and Distress Ratios:** isotonic/Platt calibration.
- **Model layer 9 for Default Probability Recovery and Distress Ratios:** proper scoring rules.
- **Model layer 10 for Default Probability Recovery and Distress Ratios:** decision-curve analysis.

Validate the **Default Probability Recovery and Distress Ratios** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Default Probability Recovery and Distress Ratios** research object, franchise, regulation, liability structure, and underwriting define resilience. |
| Cyclical | In the **Default Probability Recovery and Distress Ratios** research object, funding cost, lending standards, defaults, and recoveries evolve. |
| Tactical/Swing | In the **Default Probability Recovery and Distress Ratios** research object, deposit flow, issuance, ratings, margin, and forced deleveraging matter. |
| Daily/Event | In the **Default Probability Recovery and Distress Ratios** research object, funding spreads, bank equity, credit ETFs, and counterparties reveal stress. |

Conflicts involving **Default Probability Recovery and Distress Ratios** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Default Probability Recovery and Distress Ratios channel 1:** test `funding cost → lending standards`.
2. **Default Probability Recovery and Distress Ratios channel 2:** test `credit availability → demand and defaults`.
3. **Default Probability Recovery and Distress Ratios channel 3:** test `asset losses → capital and intermediation`.
4. **Default Probability Recovery and Distress Ratios channel 4:** test `margin/redemptions → forced sales and contagion`.

**Default Probability Recovery and Distress Ratios asset translation:** Credit/banks: test funding, standards, spreads, default/recovery, and balance-sheet capacity. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Default Probability Recovery and Distress Ratios** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Default Probability Recovery and Distress Ratios:** equating spread with default probability.
- **Failure test 2 for Default Probability Recovery and Distress Ratios:** fixed recovery assumption.
- **Failure test 3 for Default Probability Recovery and Distress Ratios:** ignoring callable bonds.
- **Failure test 4 for Default Probability Recovery and Distress Ratios:** using index spread for issuer risk.
- **Failure test 5 for Default Probability Recovery and Distress Ratios:** missing liquidity and forced-fund flows.
- **Failure test 6 for Default Probability Recovery and Distress Ratios:** confidence as prose intensity.
- **Failure test 7 for Default Probability Recovery and Distress Ratios:** base-rate neglect.
- **Failure test 8 for Default Probability Recovery and Distress Ratios:** double counting correlated evidence.
- **Failure test 9 for Default Probability Recovery and Distress Ratios:** outcome-based scoring of process.
- **Failure test 10 for Default Probability Recovery and Distress Ratios:** calibrating on in-sample predictions.

Score **Default Probability Recovery and Distress Ratios** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Default Probability Recovery and Distress Ratios

- [[65 Source Registry and Claim Lineage/FED_FSR — Federal Reserve — Financial Stability Report]]
- [[65 Source Registry and Claim Lineage/IMF_GFSR — IMF Global Financial Stability Report]]
- [[65 Source Registry and Claim Lineage/OFR_FSI — Office of Financial Research Financial Stress Index]]
- [[65 Source Registry and Claim Lineage/SEC_EDGAR — SEC EDGAR]]
- [[65 Source Registry and Claim Lineage/PHIL_RTDS — Philadelphia Fed — Real-Time Data Set]]
- [[65 Source Registry and Claim Lineage/ALFRED — Federal Reserve Bank of St. Louis ALFRED]]
- [[65 Source Registry and Claim Lineage/IMF_WEO — IMF World Economic Outlook]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
