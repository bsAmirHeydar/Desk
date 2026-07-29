---
title: "19 Fundamental-Only Research Boundary and Implementation Standard"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-only, research-boundary, implementation-governance]
---
# 19 Fundamental-Only Research Boundary and Implementation Standard

## Purpose

This Vault is a fundamental, macroeconomic, balance-sheet, institutional-flow, market-structure, valuation and decision-science reference. It deliberately excludes non-fundamental price-pattern methods and proprietary trigger systems.

The exclusion is architectural rather than ideological. A research system becomes auditable only when it can distinguish:

1. information about the economic or financial state;
2. expectations already embedded in prices;
3. causal mechanisms and rival explanations;
4. instrument selection and portfolio consequences;
5. implementation constraints such as liquidity, cost, market impact and timing;
6. realized outcomes and attribution.

Price data remain admissible when used as a market-implied measurement, a response variable, a valuation input, a liquidity measure, a volatility estimate, a positioning proxy, an event-study outcome or a causal-leader observation. Price-only pattern interpretation is not admissible.

## Allowed research objects

- economic state and regime estimation;
- inflation, growth, labor, fiscal and monetary analysis;
- yield curves, policy pricing, term premium, collateral and funding;
- external balances, global dollar liquidity and FX valuation;
- corporate cash flows, earnings, balance sheets, credit and valuation;
- physical commodity balances, inventories, logistics and supply chains;
- market-implied distributions from options and rates;
- institutional positioning, fund flows, systematic allocations and dealer balance-sheet constraints;
- market depth, auctions, transaction costs, basis and execution capacity;
- geopolitical, sanctions, regulatory, climate and sovereign-risk transmission;
- portfolio construction, scenario loss, concentration and liquidity risk;
- point-in-time historical reconstruction, forecasting, causal inference and model governance.

## Prohibited research objects

- chart-pattern labels as evidence of economic state;
- indicator crossovers as causal claims;
- price geometry as a substitute for source-controlled information;
- discretionary reinterpretation of risk limits because a narrative remains attractive;
- undocumented pattern recognition used to increase confidence;
- retrospective chart annotation presented as ex-ante evidence.

## Fundamental decision states

Every operational output must use one of the following states or an explicitly defined research equivalent:

- `FUNDAMENTALLY_FAVORABLE_LONG`
- `FUNDAMENTALLY_FAVORABLE_SHORT`
- `BALANCED_OR_RELATIVE_VALUE_ONLY`
- `NO_DEPLOYMENT`
- `INSUFFICIENT_EVIDENCE`

The state is not an order. It is a research conclusion about expected payoff after pricing, scenario distribution, liquidity, cost and portfolio constraints.

## Implementation governance

Implementation may use:

- instrument selection;
- cash, futures, options, swaps, ETFs or relative-value expressions;
- execution windows defined by scheduled information or liquidity;
- risk budgets and scenario-loss limits;
- market-impact estimates;
- financing, carry and roll analysis;
- hedge ratios and basis risk;
- time expiry and information expiry;
- explicit cancellation conditions.

Implementation may not use an undocumented price pattern to override the fundamental decision state.

## Acceptance tests

A note, model, prompt or workflow passes this standard only when:

1. no prohibited price-pattern language remains;
2. the economic or institutional mechanism is explicit;
3. the priced baseline is documented;
4. the causal leader and independent confirmations are named;
5. uncertainty, rival models and missing data are disclosed;
6. deployment conditions are expressed through instrument, cost, liquidity, risk and expiry;
7. post-outcome attribution separates information quality, model quality, expression, timing, cost and residual noise.

## Canonical links

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
- [[00 Core Standards/17 Context Object and Permission Schema Standard]]
