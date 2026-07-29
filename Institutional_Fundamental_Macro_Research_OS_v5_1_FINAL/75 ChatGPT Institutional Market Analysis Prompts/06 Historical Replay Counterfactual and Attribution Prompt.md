---
title: "Historical Replay Counterfactual and Attribution Prompt"
type: prompt
status: evergreen
version: 5.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompt
  - historical
  - replay
  - counterfactual
  - attribution
---
# Historical Replay, Counterfactual and Attribution Prompt

## Copy-ready prompt

~~~text
Act as a blind institutional decision-replay and causal-attribution engine. The complete Institutional Fundamental Macro Research OS Vault ZIP is uploaded. Open and use it, especially the point-in-time, historical reconstruction, event-study, rejected-trade counterfactual, permission-proof, transaction-cost and attribution notes.

INPUT
MARKET: [market/symbol]
DECISION_CUTOFF: [YYYY-MM-DD HH:MM:SS TIMEZONE]
TRADE_OR_DECISION: [describe the proposed or actual decision]
TRADE_VEHICLE: [optional]
HOLDING_HORIZON: [intraday/2-10D/weeks]
TECHNICAL_INFORMATION_AVAILABLE_AT_CUTOFF: [optional]
PORTFOLIO_INFORMATION_AVAILABLE_AT_CUTOFF: [optional]
OUTCOME_WINDOW_END: [optional]
OUTPUT_LANGUAGE: [English/Persian]

PHASE A — BLIND RECONSTRUCTION
- Freeze all information at DECISION_CUTOFF.
- Open the Vault, build a research route and reconstruct only contemporaneous evidence, first-release vintages, expectations, market pricing, contract state, catalyst map and cross-asset conditions.
- Build multihorizon states, causal/rival models and scenario probabilities without seeing or using the result.
- Issue and lock a permission and decision-quality assessment.
- Assign a locked decision ID.

PHASE B — OUTCOME RECOVERY
Only after Phase A is locked:
- Recover the subsequent price path, realized catalysts and relevant revisions through OUTCOME_WINDOW_END.
- Label all later information EX-POST.
- Do not edit Phase A.

PHASE C — CAUSAL ATTRIBUTION
Separate:
- thesis correctness;
- causal-mechanism correctness;
- timing;
- expression/basis;
- execution;
- sizing and risk control;
- transaction cost and liquidity;
- luck, path dependency and exogenous shocks.

PHASE D — COUNTERFACTUALS
Compare the locked decision with:
- no trade;
- technical-only baseline;
- simple macro rule;
- random permission;
- opposite direction;
- alternative instrument/expression;
- delayed entry;
- smaller size;
- rejected opportunity.

Do not claim a counterfactual was executable unless the information, liquidity, instrument and timestamp made it feasible.

PHASE E — LEARNING WITHOUT HINDSIGHT
Record:
- what could have been known;
- what could not have been known;
- which process rule was followed or violated;
- whether the fundamental permission added incremental value;
- whether a new rule is justified by enough repeated evidence rather than one outcome;
- model, data or workflow changes to test in shadow mode.

OUTPUT
1. Decision and cutoff identity
2. Vault research route
3. Point-in-time source/vintage audit
4. Blind multihorizon reconstruction
5. Blind scenario distribution
6. LOCKED decision and permission
7. EX-POST outcome path
8. Causal attribution
9. Counterfactual comparison table
10. Avoided losses, rejected winners and opportunity cost
11. Transaction cost, capacity and execution audit
12. Process lessons and proposed tests
13. YAML replay record
14. Anti-hindsight checklist

Perform all phases in order and visibly preserve the separation.
~~~
