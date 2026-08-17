# Scientific Constitution and V2 Freeze

P01 preserves `baseline/v2_frozen_surface_manifest.json` as the **historical V2 snapshot**. P05 repaired the original ownership-boundary defect without replacing any historical hash.

Current freeze semantics distinguish two classes:

- **LEGACY_BASELINE_IMMUTABLE** — V2 scientific/version manifests represented in the historical snapshot. Missing files or SHA-256 drift fail closed.
- **DEPLOYMENT_MUTABLE** — `AlphaDesk.ps1`, operator run documentation, and the current production-routing manifest. Downstream versioned deployment changes are recorded as historical drift but are not misreported as scientific corruption.

The machine-readable boundary lives in `config/v2_freeze_boundary_policy.json`. A deployment exemption never grants Direction, Permission, semantic authority, or broker authority. Historical evidence remains auditable and is never rewritten to match the current launcher.
