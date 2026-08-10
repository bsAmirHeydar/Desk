---
prompt_id: P62_D4_GOVERNANCE
version: 1.0.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.1.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# P62_D4_GOVERNANCE

## Purpose
Resolve active validated D4 promotions/constraints only; unregistered rules have zero authority.

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
- `d3_adjudication`

## Canonical Vault dependencies
- `102 Forward Validation Calibration Promotion and Scientific Governance Engine/31 V20 D4 Full-Vault Production Prompt.md`

## Process instructions
Read only the canonical D4 promotion registry/authority state and frozen research states. Apply ACTIVE validated records within their exact scope. No unregistered rule, no inferred promotion, no direction creation. Produce an auditable D4 authority receipt.

## Authority
May create: d4_authority_receipt.
Must not create: unregistered_promotion, fundamental_direction.

## Output artifacts
- `d4_authority_receipt` → `102 Forward Validation Calibration Promotion and Scientific Governance Engine/schemas/AlphaLab_D4_Authority_Receipt.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
