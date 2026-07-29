---
title: "02 Evidence Source Lineage and Claim Types"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [evidence, sources, citations, lineage]
---
# 02 Evidence Source Lineage and Claim Types

## Evidence hierarchy

Evidence must be ranked by its relationship to the phenomenon, not by how persuasive the prose appears.

1. **Primary legal or statistical record:** law, regulation, filing, official statistical release, exchange specification, auction result, central-bank decision.
2. **Primary operational record:** transaction record, inventory record, settlement data, company transcript, physical-flow measurement, official balance sheet.
3. **Derived official estimate:** seasonally adjusted series, national accounts estimate, central-bank model estimate.
4. **Auditable market-derived estimate:** curve-implied policy path, breakeven, option-implied distribution, basis or spread calculated from documented inputs.
5. **Peer-reviewed or institutionally documented model:** published methodology with reproducible assumptions.
6. **Reputable secondary analysis:** useful for synthesis, not a substitute for primary evidence.
7. **Expert judgment:** admissible only when labeled, bounded and reviewable.
8. **Unverified commentary:** never sufficient for a material claim.

## Claim taxonomy

| Claim type | Example | Minimum support |
|---|---|---|
| Observation | CPI was published at a stated value | Primary release and timestamp |
| Accounting identity | Sector balances sum consistently | Definitions, units and reconciliation |
| Measurement claim | Shelter inflation momentum changed | Transformation and sensitivity analysis |
| Forecast claim | Growth distribution shifted lower | Model version, benchmark and interval |
| Causal claim | Funding stress caused basis widening | Identification strategy and rival models |
| Market-pricing claim | More easing is embedded in the curve | Instrument specification and curve construction |
| Scenario claim | A tariff shock would raise near-term goods inflation | Conditional assumptions and transmission map |
| Decision claim | Deployment is unfavorable after costs | Scenario payoff, risk, cost and portfolio context |

## Claim-level citation record

Every material claim must carry or resolve to:

```yaml
claim_id:
claim_text:
claim_type:
source_id:
source_title:
source_locator:
publication_timestamp:
observation_period:
retrieval_timestamp:
vintage:
transformation_id:
model_id:
analyst_judgment:
confidence:
known_limitations:
```

`source_locator` must be as precise as the source permits: table, series, page, paragraph, filing item, transcript line, auction field or API endpoint.

## Lineage graph

The desk must be able to traverse:

```text
Source artifact
→ Observation
→ Transformation
→ Feature
→ Model estimate
→ Claim
→ Scenario
→ Decision state
→ Portfolio action
→ Outcome attribution
```

A broken edge invalidates downstream auditability.

## Source-quality controls

- preserve the downloaded or hash-addressed source artifact when licensing permits;
- store source timezone and publication timestamp;
- distinguish preliminary, revised and benchmark vintages;
- record units, seasonal adjustment, population and coverage;
- disclose source methodology changes and breaks;
- prohibit silent substitution of a similar series;
- use archived snapshots for web sources that may change;
- maintain a source retirement and replacement log.

## Evidence confidence

Confidence is capped by the weakest material component. High-quality data cannot rescue a non-identified causal claim; a strong model cannot rescue a contaminated vintage; a precise estimate cannot rescue a structurally unstable relation.
