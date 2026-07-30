---
title: "05 Rates Treasury Repo and Inflation Markets Scientific Certification Scorecard"
type: canonical-standard
status: canonical
version: 9.0.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, scientific-qa]
---
# 05 Rates Treasury Repo and Inflation Markets Scientific Certification Scorecard

## Certification object

This scorecard tests whether an analysis has institutionally complete coverage of policy path, curve decomposition, term premium, inflation compensation, Treasury, repo, collateral and securitized rates.

## Mandatory science

- exact state vector and accounting identities;
- measurement definitions, transformations, publication lags and revisions;
- causal mechanisms and serious rival models;
- regime dependence and historical reference classes;
- expectations, pricing, valuation, carry and risk-premium translation where applicable;
- cross-domain transmission and institutional constraints;
- current and historical point-in-time output capability.

## Required primary evidence

- official rates and auctions
- yield and inflation curves
- repo and dealer statistics

## Red-team failure modes

- model-dependent term premium
- basis and delivery optionality
- liquidity versus macro shocks

## Certification tests

1. Can the report define the object and every material subcomponent?
2. Are state and market expectations reconstructed separately?
3. Does the conclusion survive at least two rival explanations?
4. Are measurement breaks, revisions and data gaps visible?
5. Are cross-asset or balance-sheet transmission channels explicit?
6. Does the report state contradictions, unknowns, expiry and update triggers?
7. Do all load-bearing claims have exact source locators?
8. Does the domain-specific benchmark query pass without generic filler?

## Verdict

FULL certification requires all eight tests, a score of at least 55/60 under [[81 Scientific QA and Certification Framework/17 Certification Verdict and Scorecard]], and no integrity veto.
