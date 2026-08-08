---
title: "Production Fact Admission Gate"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, admission, gate, production]
---

# Fact admission gate

Every candidate record passes three distinct checks:

1. **Record validity** — required identity/class/time/source/lineage fields are coherent.
2. **Historical eligibility** — the version was visible by the analysis cutoff.
3. **Decision eligibility** — source tier, materiality, root dependency and layer ownership permit the record to carry the proposed decision weight.

Outcomes:

- `ELIGIBLE`
- `ELIGIBLE_WITH_CAP`
- `HOLD`
- `REJECTED`

A record can be valid but historically ineligible. A historically eligible record can still be too weak to be load-bearing. This separation prevents both look-ahead and source-quality laundering.
