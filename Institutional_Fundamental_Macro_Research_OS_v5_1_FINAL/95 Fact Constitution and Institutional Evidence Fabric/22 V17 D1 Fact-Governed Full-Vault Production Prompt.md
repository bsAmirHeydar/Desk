---
title: "Alpha Lab V17 D1 — Fact-Governed Full-Vault Production Prompt"
type: production-live-analysis-prompt
status: execution-ready
version: 17.0.0
language: en
output_language: fa
---
# Alpha Lab V17 D1 — Fact-Governed Full-Vault Production Prompt

Run only after `95 .../tools/alphalab_d1_preflight.py --mode runtime` returns PASS.

Production universe is exactly XAUUSD, NASDAQ100, SP500, DJIA, EURUSD and USDJPY. Crude oil is outside this profile.

## 0. Freeze the epistemic frame
Freeze `run_id`, symbol, `analysis_cutoff_utc`, manifest/Vault version, model identity if available, and source cutoff. Do not invent timestamps, access, institutional flow or unavailable metadata.

## 1. Build the smallest sufficient retrieval plan
Use the V16.1 retrieval firewall. Canonical/current authorities are load-bearing; archived/supporting legacy notes are history/reference only unless explicitly requested in history mode.

## 2. Construct governed Fact Records
For every load-bearing claim expose:
- primary fact/inference class;
- source tier and source locator/snapshot ID;
- event/reference/effective/publication/first-seen/retrieval/ingestion/validity/supersession clocks when applicable;
- release family/vintage/revision lineage;
- parent fact IDs and derivation method for derived records;
- root cause ID where known;
- decision materiality;
- availability state.

Never convert `PUBLIC_PROXY`, `MODEL_INFERENCE`, `NARRATIVE_INFERENCE` or `SCENARIO_ASSUMPTION` into a direct observation by wording.

## 3. Enforce point-in-time visibility
At the analysis cutoff exclude future publications and revisions. Unknown publication time may not be backfilled. Decision-critical unresolved visibility -> HOLD. Material noncritical uncertainty -> confidence/validity cap where the remaining evidence is sufficient.

## 4. Build dependency-aware Decision Evidence Pack
Same-root descendants are not independent votes. If root independence is unresolved and decision-critical, do not fabricate confidence. Record the unresolved dependency.

## 5. Produce Fact Coverage Receipt
For all ten fact families declare retrieved/limited/unavailable/D2-pending status, direct-vs-proxy mix, source tiers, material gaps and decision effect.

## 6. D1 admission gate
Proceed only when the evidence pack is record-valid, historically eligible and decision-sufficient under materiality. Otherwise return `NO_TRADE`/`HOLD` with exact reason; do not repair evidence with hindsight.

## 7. Delegate to validated V16.1 science
Run the V16.1 integrated production engine as a subengine. Preserve its authority map:
- Fundamental = sole direction authority;
- Narrative = transmission clearance;
- Timing = temporal clearance;
- Calibration = SHADOW;
- Portfolio = SHADOW;
- Operational = ENFORCED.

D1 does not let Positioning/Flow/Plumbing/Mechanics/Capacity create new direction or veto rules before D2 validation.

## 8. Final output per symbol
Return in Persian:
- Fundamental Direction and Force State;
- Narrative Transmission Clearance;
- D1 Evidence Admission status;
- decision-critical unknowns;
- root-cause dependency notes;
- Fact Coverage Receipt summary;
- Timing Clearance;
- Research Edge;
- confidence/validity caps;
- Calibration/Portfolio shadow diagnostics;
- Operational Gate;
- Final Permission `BUY|SELL|NO_TRADE`;
- `valid_until_utc` and `next_review_utc`;
- exact reason for HOLD/NO_TRADE.

## 9. Execution boundary
M1 Donchian-20, 4ATR initial stop and candle-close trailing remain external mechanical execution only. Price technical analysis may not create Fundamental direction or Timing clearance.

## 10. Immutable learning
Preserve the Decision Evidence Pack, Fact Coverage Receipt and output hash/reference for later outcome attribution. New revisions create a new run; never rewrite the old one.
