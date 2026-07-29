---
title: "01 Research Object and Decision Contract"
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
# 01 Research Object and Decision Contract

> [!abstract] Purpose
> Convert a vague market question into a time-stamped, falsifiable research object with an explicit decision owner, horizon, action set, risk ceiling, and expiration.

## The decision object

Institutional fundamental work is not a collection of facts. It is a contract between research and capital allocation. Every research object must specify:

1. **Target variable** — the economic state, market price, spread, curve, cash flow, or probability being estimated.
2. **Decision horizon** — structural, cyclical, tactical, swing, daily, event, or microstructure.
3. **Information cutoff** — the exact timestamp beyond which evidence is prohibited.
4. **Priced baseline** — the distribution already embedded in curves, options, consensus, positioning, or valuation.
5. **Alternative scenarios** — paths, probabilities, signposts, and feedback.
6. **Expression** — instrument, direction, relative-value leg, optionality, and intended holding period.
7. **Permission** — `LONG_ONLY`, `SHORT_ONLY`, `TWO_WAY_REDUCED`, or `NO_TRADE`.
8. **Risk contract** — size ceiling, expected gap, liquidity assumptions, invalidation, and expiry.
9. **Owner and veto** — who can approve, challenge, reduce, or terminate the position.
10. **Learning record** — forecast, execution, P&L, counterfactual, and attribution.

A research note that cannot fill these fields is educational material, not a deployable decision object.

## Research types

Separate four objects that are often mixed:

| Object | Question | Valid output |
|---|---|---|
| Measurement | What was observed and how reliable is it? | Point-in-time fact with uncertainty |
| State estimation | What latent condition best explains the evidence? | Probability distribution |
| Forecast | What is likely to happen over a defined horizon? | Density, not slogan |
| Trade decision | Is the expected payoff superior after pricing, cost, and risk? | Permission and risk budget |

A correct state estimate does not imply a profitable trade. The state can be known, fully priced, expressed in the wrong instrument, overwhelmed by a different exposure, or realized on the wrong horizon.

## Decision contract

```yaml
research_object:
  as_of:
  information_cutoff:
  target:
  asset:
  horizon:
  state_distribution:
  expectation_distribution:
  priced_distribution:
  vulnerable_assumption:
  scenarios:
  causal_leader:
  independent_confirmations:
  expression:
  permission:
  confidence:
  size_ceiling:
  fundamental_invalidation:
  technical_handoff:
  expiry:
  next_catalyst:
  owner:
  veto_owner:
  evidence_packet:
  model_version:
```

## Minimum acceptance tests

A research object cannot enter production unless:

- all observations existed at the cutoff;
- source, units, seasonal treatment, and revision policy are known;
- the priced baseline is measured rather than guessed;
- at least one credible rival explanation is retained;
- the expected leader is named before the target moves;
- action thresholds are defined before observing the outcome;
- liquidity and cost are included;
- the technical entry and structural stop remain independent;
- probability statements can later be scored;
- the decision can be reconstructed without the analyst.

## Separation of duties

Research estimates states and distributions. The portfolio manager chooses exposure. Independent risk constrains concentration and survival. Execution chooses order type, timing, and venue. Attribution determines whether the result came from state, pricing, expression, timing, execution, or noise.

No role may retroactively rewrite another role's record.

## Related standards

- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Execution Handoff]]
