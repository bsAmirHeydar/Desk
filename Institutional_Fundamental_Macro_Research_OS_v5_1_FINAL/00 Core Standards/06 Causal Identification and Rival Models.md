---
title: "06 Causal Identification and Rival Models"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [causal-inference, rival-models, identification]
---
# 06 Causal Identification and Rival Models

## Principle

Co-movement is not a mechanism. A research claim is causal only when the identification strategy explains why the variation used is plausibly exogenous to the outcome or when the desk explicitly limits the claim to a conditional predictive relation.

## Causal workflow

1. Define the intervention, shock or information event.
2. Specify the causal graph and timing.
3. Identify confounders, mediators, colliders and feedback loops.
4. State the identifying assumption.
5. Select an admissible design.
6. Predeclare the causal leader and lag structure.
7. Estimate uncertainty and sensitivity.
8. Test rival models that predict similar target movement.
9. Report where the design fails.

## Admissible designs

- randomized or quasi-random assignment where available;
- high-frequency event identification;
- narrative or proxy structural shocks;
- instrumental variables;
- local projections and state-dependent responses;
- difference-in-differences with credible parallel trends;
- synthetic controls;
- regression discontinuity;
- panel designs with appropriate fixed effects and clustered uncertainty;
- accounting decompositions when the claim is identity-based rather than causal;
- predictive models explicitly labeled non-causal.

## Required rival models

At least one rival must explain the same target movement through a materially different mechanism. Examples:

- growth news versus term-premium shock;
- policy repricing versus Treasury supply;
- safe-haven demand versus forced deleveraging;
- physical shortage versus financial positioning;
- earnings revision versus discount-rate compression;
- dollar funding stress versus domestic monetary divergence.

## Discriminating evidence

A good research object names evidence that differs across models: which curve point moves, whether credit confirms, whether physical basis tightens, whether option skew changes, whether volumes and funding spreads respond, or whether the effect survives after the event window.

## Failure modes

- selecting the narrative after observing the target move;
- using the target price as both evidence and outcome;
- conditioning on a mediator or collider;
- ignoring anticipation and information leakage;
- assuming stable coefficients across regimes;
- treating sign-consistent correlations as causal proof;
- failing to cluster or adjust uncertainty;
- omitting policy endogeneity;
- using revised data in historical identification.
