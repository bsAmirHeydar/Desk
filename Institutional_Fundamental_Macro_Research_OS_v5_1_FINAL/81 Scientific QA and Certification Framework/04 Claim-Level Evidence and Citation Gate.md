---
title: "04 Claim-Level Evidence and Citation Gate"
type: canonical-standard
status: canonical
version: 9.0.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, scientific-qa]
---

# Claim-Level Evidence and Citation Gate

## Claim taxonomy

Every load-bearing statement must be tagged internally as one of:

- observed fact;
- officially published estimate;
- derived measurement;
- market-implied estimate;
- forecast;
- causal inference;
- scenario assumption;
- institutional judgment;
- unknown or unavailable information.

## Required locator

A certified claim records:

```yaml
claim:
claim_type:
source_organization:
document_or_series:
publication_timestamp:
reference_period:
vintage_or_filing_version:
exact_locator: page | table | section | series_id | filing_item
transformation:
units:
interpretation:
limitations:
contradictory_source:
```

A homepage link is not a claim-level citation. An official source route is necessary but insufficient without a document, series or table locator.

## Evidence hierarchy

1. legal text, regulator, statistical agency, central bank, exchange, issuer filing or physical-market authority;
2. peer-reviewed or official research with disclosed methodology;
3. high-quality commercial data with a transparent definition;
4. contemporaneous reporting used only for facts not yet available in primary documents;
5. analyst estimates and proxies, clearly labelled;
6. anecdote, social media or unsourced commentary — not admissible for load-bearing claims.

## Triangulation

Triangulation must add independent information. Three outlets quoting the same agency release are one source, not three. Independent triangulation may combine:

- official quantity data;
- market-implied pricing;
- balance-sheet or filing evidence;
- physical/logistics evidence;
- institutional flow evidence.

## Citation completeness threshold

A report cannot receive FULL certification unless every conclusion-changing claim is sourced. Supporting descriptive details may be grouped, but the reader must be able to reproduce the conclusion from the ledger.

## Evidence conflicts

When primary sources disagree due to definitions, lags or coverage, preserve the conflict. Explain which measure is decision-relevant and why. Never average incompatible series merely to manufacture agreement.
