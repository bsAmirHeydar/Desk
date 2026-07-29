---
title: "13 Claim Evidence Matrix Standard"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [claim-evidence, audit]
---
# 13 Claim Evidence Matrix Standard

## Required matrix

Every material research output must maintain a matrix with one row per claim:

| Claim ID | Claim | Type | Evidence | Locator | Cutoff admissible? | Transformation | Model | Rival | Confidence | Decision relevance |
|---|---|---|---|---|---|---|---|---|---|---|

## Claim states

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `CONTESTED`
- `MODEL_DEPENDENT`
- `JUDGMENT`
- `UNKNOWN`
- `REJECTED`

## Rules

- A source link alone is not evidence; the locator and relevant extract or field must be known.
- A chart or derived statistic must resolve to raw observations and transformations.
- Market-implied quantities must disclose instrument and construction method.
- A causal claim must point to an identification record.
- A decision claim must point to scenario payoff, risk, cost and portfolio records.
- Conflicting evidence remains visible; it is not deleted to simplify the narrative.
