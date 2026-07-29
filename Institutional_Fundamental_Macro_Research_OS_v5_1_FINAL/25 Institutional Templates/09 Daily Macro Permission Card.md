---
title: "Daily Macro Permission Card"
type: template
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 25-institutional-templates
  - daily-macro-permission-card
  - institutional-fundamental
---
# Daily Macro Permission Card

> [!template] Operational artifact
> Copy this note into the current research period. Do not edit the canonical template.

| Section | Required entry |
|---|---|
| As-of and cutoff | Date, timezone, source cutoff, market snapshot |
| Decision target | Asset, horizon, action set, owner |
| State stack | Structural, cyclical, tactical, swing, daily, event, microstructure |
| Priced baseline | Consensus distribution, curves, options, valuation, positioning |
| New information | Observed facts, revisions, source timestamps |
| Scenarios | Probability, path, signposts, payoff, feedback |
| Transmission | Leader, confirmations, target, lag, expected half-life |
| Permission | Allowed direction, confidence, size ceiling, veto |
| Risk | Gap, liquidity, concentration, financing, invalidation, expiry |
| Attribution | Forecast, expression, timing, execution, cost, counterfactual |

## Working form

```yaml
template: "Daily Macro Permission Card"
as_of:
information_cutoff:
decision_owner:
asset:
horizon:
question:
observed_facts: []
derived_measurements: []
model_estimates: []
priced_baseline:
desk_distribution:
vulnerable_assumption:
scenarios:
  base:
    probability:
    path:
    signposts:
  upside:
    probability:
    path:
    signposts:
  downside:
    probability:
    path:
    signposts:
causal_leader:
independent_confirmations: []
contradictions: []
permission:
confidence:
size_ceiling:
fundamental_invalidation:
implementation_handoff:
expiry:
next_catalyst:
source_claim_ids: []
model_versions: []
post_decision_attribution:
```

## Completion rule

Blank fields mean `unknown`, not permission to invent a value. Store evidence under [[00 Core Standards/13 Claim Evidence Matrix Standard]] and evaluate the decision under [[00 Core Standards/07 Permission Proof and Incremental Edge]].
