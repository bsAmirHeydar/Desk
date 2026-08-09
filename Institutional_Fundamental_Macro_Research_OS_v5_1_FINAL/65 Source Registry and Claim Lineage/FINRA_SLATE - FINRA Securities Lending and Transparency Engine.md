---
title: "FINRA — Securities Lending and Transparency Engine (SLATE)"
type: source-contract
status: canonical
version: 21.3.0
created: 2026-08-09
updated: 2026-08-09
language: en
tags: [source-registry, observability-v21-3]
source_key: "FINRA_SLATE"
canonical_url: "https://www.finra.org/filing-reporting/slate"
---
# FINRA — Securities Lending and Transparency Engine (SLATE)

## Official route
https://www.finra.org/filing-reporting/slate

## Access / cadence
MIXED_PUBLIC_SUBSCRIPTION

## Institutional use
Securities-loan transaction dissemination and daily loan statistics under FINRA Rule 6500 Series.

## Point-in-time / latency
Public dissemination is delayed by rule; full daily loan-level/statistics products may require subscription. Loan amount dissemination has additional delay.

## Hard boundaries
- A securities loan is not a short sale.
- Loan activity is not short interest.
- Borrow/lending activity does not by itself prove directional bearish positioning.

## Admission contract
Record publication/retrieval/reference times, exact table/file/product, units, corrections/cancellations where applicable, access class, and whether the observation is direct, aggregate, proxy or model inference. A registered source is not assumed available in a run.
