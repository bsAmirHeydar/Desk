---
prompt_id: W21_SNAPSHOT_AUDIT
version: 1.0.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.0.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# W21_SNAPSHOT_AUDIT

## Purpose
Audit captured source snapshots, point-in-time visibility, publication/first-seen semantics and frozen snapshot integrity.

## Non-negotiable execution rules
- Scientific stack authority is V21.3.0. R2 is execution/orchestration only and creates no new scientific authority.
- `Direction authority remains FUNDAMENTAL_ONLY at the active strategy horizon.`
- D1 controls fact admission, vintage, lineage and evidence materiality. Never convert inference/proxy into fact.
- Strict point-in-time: never use any information unavailable at `analysis_cutoff_utc`. Outcome/future world is forbidden before R1 Decision Seal.
- Same-root observations are one independent root; preserve materially distinct channels under the root.
- Unknown, unavailable and undetermined are explicit states, never zero.
- No numeric probability unless backed by a valid D4 calibration record.
- Do not use free conversation memory. Use only the typed inputs/context bundle supplied to this process.
- If a decision-material input is missing, return the appropriate unresolved/fail-closed state and request targeted escalation; do not improvise.
- Keep interpretation flexible and multi-model, but evidence/time/authority rules strict.

## Allowed typed inputs
- `retrieval_plan`
- `coverage_requirements`
- `observability_plan`

## Canonical Vault dependencies
- `95 Fact Constitution and Institutional Evidence Fabric/07 First-Seen Retrieval Ingestion and Snapshot Integrity.md`
- `RUNTIME/R1 Foundation/03 Temporal Visibility and Point-in-Time Constitution.md`

## Process instructions
Audit the actual captured source snapshots. Confirm source identity, publication/first-seen/retrieval/ingestion timing, vintage class, hash integrity and cutoff visibility. Build the frozen snapshot manifest. If a required current-state fact arrived after cutoff, it is invisible even if the source published earlier.

## Authority
May create: snapshot_manifest, snapshot_audit.
Must not create: market_thesis, future_outcome.

## Output artifacts
- `snapshot_manifest` → `RUNTIME/R1 Foundation/schemas/AlphaLab_Snapshot_Manifest.schema.json`
- `snapshot_audit` → `RUNTIME/R2 Prompt Execution OS/schemas/AlphaLab_R2_Snapshot_Audit.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
