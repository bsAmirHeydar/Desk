---
prompt_id: P63_FINAL_DECISION
version: 1.0.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.0.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# P63_FINAL_DECISION

## Purpose
Produce the rich Research Intent and compress only at the final adapter to BUY/SELL/NO_TRADE. Operational execution safety remains an R3 handoff.

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
- `decision_utility`
- `d4_authority_receipt`

## Canonical Vault dependencies
- `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/46 V21 Cognitive-Hardened Full-Vault Production Prompt.md`
- `94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/00 Institutional Evidence Calibration Portfolio and Model Risk Production Engine MOC.md`

## Process instructions
Synthesize only frozen upstream outputs. Produce rich Research Intent, cognitive adjudication and the final BUY/SELL/NO_TRADE research adapter. Preserve Fundamental-only direction, outside-strategy edge separation, structured review/invalidation triggers, validity and explicit constraints. Do not access Outcome World. Module 94 broker/operational execution gate is explicitly deferred to R3 execution handoff, not silently skipped.

## Authority
May create: research_intent, cognitive_adjudication, final_permission.
Must not create: invent_evidence, mutate_frozen_fact, direction_flip, outcome_world_access.

## Output artifacts
- `research_intent` → `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/schemas/AlphaLab_Research_Intent.schema.json`
- `cognitive_adjudication` → `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/schemas/AlphaLab_Cognitive_Adjudication.schema.json`
- `final_permission` → `RUNTIME/R2 Prompt Execution OS/schemas/AlphaLab_R2_Final_Permission.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
