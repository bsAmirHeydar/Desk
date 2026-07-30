---
title: "12 Scenario Tail and Update Gate"
type: canonical-standard
status: canonical
version: 9.0.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, scientific-qa]
---

# Scenario, Tail and Update Gate

## Scenario architecture

At minimum construct:

- base scenario;
- meaningful upside alternative;
- meaningful downside alternative;
- at least one nonlinear or tail scenario when material.

Scenarios must be mutually interpretable, collectively broad enough for the decision and linked to observable signposts.

## Required fields

```yaml
scenario:
probability_or_weight:
initial_conditions:
causal_path:
first_market_leaders:
asset_payoff_by_horizon:
liquidity_and_funding_effects:
second_round_feedbacks:
confirmation_signposts:
falsifiers:
expiry:
```

## Tail analysis

Tail states require more than adding a severe percentage move. Identify:

- trigger;
- nonlinear balance-sheet mechanism;
- forced buyers or sellers;
- collateral and margin effects;
- policy reaction capacity;
- market closure, basis or liquidity risk;
- recovery or persistence mechanism.

## Updating

Use Bayesian discipline qualitatively or quantitatively. New evidence updates the scenario distribution according to diagnosticity, independence and reliability. A noisy indicator should not move probability as much as a direct institutional or physical observation.

## Veto conditions

- scenarios differ only by arbitrary numeric magnitude;
- probabilities sum incorrectly or imply false precision;
- no signposts or update rules exist;
- the tail ignores funding, collateral or institutional response;
- the base scenario is merely the analyst's preferred narrative.
