---
title: "02 Evidence Source Lineage and Claim Types"
type: standard
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - institutional-standard
  - fundamental-research
  - governance
---
# 02 Evidence Source Lineage and Claim Types

> [!abstract] Purpose
> Make every material claim traceable to an observation, transformation, model, assumption, and time of availability.

## Claim ontology

Every sentence used in a decision packet must be typed:

- **Observed fact** — directly reported by a named source.
- **Derived measurement** — deterministic transformation of observations.
- **Model estimate** — output that depends on parameters and assumptions.
- **Market-implied estimate** — inferred from prices under conventions.
- **Forecast** — future distribution conditional on an information set.
- **Causal claim** — assertion about a mechanism, requiring identification.
- **Scenario assumption** — deliberately hypothetical input.
- **Desk judgment** — expert synthesis not reducible to one model.
- **Decision rule** — mapping from evidence to action.
- **Outcome attribution** — ex-post decomposition, never evidence available ex ante.

## Evidence hierarchy

Authority alone does not determine relevance. For a specific claim, rank evidence by:

1. direct observation of the object;
2. official or legally required disclosure;
3. reproducible transformation;
4. market price with understood conventions;
5. validated model estimate;
6. survey or expert forecast;
7. alternative-data proxy;
8. anecdote or unverified report.

A lower-ranked source can be timelier, but its measurement error must be explicit.

## Claim–evidence matrix

| Claim ID | Claim type | As-of time | Source/series | Transformation | Model | Uncertainty | Rival | Decision use |
|---|---|---|---|---|---|---|---|---|

The matrix must preserve negative evidence and contradictions. Evidence that weakens the thesis is not deleted; it changes the posterior or confidence ceiling.

## Source requirements

For every series or document record:

- publisher and legal status;
- canonical URL or dataset identifier;
- units and universe;
- frequency and reference period;
- release calendar and embargo time;
- revision and benchmark policy;
- seasonal adjustment;
- known breaks;
- access timestamp;
- checksum or archived snapshot where permitted;
- downstream features and decisions.

## Citation discipline

A source bundle at the bottom of a note is not sufficient. Claims used in production should cite a source key and, for documents, section/table/page. In Obsidian:

```text
Claim: Dealer inventories rose during the settlement window.
Evidence: [NYFED_DEALERS; table=<id>; release=<timestamp>; retrieved=<timestamp>]
```

## Correlated evidence

Multiple indicators can be transformations of the same underlying release. Do not count payroll employment, payroll diffusion, and payroll contribution as three independent confirmations. Record dependency families and cap the combined likelihood ratio.

## Alternative data

Alternative data must document:

- legal right to use;
- sampling frame and coverage;
- survivorship and panel churn;
- revisions and vendor restatements;
- mapping from proxy to target;
- failure under behavioral or platform changes;
- latency and operational continuity.

## Evidence red flags

- final-vintage data in a historical signal;
- consensus obtained after the release;
- unarchived webpage overwritten through time;
- chart without series identifiers;
- model output presented as observed fact;
- vendor methodology change without backfill;
- source contamination across unrelated assets;
- publication-date mismatch;
- claim that cannot be reconstructed.

## Related standards

- [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]]
- [[00 Core Standards/13 Claim Evidence Matrix Standard]]
- [[65 Source Registry and Claim Lineage/00 Source Registry MOC]]
