---
title: Alpha Runtime
status: canonical-runtime
runtime_version: R2.0.0
scientific_stack: V21.3.0
---
# Alpha Runtime

Alpha Runtime is the execution substrate for the Alpha Lab scientific Vault. It is deliberately separated from the scientific stack: `V21.3.0` remains the scientific/cognitive authority while `R1.0.0` provides the first runtime foundation.

## Current runtime status

`R2.0.0` preserves certified R1 Phase 0–2 and adds **Phase 3 + Phase 4**: Prompt Registry/Prompt Packs and the Prompt Process Graph Orchestrator.

1. Architecture Constitution.
2. Universal Run and immutable storage core.
3. Point-in-time visibility, historical replay and outcome firewall.

R2 does **not** create new scientific or trade-permission authority. It executes the V21.3 production science through typed, versioned, authority-separated process prompts. Universal launchers and concrete host execution binding arrive in R3.

## Start here

- [[RUNTIME/R1 Foundation/00 R1 Foundation MOC]]
- [[RUNTIME/R1 Foundation/01 Architecture Constitution]]
- [[RUNTIME/R1 Foundation/02 Universal Run Contract]]
- [[RUNTIME/R1 Foundation/03 Temporal Visibility and Point-in-Time Constitution]]
- [[RUNTIME/R1 Foundation/04 Storage Constitution]]
- [[RUNTIME/R1 Foundation/09 Replay and Reproduction Contract]]

## Non-negotiable boundary

```text
Vault = scientific knowledge / policies / schemas
Runtime = execution contracts / workflow substrate
Run Store = evidence / states / decisions / outcomes
```

Run data are not canonical Vault knowledge and must not be committed to the scientific Git history.


## R2 Prompt Execution OS

- [[RUNTIME/R2 Prompt Execution OS/00 R2 Prompt Execution OS MOC]]
- Prompt pack: `ALPHALAB_PROMPT_PACK_1.0.0`
- 25 typed processes; 8 independent market-state workers; deterministic stage gates; R1 Decision Seal integration.
