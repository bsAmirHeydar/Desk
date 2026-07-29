---
title: "05 Expectations Pricing and Distribution Gap"
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
# 05 Expectations Pricing and Distribution Gap

> [!abstract] Purpose
> Measure the difference between the desk distribution and the distribution embedded in market prices, rather than classifying data as simply good or bad.

## Three distributions

1. **Economic distribution** — possible values of the state or release.
2. **Market distribution** — outcomes implied by curves, options, consensus, and positioning.
3. **Payoff distribution** — asset return conditional on outcome, regime, liquidity, and expression.

A trade exists only when the payoff-weighted difference is attractive after cost:

\[
Edge(a)=\sum_s [P_{desk}(s)-P_{mkt}(s)]\,Payoff(a,s)-Cost(a)
\]

## Measurement hierarchy

For policy, use meeting-dated OIS/futures and options where available. For inflation, use forecasts, fixings, breakevens, swaps, and option tails. For equities, use consensus revisions, guidance, reverse DCF, index concentration, and options. For commodities, use physical balances, curves, location spreads, and positioning.

No single object fully reveals expectations. Market prices include risk premia, liquidity, collateral value, regulatory demand, and convexity.

## Vulnerable assumption

A useful research packet states the assumption that must break:

- path of policy rather than next meeting;
- persistence rather than one print;
- margin rather than revenue;
- duration absorption rather than nominal deficit;
- refinery/product tightness rather than crude headline;
- hedge demand rather than unhedged capital flow.

## Surprise vector

For multi-component releases:

\[
S_t=(S_{headline},S_{core},S_{revision},S_{breadth},S_{policy-relevant})
\]

Estimate component betas by regime and horizon. Do not reduce a vector to one scalar unless the weights were estimated out of sample.

## Exhaustion

A correct thesis may have no remaining edge when:

- the price move already matches historical conditional response;
- options price a more extreme distribution;
- positioning is aligned and crowded;
- carry/roll is adverse;
- the next catalyst arrives before the expected half-life;
- the chosen instrument embeds unrelated expensive exposure.

## Required record

Record the consensus source and timestamp, dispersion, market-implied path, desk distribution, disagreement, payoff asymmetry, price already moved, and residual expected value.
