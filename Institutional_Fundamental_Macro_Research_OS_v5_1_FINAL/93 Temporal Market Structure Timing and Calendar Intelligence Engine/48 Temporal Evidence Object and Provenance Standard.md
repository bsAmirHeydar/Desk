---
title: "Temporal Evidence Object and Provenance Standard"
type: canonical-data-standard
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, evidence, provenance]
---
# Temporal Evidence Object and Provenance Standard

Every material clock must be an auditable evidence object, not free-form prose.

Required fields:
- `clock_id`, `clock_family`, `symbol_scope`;
- exact instrument/reference venue/product/series identity;
- source organization, primary URL or document ID, source tier;
- `retrieved_at_utc`, `published_or_announced_at_utc` when known;
- source-local time and timezone, IANA zone, UTC-normalized time;
- trade/business/settlement-date semantics;
- schedule status: `CONFIRMED`, `TENTATIVE`, `TBD_TIME`, `REVISED`, `CANCELLED`, `UNSCHEDULED`;
- methodology/rule version and effective date where relevant;
- mechanism class;
- independence/dependency relation to other clocks;
- materiality to target asset and horizon;
- evidence confidence and missing fields.

## Source hierarchy
1. exchange/venue/clearinghouse/benchmark administrator/index provider;
2. government/central bank/statistical agency/official issuer;
3. regulatory or BIS-type institutional research for structural mechanisms;
4. high-quality secondary sources only when primary source is unavailable, with confidence cap.

## Freshness
A recurring clock stored in the Vault is a methodology template, not today's calendar. Live production must re-check the current official calendar when the clock can change because of holidays, rule amendments, special sessions, corporate announcements or Treasury/central-bank schedule revisions.

## No false precision
If official time is undecided or a tentative schedule can change, preserve `TBD_TIME` / `TENTATIVE`; do not manufacture a timestamp to satisfy downstream code.
