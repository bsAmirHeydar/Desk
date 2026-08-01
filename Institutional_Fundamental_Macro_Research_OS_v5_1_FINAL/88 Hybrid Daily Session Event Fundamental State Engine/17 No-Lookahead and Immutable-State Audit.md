---
title: "No-Lookahead and Immutable-State Audit"
type: validation-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [no-lookahead, immutable, audit]
---
# No-Lookahead and Immutable-State Audit

## Immutable record rule

Once a historical record is written, later information may not change it. A later revision, confirmation, contradiction or outcome creates a new record linked through `parent_record_id`.

## Forbidden leakage

- later economic revisions;
- later policy decisions or speeches;
- full-day or future-session prices in an earlier record;
- end-of-window outcomes in state scoring;
- later media explanations;
- current index constituents or contract rules applied historically;
- unverified hindsight about what a political statement meant;
- selecting events because they later mattered.

## Reaction-window separation

T0 includes the release/headline and observations available at T0. T+5 includes only information available by T+5, and so on. Never summarize the entire reaction path inside T0.

## Audit fields

Every record stores:

- cutoff;
- publication and desk-availability time;
- reference period;
- vintage;
- observation time;
- source locator;
- timestamp uncertainty;
- no-lookahead status;
- contamination test result.

## Failure policy

Any unresolved lookahead incident invalidates the affected record and prevents a strict-pass run. Do not silently delete the incident; report it in the audit ledger.
