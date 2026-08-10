---
prompt_id: P10_SCOPE
version: 1.0.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.1.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# P10_SCOPE

## Purpose
Resolve exact instrument, market book, horizon, session and strategy scope without analysis contamination.

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
- `run_request / scope supplied by orchestrator`

## Canonical Vault dependencies
- `91 Global Multi-Asset Coverage and Instrument Intelligence Engine/00 Global Multi-Asset Coverage and Instrument Intelligence Engine MOC.md`
- `CURRENT_PRODUCTION_MANIFEST.json`

## Process instructions
Resolve the exact instrument, production market book, asset family, active strategy horizon, relevant session/event frame, run scope and strategy boundary. Distinguish research-supported instruments from the six-market production universe. Do not analyze direction. Return explicit ambiguity rather than guessing aliases.

## Authority
May create: scope_state.
Must not create: fundamental_direction, final_permission.

## Output artifacts
- `scope_state` → `RUNTIME/R2 Prompt Execution OS/schemas/AlphaLab_R2_Scope_State.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
