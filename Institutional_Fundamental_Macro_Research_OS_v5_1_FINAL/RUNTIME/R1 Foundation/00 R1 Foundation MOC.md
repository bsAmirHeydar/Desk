---
title: Alpha Runtime R1 Foundation
status: canonical-runtime-foundation
version: R1.0.0
phases: [0, 1, 2]
---
# Alpha Runtime R1 — Scientific Runtime Foundation

R1 freezes the substrate on which future prompt orchestration will run. Its purpose is not to add market intelligence; it makes existing intelligence reproducible, point-in-time, immutable and replayable.

## R1 constitutions

1. [[01 Architecture Constitution]]
2. [[02 Universal Run Contract]]
3. [[03 Temporal Visibility and Point-in-Time Constitution]]
4. [[04 Storage Constitution]]
5. [[05 Artifact and Provenance Contract]]
6. [[06 Run Lifecycle and State Machine]]
7. [[07 Decision World Outcome World Firewall]]
8. [[08 Decision Seal and Run Close Seal]]
9. [[09 Replay and Reproduction Contract]]
10. [[10 Failure Degradation and Recovery Semantics]]
11. [[11 Backend Abstraction and Scale Boundary]]
12. [[12 R1 Acceptance and Certification Standard]]
13. [[13 Full-Vault Strict Runtime Boundary]]
14. [[14 R2 Handoff Contract]]

## Executable components

- `schemas/` — canonical R1 contracts.
- `config/` — runtime, storage, lifecycle and temporal policies.
- `sql/catalog_schema.sql` — SQLite control-plane catalog.
- `alpha_runtime/` — standard-library runtime package.
- `tools/alpha_runtime.py` — single CLI.
- `tests/` — behavioral R1 acceptance suite.

## Authority

R1 has **zero market-direction and zero permission authority**. It stores, freezes, gates and reproduces what later reasoning stages create.
