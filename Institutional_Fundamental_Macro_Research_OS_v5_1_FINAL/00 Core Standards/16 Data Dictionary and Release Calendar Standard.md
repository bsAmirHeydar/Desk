---
title: "16 Data Dictionary and Release Calendar Standard"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [data-dictionary, release-calendar, metadata]
---
# 16 Data Dictionary and Release Calendar Standard

## Series dictionary

Each series or document field must include:

```yaml
series_id:
official_name:
source_id:
source_locator:
concept_definition:
unit:
frequency:
reference_period:
population_or_coverage:
seasonal_adjustment:
price_or_volume_basis:
release_timestamp_rule:
timezone:
first_release_available:
revision_schedule:
benchmark_revision_policy:
transformation_chain:
known_breaks:
expected_lead_lag:
relevant_horizons:
relevant_assets:
quality_flags:
license_classification:
owner:
```

## Calendar controls

The release calendar must distinguish scheduled timestamp, actual timestamp, delay, early release, embargo, holiday adjustment and daylight-saving conversion. A calendar event is linked to the exact source artifact and to all observations published in the release.

## Transformation registry

Every transformation receives an ID and version: logarithm, annualization, diffusion, contribution, chain weighting, seasonal adjustment, interpolation, mixed-frequency aggregation, curve construction, winsorization or normalization.

## Break management

Methodology changes, reclassifications, benchmark revisions, sample redesigns and discontinuities must create explicit break records. The platform must not splice series silently.
