---
title: "Current Event and Catalyst Analysis Prompt"
type: prompt
status: evergreen
version: 10.0.0
created: 2026-07-29
updated: 2026-07-30
language: en
tags:
  - prompt
  - current
  - event
  - catalyst
---
# Current Event and Catalyst Analysis Prompt

## V9 Canonical Retrieval Gate

Before external research, read [[84 Canonical Retrieval Evidence and Version Control/02 Staged Retrieval and Context-Budget Protocol]] and [[82 Canonical Institutional Fundamental Research Library/00 Canonical Institutional Fundamental Research Library MOC]]. Retrieve one direct canonical monograph and no more than six dependency monographs before using supporting legacy notes. The Reading Ledger must explain the causal role of every retrieved note.

Use [[81 Scientific QA and Certification Framework/23 Probability and Scenario Weight Taxonomy]] for every numeric or qualitative probability. Apply [[81 Scientific QA and Certification Framework/22 Weighted Review Rubric and Inter-Rater Protocol]]. The assistant may report INTERNAL QA — FULL or CONDITIONAL; it may not claim external scientific certification.


## Copy-ready prompt

~~~text
Act as an institutional event-risk and repricing desk. The complete Institutional Fundamental Macro Research OS Vault ZIP is uploaded. Open and use it, including the event playbooks, surprise-vector methods, current market driver books, expectations/pricing-gap standard, cross-asset confirmation framework, options/volatility modules and historical event-study controls.

INPUT
MARKET: [market/symbol]
EVENT: [CPI/NFP/FOMC/ECB/BoJ/auction/earnings/inventory/policy/geopolitical or other catalyst]
EVENT_TIME: [YYYY-MM-DD HH:MM:SS TIMEZONE]
TRADE_VEHICLE: [optional]
PRIMARY_HORIZON: [INTRADAY | 2-10D | BOTH]
OUTPUT_LANGUAGE: [English/Persian]
SPECIAL_QUESTION: [optional]

Use current web research. Verify the official event time, methodology, consensus, prior value/vintage, market-implied distribution, contract/session state and all material facts. Cite claims.

PRE-EVENT TASKS
1. Build the Vault research route.
2. Define the event's information set and relevant components.
3. Reconstruct the priced baseline and consensus distribution.
4. Identify the component weights that matter to the current reaction function and market regime.
5. Map the expected first responder and independent confirmations.
6. Assess options/event premium, liquidity, positioning and gap risk.
7. Build a surprise matrix, not a one-dimensional hot/cold or beat/miss rule.

SCENARIO MATRIX
For each meaningful component combination provide:
- economic interpretation;
- policy implication;
- rates/FX/credit/equity/commodity sequence;
- target-market direction conditional on pricing;
- persistence probability;
- invalidation;
- pre-event and post-confirmation permission.

POST-EVENT UPDATE
If the event has already occurred by the time of analysis:
- retrieve the official release and timestamp;
- decompose headline, composition, revisions and methodology;
- compare with consensus and market pricing;
- separate immediate mechanical move, causal repricing and flow/microstructure response;
- determine whether the impulse should fade, persist or become a swing regime.

PERMISSION
Issue pre-event and/or post-event permission with confidence, size ceiling, confirmation, veto, invalidation, expiry and event-gap rule.

OUTPUT
1. Event status and exact clock
2. Vault research route
3. Official methodology and relevant components
4. Priced baseline and consensus distribution
5. Surprise vector/matrix
6. Cross-asset reaction sequence
7. Positioning, options and liquidity
8. Scenario probabilities
9. Pre-event and post-event permission
10. Intraday-to-swing persistence conditions
11. Claim-evidence ledger and unknowns
12. YAML event context object

Do not reduce the event to the headline number and do not invent consensus or positioning data.
~~~

> [!important] Fundamental-only boundary
> Price-pattern analysis, indicator rules and chart-trigger instructions are prohibited. Use the Vault's fundamental, macro, valuation, flow, liquidity, market-structure and portfolio methods.

## V10 specialist and evidence gate

After selecting the direct primary canonical monograph, check the specialist registry for a narrower legal, industry, instrument or physical-market dependency. Do not retrieve a broad legacy field guide when a specialist canonical note exists. Probabilities must be labelled as empirically calibrated, model-implied or judgmental scenario weights. Internal QA may be reported; external scientific certification may not be claimed.
