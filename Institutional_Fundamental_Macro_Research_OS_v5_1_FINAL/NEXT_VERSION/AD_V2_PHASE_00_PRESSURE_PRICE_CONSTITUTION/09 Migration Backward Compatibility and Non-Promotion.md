---
title: "Migration Backward Compatibility and Non-Promotion"
type: migration-standard
status: shadow-development
version: "0.1.0"
---
# Migration, Backward Compatibility and Non-Promotion

## V1 records

All existing V1 records keep their original semantics. Phase 00 does not reinterpret old `force`, `consumption`, `remaining_pressure`, `driver_transition`, `model_disagreement`, or permission records as if the new V2 objects had already existed.

## V2 writes

Later phases must version any new first-class objects. A V2-native record may reference a V1 field, but the mapping must be explicit and one-way.

## Compatibility policy

- V1 readers may ignore V2 shadow fields.
- V2 readers may adapt V1 records with an explicit `LEGACY_ADAPTER` provenance label.
- A missing V2 field in a V1 record is not evidence of `LOW` or `NEUTRAL`; it is `NOT_RECORDED_IN_V1`.
- No backfill may use future price outcomes to populate a historical V2 Pressure state.

## Phase 00 promotion state

`SHADOW_ONLY`.

No Phase 00 object can:

- create BUY/SELL;
- flip Direction;
- create positive permission;
- mutate D4 promotion registry;
- change broker-write authority;
- change live scheduler authority;
- supersede the current production manifest.

## Promotion requirements for later phases

Any future enforcement requires explicit engineering certification and, where empirical claims are made, D4 forward evidence. Presence in the repository is not promotion.
