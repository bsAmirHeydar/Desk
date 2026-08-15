---
title: "P04 Non-Promotion, Backward Compatibility and Rollback"
type: governance-contract
status: shadow-development
---
# V1 remains closed

P04 writes only to `NEXT_VERSION/AD_V2_PHASE_04_LATENT_RELEASE_ENGINE`.

No V1 runtime, production manifest, broker authority or canonical V1 direction logic is changed.

P04 consumes P00-P03 by exact hash dependency and is `SHADOW_ONLY`.

Rollback removes P04 only. P00-P03 remain intact.
