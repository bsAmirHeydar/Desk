---
title: "P03 Non-Promotion Backward Compatibility and Rollback"
type: governance-contract
status: shadow-development
---
# Non-Promotion

P03 is `SHADOW_ONLY`.

It does not alter:

- V1 Production Manifest;
- R1/R2/R3/R4 production authority;
- Module 89 Direction authority;
- Module 101 permission authority;
- broker/execution authority.

All P03 files live under `NEXT_VERSION/AD_V2_PHASE_03_PRICE_TRANSMISSION_ENGINE`.

## Rollback

Rollback removes P03 files only. P00, P01, P02 and all V1 production files remain intact.

## Compatibility

P03 consumes exact installed P02 runtime and manifests through dependency fingerprints. A mismatch hard-fails installation rather than attempting heuristic migration.
