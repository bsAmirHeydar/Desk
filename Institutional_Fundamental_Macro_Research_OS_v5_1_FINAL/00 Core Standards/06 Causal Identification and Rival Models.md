---
title: "06 Causal Identification and Rival Models"
type: standard
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - institutional-standard
  - fundamental-research
  - governance
---
# 06 Causal Identification and Rival Models

> [!abstract] Purpose
> Prevent persuasive correlation from becoming a trade mechanism without identification, rival explanations, and leading evidence.

## Causal object

Define treatment/shock, outcome, timing, confounders, mediators, and forbidden post-treatment controls. Draw the assumed graph before estimating.

A causal claim should answer:

- What changed exogenously?
- Who was exposed and who was not?
- What would have happened otherwise?
- Which channel should move first?
- What observation would contradict the channel?

## Identification ladder

From weakest to strongest for a given claim:

1. descriptive co-movement;
2. temporal lead–lag;
3. conditional predictive relation;
4. natural experiment or discontinuity;
5. valid instrument/proxy shock;
6. structural restrictions supported by institutions;
7. replicated evidence across designs.

A trade may use predictive relations without claiming causality, but the limitation must be explicit.

## Methods

Use local projections for horizon responses, BVAR/SVAR for joint dynamics, fixed effects for repeated units, modern staggered DiD for treatment timing, IV with weak-instrument diagnostics, synthetic controls for singular interventions, and event studies for timestamped surprises.

## Rival model protocol

For every thesis include:

- policy-path explanation;
- term-premium/supply explanation;
- growth/cash-flow explanation;
- risk-premium/liquidity explanation;
- positioning/forced-flow explanation;
- measurement-error explanation.

Specify the first market or data sign that distinguishes them.

## Causal leader

The leader is the market closest to the mechanism, not the market that moved first by chance. Examples: meeting-dated rates for policy; products/cracks and curve for refinery tightness; cross-currency basis for dollar funding; credit/bank funding for intermediation stress.

## Rejection

Reject or reduce the claim when the leader fails, an independent confirmation contradicts it, the effect occurs before treatment, sensitivity to controls is extreme, or a placebo produces the same result.
