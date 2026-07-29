---
title: "01 Institutional Query Taxonomy and Analysis Object Contract"
type: institutional-standard
status: canonical
version: 6.3.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-analysis, fundamental-only, analysis-canon]
---

# Institutional Query Taxonomy and Analysis Object Contract

## Query classes

- Current full-spectrum market state
- Historical point-in-time reconstruction
- Asset driver and valuation analysis
- Country, sovereign and policy analysis
- Company, industry and equity analysis
- Commodity physical-system analysis
- Event, data release and policy catalyst analysis
- Cross-asset relative-value analysis
- Portfolio hidden-exposure and scenario analysis
- Structural regime and long-horizon analysis

## Mandatory object fields

```yaml
analysis_object:
object_type:
instrument_or_entity:
jurisdiction:
cutoff_timestamp:
information_set:
primary_horizon:
secondary_horizons:
benchmark_or_relative_object:
mandate_context:
requested_decisions:
excluded_methods:
```

## Scope control

The analysis must state what is included, excluded and unresolved. Ambiguous requests are resolved by mapping the economic object, legal instrument, quotation convention, governing institution and data-release clock.

## Object-specific completeness

A generic macro essay is not a market analysis. A company analysis must reach statements and business economics. A commodity analysis must reach physical balance and logistics. A sovereign analysis must reach institutions, fiscal accounts, external accounts and investor base. A portfolio analysis must reach hidden common drivers and nonlinear scenario loss.
