---
title: "07 Permission Proof and Incremental Edge"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [incremental-edge, decision-state, validation]
---
# 07 Permission Proof and Incremental Edge

## Objective

A fundamental decision layer is valuable only if it improves a predeclared baseline after realistic costs, latency, capacity and opportunity cost. Complexity is not evidence of edge.

## Baselines

At minimum compare:

1. unconditional exposure;
2. simple calendar exclusions;
3. simple valuation or macro rule;
4. market-implied-only model;
5. full fundamental decision engine;
6. full engine after cost, financing, latency and portfolio constraints.

## Evaluation unit

The unit may be a forecast, a decision opportunity, a campaign, an event window or a portfolio rebalance. It must be defined before outcome analysis. Rejected opportunities must be stored; otherwise the value of `NO_DEPLOYMENT` cannot be measured.

## Metrics

- out-of-sample expected value;
- probability calibration and Brier score;
- log score for density forecasts;
- hit rate and payoff distribution;
- drawdown and tail loss;
- expected shortfall and scenario loss;
- turnover, cost and implementation shortfall;
- missed favorable outcomes;
- avoided adverse outcomes;
- stability by regime, horizon and asset;
- capacity and liquidity sensitivity;
- incremental information ratio or utility versus baseline.

## Research design

Use rolling or expanding pseudo-real-time evaluation, embargoes where labels overlap, realistic release timestamps, model-version freezes and nested validation. Hyperparameter selection must occur inside the training window.

## Decision thresholds

Thresholds are selected by expected utility under constraints, not by maximizing in-sample accuracy. The desk must disclose how threshold changes affect false deployment, missed opportunity, tail loss and concentration.

## Promotion standard

A decision engine is promoted only when:

- it beats simple baselines out of sample;
- calibration is acceptable or explicitly corrected;
- performance survives reasonable cost and latency stress;
- the effect is not concentrated in one episode;
- the mechanism is economically coherent;
- capacity and data licensing are operationally feasible;
- independent risk approves the failure and retirement plan.
