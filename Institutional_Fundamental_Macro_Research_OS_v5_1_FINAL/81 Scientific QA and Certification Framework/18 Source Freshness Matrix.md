---
title: "18 Source Freshness Matrix"
type: canonical-standard
status: canonical
version: 9.0.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, scientific-qa]
---

# Source Freshness Matrix

## Purpose

The matrix maps research claims to source classes, expected update intervals and maximum safe staleness. It prevents the use of a recent article to support an old methodology or an old quarterly release to describe an intraday state.

| Domain | Primary source examples | Typical cadence | Main freshness risk |
|---|---|---|---|
| policy | central-bank decision, minutes, speeches | event-driven | later communication changes reaction function |
| rates | official/reference rates, exchanges, Treasury | intraday/daily | stale curve or wrong settlement time |
| macro | statistical agencies | weekly to quarterly | revisions and reference-period lag |
| corporate | regulator/issuer filings | event/quarterly | filing acceptance time and restatements |
| credit/banks | regulators, filings, surveys | weekly to quarterly | opacity and valuation lag |
| commodities | physical authorities, exchanges | daily to monthly | estimates, unreported inventories and logistics |
| positioning | regulators/exchanges/fund reports | daily/weekly | lag and category mismatch |
| countries | IMF, national authorities, central banks | monthly to annual | definition changes and data quality |
| derivatives | exchange methodology and live surface | intraday | model and timestamp sensitivity |

## Current official standards added in v8

- Federal Reserve revised model-risk guidance, SR 26-2 (2026), replacing SR 11-7.
- IMF BPM7 (released 2025) for external-sector statistics.
- SEC EDGAR and Inline XBRL structured financial data.
- BIS global liquidity methodology.
- NAIC solvency and ORSA frameworks.
- MSRB EMMA municipal disclosure and trade data.
- FERC Energy Markets Primer and market-design material.
- IAEA nuclear fuel-cycle and uranium publications.

Source notes reside in [[65 Source Registry and Claim Lineage/00 Source Registry and Claim Lineage MOC]].
