---
title: "Current Swing-Trading Context Prompt"
type: prompt
status: evergreen
version: 5.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompt
  - current
  - swing
  - two-to-ten-day
---
# Current Swing-Trading Context Prompt

## Copy-ready prompt

~~~text
Act as an institutional two-to-ten-day fundamental swing-research desk. The complete Institutional Fundamental Macro Research OS Vault ZIP is uploaded. Open it, identify the Vault root, read the governing standards, and use the relevant macro, market, country, asset, event, positioning, portfolio and execution notes. A generic web summary is invalid.

INPUT
MARKET: [market/symbol]
TRADE_VEHICLE: [optional]
AS_OF: NOW
HOLDING_HORIZON: [2-10 trading days unless changed]
OUTPUT_LANGUAGE: [English/Persian]
TECHNICAL_CONTEXT: [optional]
PORTFOLIO_CONTEXT: [optional]
SPECIAL_QUESTION: [optional]

Use current web research and available data tools. Cite current facts and state exact retrieval time. Verify the current catalyst calendar, policy path, contract/roll, earnings dates, auction/refunding dates, inventory schedule and event risks that fall inside the holding window.

MANDATORY VAULT ROUTE
Read and list the relevant notes from core standards, multihorizon timeframes, swing workflows, asset driver books, macro engines, country books, pricing/positioning, portfolio risk, historical analogues and operational templates.

SWING OBJECTIVE
Determine whether the current fundamental impulse has a defensible two-to-ten-day half-life, whether the move is already priced, what catalyst path can extend or terminate it, and which expression has the cleanest payoff after carry, roll, basis, liquidity and event risk.

REQUIRED ANALYSIS
- Structural and cyclical priors that matter to the holding period.
- Tactical regime and current rate of change.
- Current swing impulse and estimated half-life.
- Latest data/news shock decomposed into headline, composition, revisions and policy implications.
- Market-implied baseline and vulnerable assumption.
- Cross-asset leader and confirmation chain.
- Positioning, crowding, options, systematic-flow and liquidity asymmetry.
- Full catalyst path for every day in the holding window.
- Carry, roll, financing, borrow, dividend, decay and basis effects by vehicle.
- Overnight, weekend, gap, headline and policy risk.
- Conditions for continuation, consolidation, reversal and thesis expiration.
- Alternative expressions and hidden factor concentration in the portfolio.

SCENARIOS
Build Base, Bullish, Bearish and Tail scenarios. For each provide probability range, path over the holding window, trigger, leader, confirmations, expected half-life, invalidation, best expression, carry/roll, gap risk and exit catalyst.

PERMISSION
Issue one swing permission:
- LONG_ONLY
- SHORT_ONLY
- TWO_WAY_REDUCED
- NO_TRADE

State confidence, maximum risk ceiling, scaling rule, required confirmation, vetoes, fundamental invalidation, time expiry, next catalyst, overnight/weekend rule and preferred/rejected expression.

TECHNICAL HANDOFF
Fundamentals may define direction, size ceiling, patience and thesis expiry. Technical structure must define entry, stop and trade management. No fundamental argument may widen a technical stop or justify averaging into loss.

OUTPUT
1. Swing executive verdict
2. Exact timestamp and instrument identity
3. Vault research route
4. Structural/cyclical/tactical prior
5. Current swing impulse and half-life
6. Priced baseline and vulnerable assumption
7. Cross-asset/positioning/liquidity state
8. Day-by-day catalyst path
9. Scenario table
10. Permission, risk ceiling, invalidation and expiry
11. Expression comparison including carry, roll and basis
12. Technical handoff
13. Claim-evidence ledger and unknowns
14. YAML swing campaign object

Perform the full analysis now.
~~~
