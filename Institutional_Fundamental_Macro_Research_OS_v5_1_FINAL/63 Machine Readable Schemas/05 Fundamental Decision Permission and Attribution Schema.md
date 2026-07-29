---
title: "05 Fundamental Decision Permission and Attribution Schema"
type: schema
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - schema
  - machine-readable
  - research-governance
---
# 05 Fundamental Decision Permission and Attribution Schema

```yaml
schema_version: 5.0.0
decision_id: string
context_id: string
timestamp: datetime
asset: string
horizon: string
permission: [LONG_ONLY, SHORT_ONLY, TWO_WAY_REDUCED, NO_TRADE]
confidence: number
size_ceiling: number
chosen_expression: string|null
implementation_condition_id: string|null
fundamental_invalidation: [string]
risk_limit: string|null
expiry: datetime
execution:
  order_type: string|null
  decision_price: number|null
  fills: [object]
  implementation_shortfall: number|null
outcome:
  gross_pnl: number|null
  net_pnl: number|null
  max_adverse_excursion: number|null
  max_favorable_excursion: number|null
attribution:
  state_estimation: number|null
  pricing_gap: number|null
  expression: number|null
  timing: number|null
  sizing: number|null
  execution: number|null
  carry_convexity: number|null
  residual: number|null
counterfactuals: [object]
```
