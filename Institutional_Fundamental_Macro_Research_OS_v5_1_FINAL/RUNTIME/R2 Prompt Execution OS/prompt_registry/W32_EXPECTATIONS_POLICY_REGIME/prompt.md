---
prompt_id: W32_EXPECTATIONS_POLICY_REGIME
version: 1.1.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.1.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# W32_EXPECTATIONS_POLICY_REGIME

## Purpose
Construct expectation stack, economic/market surprise, bilateral policy reaction where applicable, and horizon-aware regime state.

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
- `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/08 Economic Surprise versus Market Surprise.md`
- `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/10 Policy Reaction Function Intelligence.md`
- `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/11 Regime Vector and State-Dependent Causal Mapping.md`

## Process instructions
Use the admitted `decision_evidence_pack` as the substantive evidence body and `evidence_integrity_receipt` as its lineage/integrity gate. Never infer substantive facts from IDs alone.

Build the expectation stack; distinguish data surprise, economic implication, policy implication, asset implication and market surprise. Build policy reaction function(s), bilateral for FX when relevant, and a horizon-aware multidimensional regime. If reaction/regime mapping is ambiguous, preserve competing states rather than universal signs.

## Authority
May create: surprise_state, policy_reaction_state, regime_state.
Must not create: fundamental_direction, final_permission.

## Output artifacts
- `surprise_state` → `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/schemas/AlphaLab_Surprise_State.schema.json`
- `policy_reaction_state` → `RUNTIME/R2 Prompt Execution OS/schemas/AlphaLab_R2_Policy_Reaction_Output.schema.json`
- `regime_state` → `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/schemas/AlphaLab_Regime_State.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
