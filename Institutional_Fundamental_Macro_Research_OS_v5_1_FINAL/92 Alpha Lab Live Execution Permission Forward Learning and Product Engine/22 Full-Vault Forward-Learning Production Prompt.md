---
title: "Alpha Lab V15.1 Full-Vault Forward-Learning Six-Market Production Prompt"
type: production-live-analysis-prompt
status: execution-ready
version: 15.1.0
language: en
output_language: fa
---
# Alpha Lab V15.1 — Full-Vault Forward-Learning Production Prompt

Execute FULL-VAULT / ZERO-SHORTCUT / FORWARD-LEARNING analysis for XAUUSD, NASDAQ100, SP500, DJIA, EURUSD and USDJPY.

## Phase 1 — Core science
Run V11 (force/consumption/remaining pressure/persistence/reversal/asymmetry), V12 (attention/narrative/validity/dominance/reflexivity/transition) and V13 (instrument/asset-family science) independently for all six markets. Produce `CORE_EDGE_CANDIDATE`; **do not assign final EDGE_ACTIVE yet**.

## Phase 2 — Mandatory Timing clearance
Run [[93 Temporal Market Structure Timing and Calendar Intelligence Engine/60 V15.1 Full-Vault Timing Clearance Production Prompt]] for every symbol and the shared global clock graph.

Timing uses factual institutional clocks, not technical price analysis. Resolve current official schedules, source freshness, product/reference-market identity, timezone/DST/business/settlement days, sessions/handoffs, macro/central-bank/Treasury clocks, WMR/LBMA benchmarks, cash open/close, futures settlement/roll/expiry/SOQ, options expiry/AM-PM/EOM, index rebalance, earnings/corporate clocks, month/quarter/year-end, funding/payment-system clocks, holidays/half-days, schedule revisions/TBD status, safe execution time budget, latency/TTL and scheduler feasibility.

## Phase 3 — Final Edge
Apply [[93 Temporal Market Structure Timing and Calendar Intelligence Engine/54 Timing Gate to Final Edge Transition Matrix]]. Final `EDGE_ACTIVE` is legal only when:
- core candidate = `ACTIVE_CANDIDATE_BULL` or `ACTIVE_CANDIDATE_BEAR`;
- timing gate = `CLEAR` or `CLEAR_WITH_CONSTRAINTS`;
- safe execution window = sufficient;
- no material timing unknown/hard blocker;
- permission expiry precedes the earliest hard hazard.

Permission mapping remains deterministic: Active Bull → BUY; Active Bear → SELL; everything else → NO_TRADE.

## Phase 4 — External execution
Entry remains M1 Donchian-20 on prior completed bars; initial stop 4 ATR; exit candle-close trailing. Donchian never supplies fundamental or timing direction. Permission controls new entries only.

## Phase 5 — Learning
Audit prior core and timing calls only after their relevant windows mature. Maintain immutable states, Hindsight Firewall and Observation→Candidate→Validated→Canonical governance. Compare `CORE_ONLY` versus `TIMING_GATED` shadow performance so Timing cannot hide behind lower trade frequency.

## Deep output
HTML must show separately: Core Direction, Core Edge Candidate, Timing Clearance, Final Edge, Permission, valid_until, next review, Global Clock, per-market Timing Intelligence, and full `Why Not Active?` for every Conditional.

Email remains only timestamp + six rows `Symbol | Edge Level | Permission`, no attachments.
