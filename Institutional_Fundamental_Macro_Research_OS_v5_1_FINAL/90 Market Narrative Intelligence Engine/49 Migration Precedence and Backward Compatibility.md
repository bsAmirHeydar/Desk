---
title: "Migration Precedence and Backward Compatibility"
type: canonical-method
status: canonical
version: 12.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v12, market-narrative, daily-intelligence]
---
# Migration Precedence and Backward Compatibility

## Precedence

Module 89 governs fact-state semantics. Module 90 governs attention and narrative semantics. Module 88 governs record density and immutable daily/session/event updates. Module 87 governs asset-specific Persian PDF delivery. Module 81 governs internal QA.

## Migration

V11 records may be embedded under `inherited_v11_state`. Do not infer narrative states from old `dominant_driver` or `narrative_saturation` fields without contemporaneous evidence. Use null, `UNAVAILABLE` or `UNDETERMINED` for non-inferable V12 fields.

Historical V11 records remain immutable. V12 can attach a separate reconstruction record with methodology version and confidence.
