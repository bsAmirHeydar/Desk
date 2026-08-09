---
prompt_id: P52_PREMORTEM
version: 1.0.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.0.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# P52_PREMORTEM

## Purpose
Assume the trade fails; enumerate decision-material failure paths with automatic/manual monitorability and actionable triggers.

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
- `scenario_tree`
- `d2_shadow_pack`
- `market_state_reconciliation`

## Canonical Vault dependencies
- `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/25 Mandatory Pre-Mortem and Observable Failure Paths.md`

## Process instructions
Assume the contemplated research intent fails. Enumerate 3-7 materially distinct failure paths when warranted; mark AUTOMATIC/MANUAL/PARTIAL/UNMONITORABLE and attach structured warning triggers. A decision-critical unmonitorable failure path must constrain/hold.

## Authority
May create: premortem.
Must not create: final_permission.

## Output artifacts
- `premortem` → `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/schemas/AlphaLab_PreMortem.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
