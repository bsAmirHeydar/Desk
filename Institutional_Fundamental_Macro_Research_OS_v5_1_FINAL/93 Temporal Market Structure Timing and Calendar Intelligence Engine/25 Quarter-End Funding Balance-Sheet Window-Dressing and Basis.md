---
title: "Quarter-End Funding Balance-Sheet Window-Dressing and Basis"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Quarter-End Funding, Balance-Sheet Window Dressing and Basis

Quarter-end can alter dealer intermediation capacity and cross-currency funding independently of macro news. BIS research documents FX spot/swap liquidity spillovers tied to quarter-end funding shocks and periodic G-SIB dealer pullback (`SRC-BIS-FX-LIQ`). The Basel Committee has also highlighted balance-sheet window dressing around reporting dates (`SRC-BIS-WINDOW`).

## Mechanisms
- leverage-ratio/reporting constraints;
- repo/funding balance-sheet reduction;
- cross-currency basis dislocation;
- reduced dealer willingness to warehouse risk;
- pension/asset-manager quarter-end rebalance;
- quarterly derivatives expiry;
- index rebalance and earnings/reporting overlap.

## Timing state
`NORMAL_QUARTER`, `QUARTER_END_BUILDUP`, `FUNDING_STRESS`, `BALANCE_SHEET_PULLBACK`, `QUARTER_END_FIX`, `POST_QUARTER_NORMALIZATION`.

## Cross-asset transmission
Funding stress can affect FX liquidity and dollar demand; rates/liquidity changes can transmit to gold and equities. V15 passes this as a causal temporal/funding force to V11/V14.1 rather than treating quarter-end as a chart pattern.

## Data
Use cross-currency basis, repo/funding indicators, dealer liquidity proxies and spreads where legally/technically available. Missing licensed data must cap confidence.
