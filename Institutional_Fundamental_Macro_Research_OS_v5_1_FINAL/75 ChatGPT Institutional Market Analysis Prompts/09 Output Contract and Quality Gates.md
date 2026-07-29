---
title: "Output Contract and Quality Gates"
type: contract
status: evergreen
version: 5.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompts
  - output-contract
  - quality-gates
---
# Output Contract and Quality Gates

Every full-spectrum prompt must deliver the following structure. A section may contain `UNKNOWN`, but it may not be silently omitted when material.

## 1. Executive institutional verdict

- one paragraph;
- dominant driver;
- what is priced;
- vulnerable assumption;
- overall permission;
- confidence range;
- invalidation and expiry.

## 2. Status board

| Field | Required value |
|---|---|
| Analysis mode | Current or historical |
| Timestamp/cutoff | Exact time and timezone |
| Market and vehicle | Exact identity |
| Session/venue state | Open, closed, pre/post or historical state |
| Dominant regime | Named and defined |
| Causal leader | Market or variable expected to lead |
| Priced assumption | Main embedded belief |
| Vulnerable assumption | Main repricing risk |
| Next catalyst | Time and timezone |
| Permission | One of four allowed labels |
| Confidence | Range plus data-quality grade |
| Invalidation/expiry | Concise rule |

## 3. Vault research route

List the Vault notes actually used and one sentence on how each affected the analysis. Do not list notes merely to create the appearance of coverage.

## 4. Evidence and data-quality statement

- source hierarchy used;
- retrieval times or historical publication times;
- first-release/vintage status;
- proprietary/live-data gaps;
- known contradictions;
- confidence penalty caused by missing evidence.

## 5. Multihorizon state matrix

| Horizon | State | Direction/rate of change | Priced gap | Dominant driver | Confidence | Half-life | Trigger | Invalidation | Conflict rule |
|---|---|---|---|---|---|---|---|---|---|
| Structural | | | | | | | | | |
| Secular | | | | | | | | | |
| Cyclical | | | | | | | | | |
| Tactical | | | | | | | | | |
| Swing | | | | | | | | | |
| Daily/session | | | | | | | | | |
| Event | | | | | | | | | |
| Microstructure | | | | | | | | | |

## 6. Economic and financial state

Cover the material components of growth, inflation, labor, policy, rates, fiscal, liquidity, credit, external balance and financial conditions.

## 7. Asset-specific state

Use the relevant market add-on and driver book. State what is not applicable.

## 8. Expectations and pricing gap

Separate:

- economic state;
- consensus;
- market-implied distribution;
- positioning;
- surprise;
- expected policy reaction;
- asset payoff.

## 9. Causal driver tree and rival models

For each driver label it direct, conditional, transmission, confirmation, flow, misleading correlation or rival explanation.

## 10. Cross-asset transmission map

State the expected sequence, leader, first confirmation, second confirmation, divergence warning and falsification response.

## 11. Positioning, volatility, liquidity and flow ecology

Distinguish observed facts from estimates. Include options, systematic and balance-sheet channels only when supported.

## 12. Catalyst map

Include scheduled events and non-event flows with date, time, timezone, expected information content and vulnerable assumption.

## 13. Scenario distribution

| Scenario | Probability range | Trigger | Causal path | Leader/confirmations | Horizon/half-life | Invalidation | Best expression | Main risk |
|---|---|---|---|---|---|---|---|---|

At least Base, Bullish, Bearish and Tail are required.

## 14. Permission and risk controls

Allowed values:

- `LONG_ONLY`
- `SHORT_ONLY`
- `TWO_WAY_REDUCED`
- `NO_TRADE`

Include confidence, size ceiling, mandatory confirmations, vetoes, invalidation, expiry, next catalyst, gap risk and portfolio concentration.

## 15. Technical handoff

State:

- permitted direction;
- prohibited direction;
- required technical condition;
- stand-down condition;
- stop sovereignty;
- no averaging into loss;
- time stop and thesis expiry.

## 16. Claim-evidence ledger

| ID | Label | Claim | Source | Timestamp/vintage | Supports/contradicts | Confidence |
|---|---|---|---|---|---|---|

Material claims must be traceable. Source lists without claim mapping are insufficient.

## 17. Unknowns and required data

State what cannot be known, why, and how it changes the conclusion.

## 18. Machine-readable context object

```yaml
research_object:
mode:
as_of:
timezone:
market_identity:
trade_vehicle:
vault_notes_used: []
data_quality:
  grade:
  missing_material_evidence: []
horizons:
  structural: {}
  secular: {}
  cyclical: {}
  tactical: {}
  swing: {}
  daily: {}
  event: {}
  microstructure: {}
priced_baseline:
vulnerable_assumption:
dominant_driver:
rival_models: []
causal_leader:
confirmations: []
divergence_warnings: []
positioning_liquidity_flow: {}
scenarios:
  base: {}
  bullish: {}
  bearish: {}
  tail: {}
permission:
confidence_range:
size_ceiling:
vetoes: []
fundamental_invalidation: []
time_expiry:
next_catalyst:
preferred_expression:
rejected_expressions: []
technical_handoff: {}
unknowns: []
```

## 19. Final quality-gate checklist

The model must visibly confirm:

- Vault opened and used;
- exact market/time resolved;
- current facts verified or historical cutoff preserved;
- claims cited and evidence labels used;
- pricing separated from state;
- rival model considered;
- horizon conflicts resolved;
- scenario probabilities coherent;
- permission, invalidation and expiry consistent;
- unknowns visible;
- YAML consistent with prose.

## Hard rejection conditions

Reject the result and redo the analysis if:

- the Vault was not used;
- the answer is generic or event-headline-only;
- historical lookahead is detected;
- a current claim lacks verification;
- the main priced assumption is absent;
- probabilities have no evidence basis;
- a material contradiction is ignored;
- directional permission lacks invalidation or expiry;
- technical risk control is subordinated to narrative conviction.
