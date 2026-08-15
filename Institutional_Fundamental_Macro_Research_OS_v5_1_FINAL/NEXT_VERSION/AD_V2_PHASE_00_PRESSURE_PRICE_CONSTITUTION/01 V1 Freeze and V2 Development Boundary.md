---
title: "V1 Freeze and V2 Development Boundary"
type: constitutional-method
status: shadow-development
version: "0.1.0"
---
# V1 Freeze and V2 Development Boundary

## Closed baseline

V1 is treated as a **frozen reference release**, not as an eternal prohibition on future code changes. The meaning is precise:

- the V1 production decision contract must remain reconstructable from Git and the recorded baseline fingerprint;
- V2 changes must be versioned and attributed to V2;
- no V2 rule may silently claim it was always part of V1;
- no V2 experimental field receives production authority without explicit later promotion.

The V1 reference at Phase 00 creation is `V21.3.0 / R4.0.0`.

## Why Phase 00 is additive-only

Phase 00 is the constitution for later work. To prevent accidental retrospective mutation, it is installed only beneath `NEXT_VERSION/`. It does not change any active canonical production file.

Later phases may need to modify or extend runtime code. When they do, they must:

1. retain a migration path from the V1 contract;
2. preserve frozen V1 records;
3. version new schemas rather than reinterpret old records in place;
4. distinguish V1-compatible reads from V2-native writes;
5. keep any unvalidated V2 state `SHADOW_ONLY` until D4/R4 promotion conditions are met.

## Baseline critical surface

`baseline/V1_CRITICAL_SURFACE_FINGERPRINT.json` records cryptographic hashes for the critical authority and semantic files inspected before Phase 00. The Phase 00 validator refuses acceptance if those files do not match the expected closed baseline.

This fingerprint is a source-baseline guard, not a claim that mutable data, true-forward records, or operational artifacts are frozen.

## Non-mutation guarantee for Phase 00

`DEVELOPMENT_MANIFEST.json` declares `active_production_files_modified = []`. The patch installer rejects any payload file outside the allowed next-version development root.
