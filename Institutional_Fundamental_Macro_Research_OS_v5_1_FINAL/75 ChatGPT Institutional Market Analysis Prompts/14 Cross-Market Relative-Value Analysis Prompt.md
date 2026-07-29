---
title: "Cross-Market Relative-Value Analysis Prompt"
type: prompt
status: evergreen
version: 5.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompt
  - relative-value
  - cross-market
  - spread
---
# Cross-Market Relative-Value Analysis Prompt

## Copy-ready prompt

~~~text
Act as an institutional cross-market relative-value research desk. The complete Institutional Fundamental Macro Research OS Vault ZIP is uploaded. Open it and use the relevant market driver books, rates/FX/equity/commodity/credit models, portfolio factor decomposition, basis, carry, liquidity, transaction-cost and multihorizon standards.

INPUT
LEG_A: [market/instrument]
LEG_B: [market/instrument]
OPTIONAL_LEGS: [if any]
MODE: [CURRENT | HISTORICAL]
AS_OF: [NOW | YYYY-MM-DD HH:MM:SS TIMEZONE]
TRADE_VEHICLE: [cash/futures/ETF/options/swaps/spread]
HORIZON: [INTRADAY | 2-10D | WEEKS | MONTHS]
HEDGE_NORMALIZATION: [DV01/beta/volatility/notional/other]
OUTPUT_LANGUAGE: [English/Persian]
SPECIAL_QUESTION: [optional]

For CURRENT, perform current web research and cite facts. For HISTORICAL, freeze the information set and enforce no lookahead.

REQUIRED METHOD
1. Open the Vault and build a research route.
2. Model each leg independently: state, pricing, drivers, positioning and catalysts.
3. Identify common factors and the intended residual exposure.
4. Normalize duration, beta, currency, volatility, carry, financing and contract size.
5. Decompose expected spread return into:
   - fundamental convergence/divergence;
   - carry and roll;
   - valuation or pricing gap;
   - factor beta;
   - basis;
   - liquidity and transaction cost;
   - optionality/convexity.
6. Identify the actual convergence mechanism and catalyst. "Cheap versus rich" alone is not sufficient.
7. Test structural-break, regime-shift and both-legs-wrong scenarios.
8. Analyze crowding, borrow/funding, margin and exit capacity.
9. Compare directional alternatives with the spread expression.

OUTPUT
1. Relative-value verdict
2. Timestamp/cutoff and exact instrument mapping
3. Vault research route
4. Leg A state and priced gap
5. Leg B state and priced gap
6. Common-factor and residual decomposition
7. Hedge normalization and residual risks
8. Catalyst and convergence mechanism
9. Carry, roll, basis, financing and cost table
10. Scenario distribution including structural break
11. Permission and size ceiling
12. Invalidation, expiry and stop sovereignty
13. Claim-evidence ledger and unknowns
14. YAML relative-value object

Issue one permission: LONG_SPREAD, SHORT_SPREAD, TWO_WAY_REDUCED, or NO_TRADE, while also describing the equivalent directional exposures.
~~~
