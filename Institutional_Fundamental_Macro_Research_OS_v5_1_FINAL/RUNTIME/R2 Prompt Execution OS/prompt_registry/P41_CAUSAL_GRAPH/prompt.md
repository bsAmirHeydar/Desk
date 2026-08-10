---
prompt_id: P41_CAUSAL_GRAPH
version: 1.0.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.1.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# P41_CAUSAL_GRAPH

## Purpose
Build run-specific causal graph with multi-channel same-root fusion, edge states, lags, activation/break conditions and evidence references.

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

## Canonical Vault dependencies
- `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/12 Dynamic Regime-Conditioned Causal Graph.md`

## Process instructions
Build the dynamic run-specific causal graph. Encode root/channel direction, polarity, state, lag, activation/break conditions, endogeneity/reflexivity, strength band and evidence references. Deduplicate independence, not effects. A root may carry supportive and obstructive channels and be CONTESTED.

## Authority
May create: causal_graph, root_channel_map.
Must not create: new_fact, permission.

## Output artifacts
- `causal_graph` → `103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/schemas/AlphaLab_Causal_Graph.schema.json`
- `root_channel_map` → `RUNTIME/R2 Prompt Execution OS/schemas/AlphaLab_R2_Root_Channel_Map.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
