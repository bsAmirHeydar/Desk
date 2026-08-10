---
prompt_id: P60_D3_EDGE
version: 1.0.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.1.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# P60_D3_EDGE

## Purpose
Apply Module 101 causal modulation only; no voting, additive scoring or Fundamental Direction flip.

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
- `adversarial_review`
- `model_disagreement`
- `premortem`
- `global_reconciliation`

## Canonical Vault dependencies
- `101 Unified Causal Fuzzy Edge Integration and Permission Adjudication Engine/27 V19 D3 Full-Vault Production Prompt.md`

## Process instructions
Apply Module 101 exactly: causal modulation of an existing Fundamental permission/state. D2 can support, friction, delay, suppress, transmission-break or capacity-block. No science voting, additive score, direction flip or new positive permission from a pre-D3 NO_TRADE.

## Authority
May create: d3_adjudication.
Must not create: direction_flip, science_voting, new_permission_from_no_trade.

## Output artifacts
- `d3_adjudication` → `101 Unified Causal Fuzzy Edge Integration and Permission Adjudication Engine/schemas/AlphaLab_D3_Adjudication.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
