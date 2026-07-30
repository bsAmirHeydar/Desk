---
title: "02 Analysis Certification State Machine"
type: canonical-standard
status: canonical
version: 9.0.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, scientific-qa]
---

# Analysis Certification State Machine

## Purpose

The state machine prevents an assistant or analyst from jumping from a question directly to a confident narrative. Each state has explicit entry and exit conditions.

```text
QUERY_RECEIVED
→ OBJECT_RESOLVED
→ VAULT_DOMAINS_RETRIEVED
→ EVIDENCE_WINDOW_LOCKED
→ STATE_AND_PRICING_RECONSTRUCTED
→ CAUSAL_MODELS_CHALLENGED
→ SCENARIOS_AND_PAYOFFS_BUILT
→ OUTPUT_AUDITED
→ CERTIFIED | CONDITIONAL | REJECTED
```

## State definitions

### QUERY_RECEIVED

Record the exact request, desired mode, cutoff, timezone, horizon, instrument and special question. Ambiguous terms such as “oil”, “dollar”, “rates”, “Nasdaq” or “credit” require object resolution before research begins.

### OBJECT_RESOLVED

Define:

- economic object;
- tradable or reference instrument;
- geography and issuer;
- currency and settlement convention;
- contract month or index methodology where relevant;
- primary horizon and secondary horizons;
- live or historical mode.

No report advances if the object can refer to materially different instruments.

### VAULT_DOMAINS_RETRIEVED

Use the query taxonomy and coverage matrix to select the relevant domain MOCs, release monographs, country books, source registry entries and output contracts. Record a Vault Reading Ledger. Missing obvious domains is a certification failure.

### EVIDENCE_WINDOW_LOCKED

For live analysis, timestamp all market-sensitive facts and verify primary sources. For historical analysis, freeze the information cutoff, publication calendar and admissible vintages. Separate later audit evidence from the reconstructed decision set.

### STATE_AND_PRICING_RECONSTRUCTED

Build distinct estimates of:

- real economy or issuer state;
- policy and institutional state;
- market-implied expectations;
- valuation and risk premium;
- positioning, funding and liquidity;
- physical balance where applicable.

### CAUSAL_MODELS_CHALLENGED

Specify the primary model, at least two plausible rivals, mediating channels, expected leaders, confirming evidence, disconfirming evidence and falsifiers. Correlation alone cannot complete this state.

### SCENARIOS_AND_PAYOFFS_BUILT

Construct base, upside, downside and tail scenarios with probabilities or qualitative weights, signposts, payoff channels, horizon-specific half-lives, path dependence and update triggers.

### OUTPUT_AUDITED

Run all relevant gates, domain scorecard and benchmark tests. Check citations, contradictions, unknowns, consistency and output completeness.

### CERTIFIED / CONDITIONAL / REJECTED

The verdict must identify every failed or conditional gate. A report cannot self-upgrade from conditional to full through stronger wording.
