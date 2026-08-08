---
title: "Alpha Lab V16 — Institutional Full-Vault Production Prompt"
type: production-live-analysis-prompt
status: execution-ready
version: 16.0.0
language: en
output_language: fa
---
# Alpha Lab V16 — Institutional Full-Vault Production Prompt

Execute only after `CURRENT_PRODUCTION_MANIFEST.yaml` is resolved and preflight is PASS.

Universe is exactly XAUUSD, NASDAQ100, SP500, DJIA, EURUSD and USDJPY. WTI is not in the deployment profile.

## 0. Freeze and provenance
Create a run ID and freeze analysis cutoff. Record model identifier if available, prompt/version hashes if available, current Vault/git version if available, source cutoff and data availability. Never invent unavailable identifiers.

## 1. Evidence fabric while researching
For each load-bearing claim capture source, publication/retrieval time, first-release/revision state, observability class and root-cause ID. Build an evidence dependency graph. Descendants of one root event are transmission evidence, not independent votes.

## 2. Core science
Run V11 Fundamental, V12 Narrative and V13 instrument/asset-family science. Use dedicated DJIA and USDJPY V16 production books. Produce `CORE_EDGE_CANDIDATE`; do not assign final Active yet.

Narrative must distinguish validity, dominance, attention, flow control and price control. A price reaction may be reaction evidence but may not circularly prove the narrative that was inferred from the same reaction. Where material, perform a price-blind validity pass before reaction evidence is admitted.

## 3. V15.1 Timing
Run full Temporal Clearance. Timing never creates direction. Only `CLEAR` or `CLEAR_WITH_CONSTRAINTS` may clear an otherwise Active core candidate.

## 4. Global dependency firewall
Resolve shared root events across Fundamental/Narrative/Timing/cross-asset evidence. Unknown dependency cannot increase confidence. Material unresolved provenance/dependency failure → `INSUFFICIENT_EVIDENCE` / NO_TRADE.

## 5. Research Edge and calibration
Create Research Edge state. Query the forward reference class if available. Report calibration status exactly: COLD_START / DEVELOPING / ELIGIBLE_FOR_CALIBRATION / CALIBRATED_SHADOW / CALIBRATED_ENFORCED. Never convert an ordinal score to probability. Calibration is shadow unless governance explicitly promotes it.

## 6. Portfolio factor gate
Build the six-market factor map. Detect duplicated USD/rates/equity-beta/growth/vol/funding/root-event exposure. Current default mode is SHADOW. If policy is ENFORCED and a hard portfolio limit is breached, final permission is NO_TRADE for blocked candidates; Research Edge remains visible.

## 7. Operational gate
Check permission freshness/TTL, market/venue state, symbol mapping, source/bridge integrity if observable, and hard incident state. Any hard operational block → NO_TRADE for new entries. Do not reinterpret the research thesis.

## 8. Final output
For each symbol output separately:
- Core Direction
- Core Edge Candidate
- Timing Clearance
- Research Edge
- Calibration Status and sample sufficiency
- Portfolio Gate and factor concentration
- Operational Gate
- Final Permission BUY/SELL/NO_TRADE
- valid_until
- next review
- Why Not Active/Why Permission Blocked when applicable
- evidence/root-cause summary and material unknowns

The minimal execution JSON remains six symbols with `permission` and `valid_until_utc`; unknown/malformed/stale/expired means NO_TRADE downstream.

## 9. Execution and learning
M1 Donchian-20, 4ATR initial stop and candle-close trail are external mechanical execution only. Append run and outcome telemetry immutably. Compare CORE_ONLY, TIMING_GATED and (when available) PORTFOLIO_GATED shadow arms. Do not score unmatured horizons.

## 10. Validation
Run a blind second pass at minimum and label it honestly as same-model unless truly independent. Log disagreements. No single outcome may become Canonical.

HTML remains deep and Persian RTL. Email remains only Tehran timestamp plus `Symbol | Edge Level | Permission`.
