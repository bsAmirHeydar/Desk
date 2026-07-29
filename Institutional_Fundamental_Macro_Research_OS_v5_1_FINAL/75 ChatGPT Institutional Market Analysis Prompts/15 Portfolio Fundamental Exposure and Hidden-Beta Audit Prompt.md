---
title: "Portfolio Fundamental Exposure and Hidden-Beta Audit Prompt"
type: prompt
status: evergreen
version: 5.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompt
  - portfolio
  - hidden-beta
  - risk-audit
---
# Portfolio Fundamental Exposure and Hidden-Beta Audit Prompt

## Copy-ready prompt

~~~text
Act as an institutional portfolio fundamental-risk, hidden-beta and catalyst-concentration audit desk. The complete Institutional Fundamental Macro Research OS Vault ZIP is uploaded. Open and use the portfolio construction, factor risk, liquidity, stress, scenario, market driver, country, options/flow and execution-handoff notes.

INPUT
PORTFOLIO: [positions, direction, size/weight/risk units, vehicle and currency]
MODE: [CURRENT | HISTORICAL]
AS_OF: [NOW | YYYY-MM-DD HH:MM:SS TIMEZONE]
HORIZON: [INTRADAY | 2-10D | WEEKS | MONTHS]
RISK_LIMITS: [optional]
KNOWN_HEDGES: [optional]
OUTPUT_LANGUAGE: [English/Persian]
SPECIAL_QUESTION: [optional]

For current mode, verify live/current facts and catalysts. For historical mode, freeze the information set.

REQUIRED METHOD
1. Open the Vault and list the material notes used.
2. Resolve every position's true economic exposure and vehicle-specific basis/carry/convexity.
3. Map each position to common fundamental drivers:
   - growth;
   - inflation;
   - policy path;
   - real yields;
   - term premium;
   - USD/global liquidity;
   - credit/risk premium;
   - commodity physical balance;
   - volatility/correlation;
   - country/political risk;
   - positioning/systematic flow;
   - liquidity and funding.
4. Identify false diversification, duplicated thesis, nonlinear exposure and hidden short-vol or short-liquidity risk.
5. Build the catalyst calendar and identify simultaneous event concentration.
6. Stress Base, growth shock, inflation shock, policy shock, fiscal/term-premium shock, USD funding shock, credit shock, volatility/liquidity shock and market-specific tails.
7. Evaluate hedges for basis risk, timing mismatch, convexity, carry and failure under stress.
8. Recommend keep, reduce, rebalance, hedge, replace or no action. Do not optimize using false precision when position data are incomplete.

OUTPUT
1. Portfolio verdict
2. Timestamp/cutoff and data-quality statement
3. Vault research route
4. Position-by-position driver map
5. Aggregate factor and hidden-beta map
6. Correlation versus causal concentration
7. Catalyst concentration calendar
8. Liquidity, financing, convexity and gap-risk audit
9. Scenario stress table
10. Hedge effectiveness and basis-risk table
11. Recommended risk actions with priorities
12. Portfolio-level permission and kill-switches
13. Claim-evidence ledger and unknowns
14. YAML portfolio context object

The audit must distinguish notional diversification from true driver diversification.
~~~

> [!important] Fundamental-only boundary
> Price-pattern analysis, indicator rules and chart-trigger instructions are prohibited. Use the Vault's fundamental, macro, valuation, flow, liquidity, market-structure and portfolio methods.
