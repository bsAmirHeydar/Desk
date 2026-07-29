---
title: "09 Portfolio Liquidity and Implementation Governance"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [portfolio, liquidity, implementation, risk]
---
# 09 Portfolio Liquidity and Implementation Governance

## Principle

A correct fundamental view can be an unacceptable portfolio decision. Research must be translated through portfolio exposure, liquidity, financing, convexity, correlation, basis and scenario loss.

## Mandatory portfolio map

Before deployment, aggregate:

- duration and key-rate exposure;
- real-yield and inflation exposure;
- dollar and cross-currency exposure;
- growth, earnings and credit beta;
- commodity and physical-balance exposure;
- volatility, skew and convexity exposure;
- liquidity and funding dependence;
- country, legal and sanctions exposure;
- crowded-flow and deleveraging exposure;
- catalyst and gap concentration.

## Expression selection

Compare cash, futures, options, swaps, ETFs and relative-value structures on:

- purity of the intended factor;
- carry and financing;
- convexity and gap behavior;
- liquidity and market depth;
- basis and hedge risk;
- transaction cost and impact;
- legal, operational and tax constraints;
- capacity and crowdedness;
- exit feasibility under stress.

## Risk sizing

Size is constrained by the minimum of:

- research-confidence budget;
- scenario-loss limit;
- liquidity-adjusted capacity;
- concentration limit;
- funding and margin headroom;
- model-risk cap;
- governance approval level.

Confidence is not leverage. A highly confident but negatively convex or illiquid expression may deserve smaller size than a lower-confidence, liquid and bounded-loss expression.

## Liquidity stress

Stress bid-ask spreads, depth, market impact, financing, haircuts, basis, correlation and execution delay. Include the possibility that the hedge becomes less liquid or more correlated precisely when needed.

## Exit governance

Every deployment requires:

- information invalidation;
- scenario-loss limit;
- liquidity contingency;
- time expiry;
- catalyst completion rule;
- financing or carry limit;
- escalation path if exit is impaired.
