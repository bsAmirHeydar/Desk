# Narrative Transmission Clearance Engine

## Authority boundary
**Fundamental is the sole creator of directional causal authority.** Narrative cannot independently create or reverse BUY/SELL direction. Narrative determines whether the fundamental force is being selected, transmitted, ignored, challenged or opposed by the market.

A narrative-only move may be described, but without sufficient fundamental directional authority it cannot become `EDGE_ACTIVE` in this deployment profile.

## Narrative clearance states
- `ALIGNED_DOMINANT`: fundamental thesis is valid and currently dominant in attention/transmission.
- `ALIGNED_EMERGING`: evidence shows market selection is forming but is not fully dominant yet.
- `NEUTRAL`: no material narrative transmission for or against the fundamental thesis.
- `CONFLICTED`: multiple narratives materially compete; control is unstable.
- `OPPOSING`: market transmission materially favors an opposing explanation.
- `UNDETERMINED`: narrative evidence is insufficient to classify.

## Fuzzy transition policy
- Fundamental `ACTIVE` + `ALIGNED_DOMINANT` -> may form Active Core Candidate.
- Fundamental `ACTIVE` + `ALIGNED_EMERGING` -> may still form Active Core Candidate **with confidence/validity cap**. Do not wait for full public consensus and miss early asymmetry.
- Fundamental `ACTIVE` + `NEUTRAL` -> `EDGE_CONDITIONAL`/Bias; wait for transmission.
- Fundamental `ACTIVE` + `CONFLICTED` -> Conditional or Fragmented depending materiality.
- Fundamental `ACTIVE` + `OPPOSING` -> no Active; preserve the fundamental bias separately and define what would re-align transmission.
- Fundamental weak/partial + any narrative state -> narrative may not upgrade it to Active.

## Circularity firewall
Narrative validity must be assessed price-blind where feasible. Price/reaction can then be used as separate transmission/dominance evidence, not as proof of the same narrative that was inferred from that price move.
