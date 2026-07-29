---
title: "09 Portfolio Liquidity and Execution Handoff"
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
# 09 Portfolio Liquidity and Execution Handoff

> [!abstract] Purpose
> Translate a research distribution into an executable position without hiding factor concentration, basis risk, liquidity, or path dependency.

## Expression selection

Choose among outright, relative-value, curve, spread, option, or cross-asset expressions. Compare:

- purity to the research driver;
- carry and roll;
- convexity;
- liquidity and market hours;
- event gap;
- financing/borrow;
- basis and counterparty risk;
- capacity;
- path sensitivity.

The highest-beta instrument is not necessarily the best expression.

## Portfolio decomposition

Map every proposed trade to underlying drivers: growth, inflation, policy path, term premium, dollar funding, credit, volatility, commodity balance, and liquidity. Multiple positions can be one hidden trade.

\[
PortfolioLoss_s=\sum_i Exposure_i\times Shock_{i,s}+Nonlinear_i(s)+Cost_s
\]

## Liquidity budget

Size against executable depth, expected participation, spread, impact, margin, and liquidation time under stress. Include simultaneous liquidity deterioration across correlated positions.

## Technical handoff

Research provides permission, leader, confirmations, fundamental invalidation, expiry, and size ceiling. Execution provides trigger, structural stop, order type, fill rule, and exit mechanics. Fundamentals never widen the structural stop after entry.

## Kill conditions

Cancel or reduce when the causal leader reverses, independent confirmation fails, liquidity deteriorates beyond the model, correlation converges across the book, margin buffer breaches, or the thesis reaches expiry without realization.

## Attribution

Separate research alpha, expression alpha, timing, sizing, execution, carry, convexity, hedge, and residual noise.
