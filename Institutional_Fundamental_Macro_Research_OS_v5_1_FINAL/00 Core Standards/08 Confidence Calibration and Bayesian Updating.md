---
title: "08 Confidence Calibration and Bayesian Updating"
type: standard
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - institutional-standard
  - fundamental-research
  - governance
---
# 08 Confidence Calibration and Bayesian Updating

> [!abstract] Purpose
> Convert evidence into probabilities that correspond to long-run frequencies and decision utility.

## Update

\[
PosteriorOdds=PriorOdds\times LikelihoodRatio
\]

Priors should be conditioned on asset, regime, horizon, and setup family. Evidence from the same release or causal chain is dependent; cap or model the joint likelihood rather than multiplying every indicator.

## Confidence components

- state-estimation certainty;
- expectation/pricing measurement quality;
- causal-mechanism confidence;
- transmission reliability;
- regime stability;
- liquidity/execution quality;
- evidence independence;
- model stability.

A low score in one indispensable component can cap total confidence.

## Calibration

Use reliability bins, Brier score, log score, calibration intercept/slope, and resolution. Evaluate out of sample and by regime. Calibration answers whether 70% forecasts occur roughly 70% of the time; discrimination answers whether high probabilities separate outcomes.

## Update limits

Update only for material evidence. Price alone is evidence about others' beliefs and flow, not automatically evidence about economic truth. Record the likelihood model used and whether the observation was anticipated.

## Human judgment

Judgment can adjust a model only through a recorded overlay containing reason, direction, magnitude, expiry, and later attribution. Compare model-only, human-only, and combined performance.

## Sizing

Probability is not position size. Size also depends on payoff asymmetry, covariance, gap risk, liquidity, confidence error, and portfolio concentration.
