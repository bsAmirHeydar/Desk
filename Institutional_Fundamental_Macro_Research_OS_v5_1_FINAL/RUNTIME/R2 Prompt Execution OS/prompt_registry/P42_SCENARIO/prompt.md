---
prompt_id: P42_SCENARIO
version: 1.0.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.1.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# P42_SCENARIO

## Purpose
Build 1-6 materially distinct conditional scenarios with observable confirmation, invalidation and transition paths; no fabricated probabilities.

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
- `hypothesis_set`
- `causal_graph`
- `root_channel_map`

## Canonical Vault dependencies
- `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/18 Scenario Tree and Conditional Path Intelligence.md`

## Process instructions
Build 1-6 materially distinct conditional causal paths, proportionate to actual uncertainty. Include required conditions, early indicators, expected leaders/signatures, structured confirmation/invalidation triggers and transition paths. Keep a decision-material adverse/tail path unless genuinely not applicable. Scenarios are not fabricated probabilities.

## Authority
May create: scenario_tree.
Must not create: fabricated_probability, final_permission.

## Output artifacts
- `scenario_tree` → `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/schemas/AlphaLab_Scenario_Tree.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
