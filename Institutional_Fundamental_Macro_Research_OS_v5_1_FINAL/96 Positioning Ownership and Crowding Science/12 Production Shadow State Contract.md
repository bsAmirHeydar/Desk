# Production Shadow State Contract

Required output per instrument:

```yaml
positioning_state:
  authority_mode: CANONICAL_SHADOW
  as_of_utc: ...
  horizon: ...
  coverage_state: ...
  observed_positions: []
  derived_positioning_states: []
  crowding_state: UNKNOWN
  fragility_state: UNKNOWN
  key_uncertainties: []
  evidence_ids: []
  independent_root_count: 0
  permission_effect_v18: NONE
```

The state is mandatory in V18 reporting when evidence is available or explicitly missing, but has no final permission authority until D3.
