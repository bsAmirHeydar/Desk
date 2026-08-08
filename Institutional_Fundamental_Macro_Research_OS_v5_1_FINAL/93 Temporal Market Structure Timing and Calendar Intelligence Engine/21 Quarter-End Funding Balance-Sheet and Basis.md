---
title: "21 Quarter-End Funding Balance-Sheet and Basis"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Quarter-End Funding, Balance-Sheet and Basis

Quarter-end can alter dealer intermediation and FX funding independently of macro news. Model leverage/reporting constraints, repo/funding balance-sheet reduction, cross-currency basis, dealer risk warehousing, pension/asset-manager rebalance, quarterly derivatives and index maintenance.

States: `QUARTER_END_BUILDUP`, `FUNDING_STRESS`, `BALANCE_SHEET_PULLBACK`, `QUARTER_END_FIX`, `POST_QUARTER_NORMALIZATION`.

Pass funding pressure as an explicit temporary causal force to the Edge engine; do not create a generic “quarter-end direction.”
