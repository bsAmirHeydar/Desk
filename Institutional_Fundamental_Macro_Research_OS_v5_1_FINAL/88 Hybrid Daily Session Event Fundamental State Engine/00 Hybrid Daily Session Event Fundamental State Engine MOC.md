---
title: "Hybrid Daily Session Event Fundamental State Engine"
type: moc
status: canonical
version: 13.0.0
created: 2026-08-01
updated: 2026-08-06
language: en
tags: [point-in-time, intraday-fundamental, historical-reconstruction, session, state-decay]
---
# Hybrid Daily Session Event Fundamental State Engine

This module is the governing architecture for dense live and historical fundamental-state reconstruction. It replaces sparse event-only recording with a hybrid system:

`DAILY BASELINE → SESSION REASSESSMENT → EVENT UPDATE → MICRO-WINDOWS → STATE DECAY → CROSS-ASSET CONFIRMATION → END-OF-DAY ATTRIBUTION`

## Canonical standards

- [[88 Hybrid Daily Session Event Fundamental State Engine/01 Architecture and Horizon Separation]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/02 Record Types and Mandatory Coverage]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/03 Session Clocks and Handoff Protocol]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/04 Scheduled and Unscheduled Event Micro-Windows]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/05 State Decay and No-Change Reassessment]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/06 Adaptive Materiality and Change Thresholds]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/07 Direction Usability and Edge Availability]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/08 Cross-Asset Confirmation and Causal-Leader Changes]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/09 Quiet-Day Flow and Liquidity Reassessment]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/10 Nasdaq 100 Fast Medium and Slow Driver Stack]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/11 S&P 500 Fast Medium and Slow Driver Stack]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/12 Gold Fast Medium and Slow Driver Stack]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/13 EURUSD Fast Medium and Slow Driver Stack]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/14 Hybrid Fundamental State Schema]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/15 Historical 100-Day Reconstruction Output Contract]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/16 Density Coverage and Gap Validation Standard]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/17 No-Lookahead and Immutable-State Audit]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/18 End-of-Day Attribution and Carry-Forward]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/19 Benchmark Scenarios and Acceptance Tests]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/20 Implementation and Migration Map]]

## Production prompt

- [[75 ChatGPT Institutional Market Analysis Prompts/17 Four-Market 100-Day Hybrid Point-in-Time Reconstruction Prompt]]
- [[75 ChatGPT Institutional Market Analysis Prompts/18 Hybrid Reconstruction Output and Density Contract]]
- [[75 ChatGPT Institutional Market Analysis Prompts/19 Hybrid Reconstruction Fast Launcher]]

## Doctrine

A valid state exists for every open trading day. Direction may remain unchanged while intensity, freshness, absorption, repricing completion, flow exhaustion, confirmation, persistence, remaining pressure, reversal risk and edge availability change. Mandatory reassessment is not a claim that fundamentals changed; it is evidence that the desk checked whether they changed.

---

## V11 compatibility bridge

Module 88 remains the governing architecture for:

- daily/session/event/no-change record density;
- scheduled and unscheduled micro-windows;
- state-decay reassessment;
- causal-leader changes;
- immutable point-in-time reconstruction;
- end-of-day attribution.

Module 89 extends the content of each state record with force, consumption, counterfactual repricing, remaining pressure, persistence, reversal hazard, path asymmetry, provenance and calibration fields:

- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/00 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine MOC]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/32 Machine-Readable V11 State Schema]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/36 Migration Precedence and Backward Compatibility]]

## V12 narrative child state

Module 88 continues to govern mandatory checkpoints and immutable record density. A V12 narrative record may attach to each daily/session/event state using [[90 Market Narrative Intelligence Engine/45 Machine-Readable V12 Narrative State Schema]].



## V13 universal multi-asset coverage

Module 91 adds universal resolution, FX/commodity/index adapters, watchlists, ranking and relative value. Start at [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/00 Global Multi-Asset Coverage and Instrument Intelligence Engine MOC]]. V11 and V12 authorities remain intact.
