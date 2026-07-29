---
title: "02 Claim Evidence Matrix Implementation"
type: institutional-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-reference]
---

# 02 Claim Evidence Matrix Implementation

The claim-evidence matrix is implemented as a first-class research table. Each row connects a sentence used in analysis to a source artifact and the transformation or model that produced it.

## Workflow

- assign a stable claim ID before publication;
- classify the claim as observation, measurement, forecast, causal, scenario, valuation or decision;
- attach source ID and precise locator;
- record cutoff admissibility and vintage;
- attach transformation and model versions;
- record supporting and contradicting evidence;
- state confidence and materiality;
- link the claim to decisions and later attribution.

## Quality tests

The platform rejects a material claim when the source is inaccessible, the locator is missing, the vintage is inadmissible, a causal statement lacks identification, or the transformation cannot be reproduced. The matrix also supports impact analysis: when a source or model changes, every dependent claim and decision can be located.
