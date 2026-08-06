---
title: "Fundamental Force Consumption Persistence and Asymmetry Calibration Engine"
type: moc
status: canonical
version: 13.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Fundamental Force Consumption Persistence and Asymmetry Calibration Engine

## Mission

Module 89 is the canonical V11 control layer for measuring and communicating fundamental force, consumption, repricing completion, remaining pressure, persistence, reversal hazard, path asymmetry and edge availability. It preserves the V10.4 hybrid recording engine while adding field-level provenance, horizon-indexed state vectors, confidence caps and an explicit bridge from ordinal judgment to empirical calibration.

## Non-negotiable interpretation

- **Force is a vector before it is a score.**
- **Consumption is a vector, not elapsed time or price distance.**
- **Remaining pressure is a residual causal state, not `100 - consumption`.**
- **Direction is not edge availability.**
- **Ordinal scores are not probabilities.**
- **Unavailable institutional data lower confidence; they are never invented.**
- **Historical analysis is frozen at the information cutoff.**
- **Fundamental asymmetry is a payoff-state handoff, not a chart entry rule.**

## Reading route

### Ontology and force

- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/01 Honest Ten-of-Ten Definition and Scope]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/02 Fundamental State Variable Ontology]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/03 Fundamental Force and Intensity Decomposition]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/04 Surprise Materiality and Expectation Revision]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/05 Transmission Breadth Depth and Independence]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/06 Institutional Amplification and Constraint Multipliers]]

### Consumption, persistence and asymmetry

- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/07 Consumption Vector and Lifecycle]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/08 Information Absorption Measurement]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/09 Repricing Completion and Counterfactual Baselines]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/10 Flow Positioning and Mechanical Exhaustion]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/11 Narrative Saturation Consensus and Crowding]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/12 Catalyst Freshness Reinforcement and Reopening]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/13 Remaining Fundamental Pressure Decomposition]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/14 Persistence Half-Life and State Survival]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/15 Exhaustion Reversal Hazard and Thesis Failure]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/16 Fundamental Path Asymmetry and Edge Availability]]

### Horizon, regime, confirmation and evidence

- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/17 Horizon-Specific State Vectors]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/18 Regime-Conditional Interpretation and Structural Breaks]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/19 Cross-Asset Confirmation and Causal-Leader Adjudication]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/20 Observability Data Tiers and Confidence Caps]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/21 Score Provenance Intervals and False-Precision Control]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/22 Analyst Reproducibility and Adjudication Protocol]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/23 Historical Point-in-Time Calibration Laboratory]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/24 Purged Walk-Forward Validation and Model Retirement]]

### Asset books and event atlases

- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/25 Nasdaq 100 Force Consumption and Persistence Book]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/26 S&P 500 Force Consumption and Persistence Book]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/27 Gold Force Consumption and Persistence Book]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/28 EURUSD Force Consumption and Persistence Book]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/29 Scheduled Event Atlas]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/30 Unscheduled Event and Headline Shock Atlas]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/31 Quiet-Day Non-Event and Slow-Burn State Change]]

### Schema, validation, migration and prompt

- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/32 Machine-Readable V11 State Schema]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/33 Scoring Ledger and Analyst Worksheet]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/34 Benchmark Scenarios and Acceptance Tests]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/35 Regression Preservation Suite]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/36 Migration Precedence and Backward Compatibility]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/37 Residual Frontiers and Research Agenda]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/38 Alpha Lab V11 Full-Spectrum Fundamental State Analysis Prompt]]
- [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/39 V11 Fast Launcher]]


## Precedence

For methodology version 11.0.0, this module governs the semantics of force, intensity, the V11 consumption vector, remaining pressure, persistence, reversal hazard, path asymmetry and edge availability. Module 88 continues to govern mandatory daily/session/event record density and immutable point-in-time reconstruction. Module 87 continues to govern Persian PDF delivery. Module 81 continues to govern internal scientific QA. Conflicts are resolved through `V11_CANONICAL_AUTHORITY_MAP.yaml`.

## V12 narrative handoff

After V11 produces the fact-state vector, hand it to [[90 Market Narrative Intelligence Engine/00 Market Narrative Intelligence Engine MOC]]. V12 must not overwrite V11 fact force, consumption, remaining pressure, fact persistence or asymmetry.



## V13 universal multi-asset coverage

Module 91 adds universal resolution, FX/commodity/index adapters, watchlists, ranking and relative value. Start at [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/00 Global Multi-Asset Coverage and Instrument Intelligence Engine MOC]]. V11 and V12 authorities remain intact.
