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
