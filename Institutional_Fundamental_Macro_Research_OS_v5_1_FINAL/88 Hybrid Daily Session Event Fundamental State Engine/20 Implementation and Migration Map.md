---
title: "Implementation and Migration Map"
type: migration-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [migration, architecture, deprecation]
---
# Implementation and Migration Map

## Superseded behavior

The following behavior is deprecated:

- creating records only after large events;
- waiting for 10–15 point changes before observing the state;
- allowing open days with no record;
- carrying a catalyst without decay reassessment;
- treating direction as equivalent to usability;
- using macro background as the majority of intraday output.

## Canonical precedence

This module governs dense daily/session/event historical reconstruction. Existing daily and hourly notes remain supporting standards and defer to this module when a conflict exists.

## Prompt migration

Historical prompts must use `HYBRID_DAILY_SESSION_EVENT_STATE` recording mode. Asset prompts must support historical session replay and mandatory checkpoint records. Launchers should state the target timezone, session schedule, event windows and density validation mode.

## Versioning

All new records include methodology version `10.4.0`. Historical runs must preserve the methodology version to prevent silent comparison across incompatible scoring definitions.

---

## V11 patch migration

V11 is applied additively through a manifest-controlled patch.

- Base precondition: Module 88 `10.4.0`.
- Target methodology: `11.0.0`.
- Added canon: Module 89.
- Modified entry points: only files listed in `PATCH_MANIFEST.json`.
- Every modified file has a required pre-patch SHA-256.
- Apply scripts create timestamped backups.
- Rollback restores overwritten files and removes only patch-added files.
- Historical records are not rewritten.

See [[V11_MIGRATION_AND_PRECEDENCE_MAP]] and [[89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/36 Migration Precedence and Backward Compatibility]].
