# V18 D2 Production Output Contract

Every run should expose a compact D2 section even if all domains are missing:

```yaml
d2_shadow:
  version: 1.0.0
  authority_mode: CANONICAL_SHADOW
  instrument: ...
  analysis_cutoff_utc: ...
  positioning: {...}
  actual_flow: {...}
  funding_plumbing: {...}
  institutional_mechanics: {...}
  market_capacity: {...}
  cross_science_independent_roots: 0
  missing_or_licensed_required: []
  d2_permission_effect: NONE
  d3_promotion_state: NOT_PROMOTED
```

Final decision is then reported separately from the existing V17 stack.


## V21.3 observability extension

For production runs using D2 pack `1.1.0`, `observability_receipt` is mandatory. The receipt records `baseline_materiality` from the six-market map and a context-sensitive `runtime_materiality`. Runtime materiality may differ only with an explicit reason; the family may not disappear from the receipt. Private/licensed gaps remain explicit and never become facts through proxy substitution.
