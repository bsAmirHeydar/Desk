---
title: "Validation Report V13"
type: validation-report
status: canonical
version: 13.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v13, universal-multi-asset]
---
# Validation Report V13

## Internal verdict

`CERTIFIED — CONDITIONAL`

## Passed gates

- Universal schema and examples
- Instrument resolution and adapter selection
- Bilateral FX synthesis and special-regime handling
- Commodity contract identity and physical-balance state
- Index methodology and point-in-time constituent controls
- Coverage and confidence-cap behavior
- Large-universe Tier 1 / Tier 2 / Tier 3 depth control
- V11 and V12 regression
- 60 benchmark contracts
- Invalid-fixture rejection
- Apply, Verify, Rollback, restored-base hash check, re-apply and manifest-only Git commit

## Coverage seed

- FX registry objects: 97, including 34 currency blocks and 63 pair seeds
- Commodity objects: 38
- Index objects: 29

The registry is extensible. Seed counts are not a claim of complete live-data coverage.

## Certification boundary

The release certifies the Vault architecture and deterministic validation only. It does not certify live data for every instrument, proprietary positioning, reserves, invisible inventories, complete historical constituents, empirical probability calibration or alpha.
