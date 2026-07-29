---
title: "17 Context Object and Permission Schema Standard"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [context-object, schema, decision-state]
---
# 17 Context Object and Permission Schema Standard

## Canonical object

```yaml
context_id:
target:
instrument_universe:
cutoff_timestamp:
timezone:
horizon:
source_snapshot_ids: []
data_vintages: []
model_versions: []
structural_state:
cyclical_state:
tactical_state:
multi_day_state:
intraday_state:
market_implied_distribution:
consensus_distribution:
pricing_gap:
causal_models: []
rival_models: []
causal_leader:
independent_confirmations: []
contradictions: []
scenario_distribution: []
expected_half_life:
carry_and_financing:
liquidity_and_capacity:
portfolio_exposures: []
decision_state:
confidence_cap:
risk_budget:
scenario_loss_limit:
information_invalidation:
time_expiry:
implementation_constraints: []
claim_ids: []
unknowns: []
reviewer:
approval_status:
```

## Decision-state rules

Use the vocabulary in [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]. The object must preserve the reasoning path; a score without distributions and evidence is invalid.

## Versioning

Every update creates a new immutable version. Changes must identify whether they arise from new data, revised data, model change, judgment change, risk constraint or portfolio change.
