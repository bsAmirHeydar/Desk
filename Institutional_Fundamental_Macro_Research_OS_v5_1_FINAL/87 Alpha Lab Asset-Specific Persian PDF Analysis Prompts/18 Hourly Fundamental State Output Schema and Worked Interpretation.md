---
title: "Alpha Lab Hourly Fundamental State Output Schema and Worked Interpretation"
type: output-schema
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [alpha-lab, hourly, schema, interpretation]
---
# Alpha Lab Hourly Fundamental State Output Schema and Worked Interpretation

## Machine-readable state object

```yaml
hourly_fundamental_state:
  record_id:
  parent_record_id:
  record_type:
  mandatory_checkpoint:
  checkpoint_completed:
  timestamp:
  timezone:
  market:
  instrument:
  session:
  observation_status: observed | estimated | conditional
  update_status: material_change | no_material_update | event_update
  direction_code:
  direction_score:
  direction_score_type: empirically_calibrated | model_implied | judgmental_ordinal
  intensity_0_100:
  confidence_0_100:
  state_phase:
  consumption:
    information_absorption_0_100:
    repricing_completion_0_100:
    flow_exhaustion_0_100:
    narrative_saturation_0_100:
    catalyst_freshness_0_100:
    remaining_fundamental_pressure_0_100:
    summary_code:
  causal_stack:
    primary_driver:
    reinforcing_driver:
    opposing_driver:
    driver_concentration_0_100:
  cross_asset_confirmation_0_100:
  move_quality:
  surprise_vector:
    headline:
    composition:
    revision:
    policy_reaction:
    positioning_liquidity:
  persistence_code:
  estimated_half_life:
  reversal_risk_0_100:
  path_asymmetry:
  edge_availability:
  invalidation:
  upgrade_trigger:
  downgrade_trigger:
  next_catalyst:
  next_mandatory_update:
  change_from_prior_snapshot:
  unavailable_inputs: []
  evidence_ledger: []
```

## Worked interpretation

Example only; values are illustrative and must not be reused without evidence.

```yaml
hourly_fundamental_state:
  timestamp: "10:00 America/New_York"
  market: "Nasdaq 100"
  observation_status: observed
  update_status: material_change
  direction_code: NEGATIVE
  direction_score: -55
  direction_score_type: judgmental_ordinal
  intensity_0_100: 70
  confidence_0_100: 65
  state_phase: STRENGTHENING
  consumption:
    information_absorption_0_100: 45
    repricing_completion_0_100: 40
    flow_exhaustion_0_100: 25
    narrative_saturation_0_100: 35
    catalyst_freshness_0_100: 85
    remaining_fundamental_pressure_0_100: 70
    summary_code: PARTIALLY_CONSUMED
  causal_stack:
    primary_driver: "higher real yields after a policy-path repricing"
    reinforcing_driver: "weaker semiconductor earnings guidance"
    opposing_driver: "stable credit spreads"
    driver_concentration_0_100: 60
  cross_asset_confirmation_0_100: 70
  move_quality: FUNDAMENTALLY_CONFIRMED
  persistence_code: MULTI_HOUR_2_4H
  reversal_risk_0_100: 35
  path_asymmetry: DOWNSIDE_DOMINANT
  edge_availability: MODERATE_FUNDAMENTAL_EDGE
```

Plain-Persian interpretation:

> جهت بنیادی در این ساعت منفی و شدت فشار نسبتاً زیاد است. محرک هنوز تازه است و فقط بخشی از بازقیمت‌گذاری انجام شده؛ بنابراین فشار نزولی باقی‌مانده همچنان قابل‌توجه است. با این حال، ثبات بازار اعتبار یک نیروی مخالف است و اعتماد تحلیل را محدود می‌کند. اگر بازده واقعی برگردد یا credit بهبود معنادار نشان دهد، حالت باید دوباره ارزیابی شود.
## V10.4 hybrid extension

For historical datasets, use the complete schema in [[88 Hybrid Daily Session Event Fundamental State Engine/14 Hybrid Fundamental State Schema]]. Hourly state objects must include record type, parent record, mandatory checkpoint, session stage, state-decay basis, before/after cross-asset confirmation and edge availability.
