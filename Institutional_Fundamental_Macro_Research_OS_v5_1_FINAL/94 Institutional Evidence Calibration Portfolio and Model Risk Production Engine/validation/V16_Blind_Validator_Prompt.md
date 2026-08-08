# V16 Blind Validator Prompt

Input only the frozen evidence pack, candidate state and canonical V16 contracts. Do not receive the primary model's hidden reasoning.

Return PASS / CONDITIONAL / FAIL and structured disagreements for: source/vintage sufficiency, causal chain, narrative circularity, independent-vs-descendant evidence, timing legality, core/timing ownership, calibration honesty, portfolio concentration, operational safety and permission mapping.

If this pass uses the same model family/configuration, label `BLIND_SECOND_PASS_SAME_MODEL`; never call it independent validation.
