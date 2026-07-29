---
title: "04 Multihorizon Inheritance and Conflict Resolution"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [multihorizon, regime, conflict-resolution]
---
# 04 Multihorizon Inheritance and Conflict Resolution

## Horizon architecture

| Horizon | Typical span | Primary question | Typical evidence |
|---|---:|---|---|
| Structural | 3–15+ years | What slow-moving constraints define the opportunity set? | demographics, productivity, institutions, capital stock, energy and fiscal capacity |
| Cyclical | 3–24 months | Where is the economy and policy cycle? | growth, inflation, labor, credit and financial conditions |
| Tactical | 2–12 weeks | Which expectation or risk premium is vulnerable? | policy path, supply calendar, revisions, positioning and valuation |
| Multi-day | 2–10 trading days | Which repricing has residual information and a credible half-life? | catalysts, flows, carry, liquidity and confirmation |
| Intraday | minutes–one session | What new information changed the distribution today? | release surprise, speech, auction, funding, cross-market response |
| Microstructure | seconds–hours | Can the decision be implemented without unacceptable cost or distortion? | depth, spread, impact, basis, auction and dealer constraints |

## Separate state objects

Each horizon must preserve its own:

- state distribution;
- prior and posterior;
- priced baseline;
- dominant causal model;
- rival model;
- catalyst set;
- expected half-life;
- invalidation;
- expiry;
- decision state.

Do not average conflicting horizons into a single undocumented score.

## Inheritance rules

- Structural analysis sets priors and constraints; it does not dictate short-horizon deployment.
- Cyclical analysis updates medium-horizon probabilities and expected policy responses.
- Tactical analysis identifies crowded expectations, supply events and risk-premium vulnerability.
- Multi-day analysis requires residual pricing gap and catalyst persistence.
- Intraday information may alter implementation or confidence without changing the structural state.
- A lower-horizon observation changes a higher-horizon state only when it is sufficiently persistent, broad, source-verified and statistically material.

## Conflict matrix

| Conflict | Required response |
|---|---|
| Structural favorable, cyclical adverse | reduce horizon, choose relative value, or wait for cyclical stabilization |
| Cyclical favorable, tactical overpricing | avoid paying for the thesis; seek a cleaner expression or no deployment |
| Multi-day thesis, intraday contradiction | suspend or reduce until the causal leader resolves |
| Fundamental thesis, adverse liquidity | reduce size, change instrument, delay or reject deployment |
| Same thesis across multiple positions | aggregate hidden exposure before approving risk |
| Competing models equally plausible | cap confidence and define discriminating evidence |

## Half-life discipline

Half-life is estimated from historical response decay, catalyst sequence and structural persistence. It must include uncertainty. The desk must not label a short-lived response as a campaign merely because the initial move was large.

## Escalation rule

A material horizon conflict must be visible in the investment-committee record. The final decision must state which horizon owns the risk, why, and what evidence transfers authority to another horizon.
