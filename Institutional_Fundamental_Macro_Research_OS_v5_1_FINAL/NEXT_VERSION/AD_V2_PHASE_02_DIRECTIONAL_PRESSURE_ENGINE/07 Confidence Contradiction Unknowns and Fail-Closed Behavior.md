---
title: "Confidence Contradiction Unknowns and Fail-Closed Behavior"
type: scientific-contract
status: shadow-development
---
# Confidence, Contradiction and Unknowns

## Pressure magnitude versus confidence

Pressure magnitude describes the estimated causal force. Confidence describes evidence reliability/completeness. They are separate.

Target-price disagreement cannot mechanically reduce pressure magnitude or confidence in P02 because P02 does not yet own a Price Transmission diagnostic. P03 may lower model-completeness confidence after a transmission audit without mutating Pressure magnitude.

## Unknown applicable roots

An applicable but unavailable root remains in the economic denominator. In explicit-root aggregation it contributes a full uncertainty interval rather than disappearing.

This widens Pressure uncertainty and lowers coverage confidence.

## Contradiction load

Opposing roots are not erased. P02 reports the independent weight pointing against the resolved sign as `LOW`, `MEDIUM`, `HIGH` or `UNDETERMINED`.

## Fail closed

P02 fails closed for:

- target-price source kinds inside a pressure root;
- duplicate or dependent top-level roots;
- invalid ranges/weights;
- horizon mismatch;
- empirical half-life without validation reference;
- broken P00/P01 dependency;
- invalid P01 semantic integrity in legacy-wrap mode.
