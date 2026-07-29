---
title: "07 Permission Proof and Incremental Edge"
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
# 07 Permission Proof and Incremental Edge

> [!abstract] Purpose
> Prove that fundamental context improves a defined technical baseline rather than merely explaining trades after the fact.

## Baselines

At minimum compare:

- technical strategy alone;
- technical plus calendar exclusion;
- technical plus random permission with equal trade count;
- technical plus simple public macro rule;
- full fundamental permission;
- fundamental permission with costs and delayed data.

## Permission outputs

- `LONG_ONLY`
- `SHORT_ONLY`
- `TWO_WAY_REDUCED`
- `NO_TRADE`

Each output requires deterministic or probabilistic thresholds stored before evaluation. Confidence is not a synonym for conviction.

## Incremental tests

Measure:

- net expectancy;
- hit rate and payoff ratio;
- drawdown;
- tail loss and gap exposure;
- turnover and implementation shortfall;
- percentage of profitable baseline trades vetoed;
- percentage of losing trades vetoed;
- opportunity cost of `NO_TRADE`;
- calibration of confidence bins;
- stability by asset, regime, event type, and horizon.

\[
IncrementalEdge=Metric(Technical+Fundamental)-Metric(Technical)
\]

Use paired trades or matched opportunities so trade selection does not create a misleading comparison.

## Decision thresholds

Optimize against utility and survival constraints, not maximum in-sample Sharpe. A permission model must beat a no-information base rate and remain useful after latency, revisions, fees, slippage, financing, and rejected-trade opportunity cost.

## Falsification

Retire or reduce a rule when:

- edge is concentrated in one episode;
- sign reverses across plausible specifications;
- confidence is uncalibrated;
- the model selects fewer trades without improving utility;
- the target asset moves before the supposed leader;
- the edge disappears with first-release data;
- the result depends on one vendor field unavailable historically.

## Governance

No analyst may change event windows, thresholds, regime labels, or exclusions after viewing test outcomes without creating a new model version and returning to research status.
