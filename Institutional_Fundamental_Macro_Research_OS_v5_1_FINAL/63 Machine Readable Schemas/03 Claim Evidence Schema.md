---
title: "03 Claim Evidence Schema"
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
# 03 Claim Evidence Schema

```yaml
schema_version: 5.0.0
claim_id: string
context_id: string
claim_text: string
claim_type: [observed, derived, model_estimate, market_implied, forecast, causal, assumption, judgment, rule, attribution]
as_of: datetime
evidence:
  - source_key: string
    series_or_document: string
    table_page_section: string
    publication_time: datetime
    vintage: string
    transformation_id: string|null
strength: [A, B, C, D, E]
relevance: number
reliability: number
uncertainty: string
dependencies: [claim_id]
rival_evidence: [claim_id]
decision_fields: [string]
```
