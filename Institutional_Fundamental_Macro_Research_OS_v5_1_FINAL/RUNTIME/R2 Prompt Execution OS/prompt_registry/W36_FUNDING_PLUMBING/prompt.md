---
prompt_id: W36_FUNDING_PLUMBING
version: 1.1.0
prompt_pack: ALPHALAB_PROMPT_PACK_1.1.0
scientific_stack: V21.3.0
runtime: R2.0.0
---
# W36_FUNDING_PLUMBING

## Purpose
Classify funding, collateral, monetary liquidity and dealer balance-sheet capacity without universal bullish/bearish sign maps.

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
- `98 Funding Plumbing Collateral and Balance Sheet Capacity Science/00 Funding Plumbing Collateral and Balance Sheet Capacity Science MOC.md`

## Process instructions
Use the admitted `decision_evidence_pack` as the substantive evidence body and `evidence_integrity_receipt` as its lineage/integrity gate. Never infer substantive facts from IDs alone.

Separate monetary liquidity, funding liquidity, collateral liquidity, market liquidity, dealer balance-sheet capacity and solvency/credit. Build transmission-capacity state without generic `liquidity bullish/bearish` signs.

## Authority
May create: funding_plumbing_state.
Must not create: generic_liquidity_sign, fundamental_direction, final_permission.

## Output artifacts
- `funding_plumbing_state` → `98 Funding Plumbing Collateral and Balance Sheet Capacity Science/schemas/AlphaLab_Funding_Plumbing_State.schema.json`

## Completion standard
Return only the output artifacts defined by the process contract. Every material unknown must be explicit. If the process cannot complete without additional evidence, emit a targeted escalation request rather than guessing.
