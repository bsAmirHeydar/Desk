---
prompt_id: W35_ACTUAL_FLOW
version: 1.0.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.0.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# W35_ACTUAL_FLOW

## Purpose
Classify actual/identified/derived/model-implied flow while preserving flow != volume/OI/price boundaries.

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
- `evidence_integrity_receipt`

## Canonical Vault dependencies
- `97 Actual Flow and Transaction Pressure Science/00 Actual Flow and Transaction Pressure Science MOC.md`

## Process instructions
Distinguish identified/transaction flow, derived flow proxies, model-implied flow and expected mechanical flow. Flow is not volume, OI change, price move or AUM change. Preserve public/private/licensed coverage gaps and participant/venue scope.

## Authority
May create: flow_state.
Must not create: positioning_state, fundamental_direction, final_permission.

## Output artifacts
- `flow_state` → `97 Actual Flow and Transaction Pressure Science/schemas/AlphaLab_Flow_State.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
