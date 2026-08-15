---
title: "Backward Compatibility Non-Promotion and Rollback"
type: governance-contract
status: shadow-development
---
# Backward Compatibility, Non-Promotion and Rollback

## V1 remains closed

P01 does not patch the production Unified Research Interface. The known V1 semantic flattening is preserved as historical behavior and documented, not silently rewritten.

## V2 reads V1

The V2 shadow adapter reads valid V1 artifacts generated under V21.3.0/R4.0.0 and emits a richer semantic object with explicit ownership.

## V2 does not write V1

No P01 code writes back into V1 `canonical_result`, report, run capsule, R2 artifact store or broker/execution paths.

## Promotion

P01 grants no Direction, Permission or broker authority. It is substrate only.

## Rollback

Rollback removes only P01 files whose hashes still match the patch manifest. P00 and the V1 repository are preserved.
