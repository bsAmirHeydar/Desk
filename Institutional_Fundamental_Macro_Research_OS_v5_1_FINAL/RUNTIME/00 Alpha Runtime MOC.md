---
title: Alpha Runtime
status: canonical-runtime
runtime_version: R1.0.0
scientific_stack: V21.3.0
---
# Alpha Runtime

Alpha Runtime is the execution substrate for the Alpha Lab scientific Vault. It is deliberately separated from the scientific stack: `V21.3.0` remains the scientific/cognitive authority while `R1.0.0` provides the first runtime foundation.

## Current runtime status

`R1.0.0` implements **Phase 0 + Phase 1 + Phase 2** only:

1. Architecture Constitution.
2. Universal Run and immutable storage core.
3. Point-in-time visibility, historical replay and outcome firewall.

It does **not** yet replace the V21.3 production prompt or create a new trade-permission authority. Prompt-process execution and orchestration arrive in R2.

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
