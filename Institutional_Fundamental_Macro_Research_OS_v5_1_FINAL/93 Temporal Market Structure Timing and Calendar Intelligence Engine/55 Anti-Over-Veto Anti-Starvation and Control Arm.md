---
title: "Anti-Over-Veto, Anti-Starvation and Control Arm"
type: canonical-validation-standard
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, validation, over-veto]
---
# Anti-Over-Veto, Anti-Starvation and Control Arm

A timing filter that blocks nearly everything can look safe while destroying opportunity. V15.1 explicitly treats **over-veto** as model risk.

## Veto discipline
A calendar label alone cannot block a trade. Month-end, Friday, expiry day, London open, cash open, quarter-end or an event later in the day require a material mechanism and a safe-window test.

## Prefer the least restrictive correct action
`NO_CHANGE` → `EARLY_REVIEW` → `SHORTEN_VALIDITY / CLEAR_WITH_CONSTRAINTS` → `HOLD` → `VETO`.

## Forward control arms
Maintain at least:
1. `CORE_ONLY`: fundamental/narrative eligible + Donchian execution;
2. `TIMING_GATED`: same core candidate + V15.1 clearance + identical Donchian execution.

Optional shadow arm: `TIMING_CONSTRAINED_ONLY`, where timing may shorten validity but not veto, to isolate the cost of hard vetoes.

## Metrics
- percentage of core active candidates cleared;
- `HOLD` and `VETO` rates by clock family;
- permission minutes lost to timing;
- over-veto and under-veto classifications after mature outcomes;
- no-trigger-before-expiry rate;
- event-reset avoidance;
- expectancy/PF/DD difference vs CORE_ONLY once sample is sufficient;
- market/regime concentration of timing benefit;
- false clock dominance rate;
- stale-permission prevention rate.

## Governance
Do not loosen the gate merely to create more trades and do not tighten it merely to reduce drawdown in one sample. Threshold changes require forward evidence and rival-model review.
