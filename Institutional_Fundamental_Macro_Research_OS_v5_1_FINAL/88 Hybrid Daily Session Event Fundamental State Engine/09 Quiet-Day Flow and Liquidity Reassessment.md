---
title: "Quiet-Day Flow and Liquidity Reassessment"
type: canonical-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [quiet-day, flow, liquidity, proxy]
---
# Quiet-Day Flow and Liquidity Reassessment

A quiet calendar does not permit a blank day.

## Required checks

- continuation or delayed digestion of prior repricing;
- Treasury issuance, settlement, refunding and cash-balance effects;
- repo, funding and collateral conditions;
- options expiry, strike concentration and hedging proxies;
- month-end, quarter-end and benchmark rebalance;
- index reconstitution and passive flow;
- CTA, volatility-control and risk-parity proxies;
- buyback windows and blackout periods;
- FX fixings and hedging demand;
- short covering, liquidation and crowded unwind;
- liquidity deterioration, holiday effects and venue-specific depth;
- relative-value rotation and sector/country reallocation.

## Evidence labels

Every flow input must be labelled:

- `OBSERVED`
- `MODEL_IMPLIED`
- `PUBLIC_PROXY`
- `STRUCTURED_JUDGMENT`
- `UNAVAILABLE`

Do not claim dealer inventory, prime-broker books, CTA notional or proprietary flow without genuine access.

## Quiet-day outputs

A quiet-day reassessment must still update:

- state decay;
- confirmation;
- remaining pressure;
- move quality;
- persistence;
- edge availability;
- next catalyst.
