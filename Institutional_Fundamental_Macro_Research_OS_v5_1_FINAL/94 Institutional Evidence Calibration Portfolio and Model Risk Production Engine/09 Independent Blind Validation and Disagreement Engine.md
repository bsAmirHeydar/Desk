# Independent Blind Validation and Disagreement Engine

A model cannot certify its own independence. V16 therefore records validator mode explicitly:
- `NONE`;
- `BLIND_SECOND_PASS_SAME_MODEL` — useful QA, **not independent validation**;
- `INDEPENDENT_MODEL_OR_ANALYST` — genuine independent review.

The validator receives the frozen evidence pack and candidate state, but not the primary model's hidden reasoning. It scores: evidence sufficiency, causal coherence, narrative circularity, dependency/double-counting, timing legality, permission legality and material missing alternatives.

Disagreements are structured, not averaged. A material unresolved disagreement caps the run or sends it to `NO_TRADE` only when the configured validation policy is ENFORCED.

Use `schemas/AlphaLab_Validation_Record.schema.json` and `validation/V16_Blind_Validator_Prompt.md`.
