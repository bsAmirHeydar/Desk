---
title: "08 Central Bank Multi-Stage Communication Clock"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Central-Bank Multi-Stage Communication Clock

Policy days are multi-stage information processes. Separate decision/statement, implementation detail, projections, press conference, Q&A, minutes/accounts and subsequent official speeches.

FOMC, ECB and BoJ must be sourced from current official calendars. Where BoJ release time is officially undecided, preserve `TIME_UNDECIDED`; never invent an exact time.

State `MULTI_STAGE_POLICY_DISCOVERY` is used when the first headline can be superseded by projections, guidance or Q&A. A first reaction is not automatically the final narrative.
