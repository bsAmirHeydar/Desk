---
prompt_id: W37_MECHANICS_CAPACITY_VOL
version: 1.1.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.1.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# W37_MECHANICS_CAPACITY_VOL

## Purpose
Classify institutional mechanics, capacity, options/convexity/volatility and execution distortions at the active horizon.

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
- `decision_evidence_pack`
- `evidence_integrity_receipt`

## Canonical Vault dependencies
- `99 Institutional Mechanics and Market Capacity Science/00 Institutional Mechanics and Market Capacity Science MOC.md`

## Process instructions
Use the admitted `decision_evidence_pack` as the substantive evidence body and `evidence_integrity_receipt` as its lineage/integrity gate. Never infer substantive facts from IDs alone.

Classify institutional mechanics and execution capacity: expiry/roll, auction/fixing, rebalance, ETF mechanics, margin/clearing, options/convexity/0DTE, volatility path, spread/depth/resiliency/impact. Capacity is instrument x venue x size x horizon x state. Do not infer dealer book from proxy as fact.

## Authority
May create: mechanics_capacity_state.
Must not create: fundamental_direction, final_permission.

## Output artifacts
- `mechanics_capacity_state` → `99 Institutional Mechanics and Market Capacity Science/schemas/AlphaLab_Mechanics_Capacity_State.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
