---
prompt_id: P11_EVIDENCE_PLAN
version: 1.0.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.1.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# P11_EVIDENCE_PLAN

## Purpose
Account for every material fact family and compile the smallest sufficient full-vault retrieval plan with no silent gaps.

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
- `scope_state`

## Canonical Vault dependencies
- `95 Fact Constitution and Institutional Evidence Fabric/00 Fact Constitution and Institutional Evidence Fabric MOC.md`
- `94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/23 Retrieval Planning and Context Firewall.md`
- `100 Six-Market D2 Fact Books and Production Shadow Engine/26 Fact Observability and Coverage Constitution.md`

## Process instructions
Compile a STRICT_FULL evidence/retrieval plan. Account for every mandatory science and all 16 observability fact families. Use contextual materiality: every family is checked, but only material families enter active retrieval. Build coverage requirements, public/licensed/private/proxy gaps, source freshness requirements and canonical Vault dependencies. No silent omission.

## Authority
May create: retrieval_plan, coverage_requirements, observability_plan.
Must not create: facts, hypotheses, final_permission.

## Output artifacts
- `retrieval_plan` → `94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/schemas/AlphaLab_Retrieval_Plan.schema.json`
- `coverage_requirements` → `RUNTIME/R2 Prompt Execution OS/schemas/AlphaLab_R2_Coverage_Requirements.schema.json`
- `observability_plan` → `RUNTIME/R2 Prompt Execution OS/schemas/AlphaLab_R2_Observability_Plan.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
