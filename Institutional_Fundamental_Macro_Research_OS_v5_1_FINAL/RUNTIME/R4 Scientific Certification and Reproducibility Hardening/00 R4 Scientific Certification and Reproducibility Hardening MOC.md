# Alpha Runtime R4 — Scientific Certification and Reproducibility Hardening

R4 is Phase 7 of the Alpha Runtime program. It adds no market-direction authority, no trade-permission authority, no new strategy and no automatic scientific promotion authority. Its job is to attack, certify and continuously invalidate the runtime if reproducibility or integrity drifts.

## Scope
- inherited R1 time/storage/seal guarantees;
- inherited R2 prompt/DAG/authority guarantees;
- inherited R3 launcher/retrieval/host/outcome/D4 guarantees;
- exact certification-surface fingerprinting with canonical text hashing;
- temporal/no-lookahead attack suite;
- decision/outcome firewall and tamper attacks;
- prompt/context pinning and drift rejection;
- input-reproduction parity;
- model/provider nondeterminism receipts rather than fabricated determinism;
- source revision, missing-source and licensed/private-gap tests;
- concurrency, crash-recovery, SQLite/WAL and ledger integrity tests;
- cross-platform timezone/Unicode/Windows portability tests;
- schema/version compatibility checks;
- environment and shadow-production certification protocol.

## Non-claim
R4 certifies runtime scientific integrity and reproducibility boundaries. It does **not** certify that a trading strategy is profitable, that a direction forecast is correct, or that future market behavior is stationary.

## Certification ladder
1. `CORE_CERTIFIED` — deterministic structural and adversarial offline suite passes.
2. `FULL_OFFLINE_CERTIFIED` — extended destructive tests in isolated temporary stores pass.
3. `ENVIRONMENT_CERTIFIED` — real production host/source bindings are attested and tested.
4. `SHADOW_PRODUCTION_CERTIFIED` — live/shadow runs pass point-in-time and replay parity protocol.
5. `PRODUCTION_READY` — explicit human/governance sign-off after all required prior levels.

Installation of R4 can establish levels 1–2 only. Levels 3–5 require the actual production environment and cannot be honestly pre-certified inside a ZIP patch.
