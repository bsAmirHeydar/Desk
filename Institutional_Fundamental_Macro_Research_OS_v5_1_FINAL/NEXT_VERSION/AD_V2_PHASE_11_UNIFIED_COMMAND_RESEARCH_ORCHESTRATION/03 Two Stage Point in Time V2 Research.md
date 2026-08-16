# Two-stage V2 research

P11 uses two point-in-time stages:

1. **Precommit** — build price-independent Pressure roots and an expected-response signature template from already-admitted research evidence. Seal the P02 fingerprint and expected signature before a new response window is observed.
2. **Observation** — only after the precommit is sealed, retrieve a subsequent Gold/cross-asset observation window and normalize actual response / Gold evidence.

The second stage cannot mutate Pressure or rewrite the precommitted expected signature.