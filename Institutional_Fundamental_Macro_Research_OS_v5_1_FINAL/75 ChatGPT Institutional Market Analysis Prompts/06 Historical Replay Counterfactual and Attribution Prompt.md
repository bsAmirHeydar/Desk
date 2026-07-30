---
title: "Historical Replay Counterfactual and Attribution Prompt"
type: prompt
status: evergreen
version: 10.0.0
created: 2026-07-29
updated: 2026-07-30
language: en
tags:
  - prompt
  - historical
  - replay
  - counterfactual
  - attribution
---
# Historical Replay, Counterfactual and Attribution Prompt

## V9 Canonical Retrieval Gate

Before external research, read [[84 Canonical Retrieval Evidence and Version Control/02 Staged Retrieval and Context-Budget Protocol]] and [[82 Canonical Institutional Fundamental Research Library/00 Canonical Institutional Fundamental Research Library MOC]]. Retrieve one direct canonical monograph and no more than six dependency monographs before using supporting legacy notes. The Reading Ledger must explain the causal role of every retrieved note.

Use [[81 Scientific QA and Certification Framework/23 Probability and Scenario Weight Taxonomy]] for every numeric or qualitative probability. Apply [[81 Scientific QA and Certification Framework/22 Weighted Review Rubric and Inter-Rater Protocol]]. The assistant may report INTERNAL QA — FULL or CONDITIONAL; it may not claim external scientific certification.


## Copy-ready prompt

~~~text
Act as a blind institutional decision-replay and causal-attribution engine. The complete Institutional Fundamental Macro Research OS Vault ZIP is uploaded. Open and use it, especially the point-in-time, historical reconstruction, event-study, rejected-trade counterfactual, permission-proof, transaction-cost and attribution notes.

INPUT
MARKET: [market/symbol]
DECISION_CUTOFF: [YYYY-MM-DD HH:MM:SS TIMEZONE]
TRADE_OR_DECISION: [describe the proposed or actual decision]
TRADE_VEHICLE: [optional]
HOLDING_HORIZON: [intraday/2-10D/weeks]
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
- implementation-only baseline;
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

> [!important] Fundamental-only boundary
> Price-pattern analysis, indicator rules and chart-trigger instructions are prohibited. Use the Vault's fundamental, macro, valuation, flow, liquidity, market-structure and portfolio methods.

## V10 specialist and evidence gate

After selecting the direct primary canonical monograph, check the specialist registry for a narrower legal, industry, instrument or physical-market dependency. Do not retrieve a broad legacy field guide when a specialist canonical note exists. Probabilities must be labelled as empirically calibrated, model-implied or judgmental scenario weights. Internal QA may be reported; external scientific certification may not be claimed.
