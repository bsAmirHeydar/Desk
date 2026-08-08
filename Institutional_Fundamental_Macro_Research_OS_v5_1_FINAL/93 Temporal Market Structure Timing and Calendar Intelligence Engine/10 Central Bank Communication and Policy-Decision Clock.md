---
title: "Central Bank Communication and Policy-Decision Clock"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Central Bank Communication and Policy-Decision Clock

Central-bank days contain multiple information releases: decision, implementation details, statement, projections, press conference, Q&A, minutes and subsequent official speeches. These can change the active narrative sequentially.

## FOMC
Use the Federal Reserve's live meeting calendar (`SRC-FED-CALENDAR`). Separate statement time, SEP meetings, press conference and minutes. Do not treat the entire two-day meeting as one timestamp.

## ECB
Use the Governing Council calendar (`SRC-ECB-MEETINGS`). Distinguish policy decision/statement from press conference and later accounts/speeches.

## BoJ
BoJ policy decisions can have less precise release times than US data. Use the official release schedule and MPM pages (`SRC-BOJ-CALENDAR`, `SRC-BOJ-MPM`) and represent `TIME_UNDECIDED` explicitly when official timing is not fixed.

## Temporal hazard
The first policy headline may be superseded by guidance, projections or Q&A. Therefore V15 can label `MULTI_STAGE_POLICY_DISCOVERY` and schedule sequential reviews rather than declaring the first reaction final.

## No-lookahead
Historical evaluation must use the document actually available at each sub-stage. Later minutes or press-conference clarifications cannot be backfilled into the original decision timestamp.
