# Unified Run Contract freeze

Canonical human entry is `AlphaDesk.ps1 run Gold`. P12 fingerprints the launcher, run contract, P11 master cluster registry and P11 orchestration runtime. The closed V1 runtime surface used by the direct bridge is separately bound and frozen; a legacy `AlphaLab.ps1` wrapper is optional when absent from the current clean HEAD.

## Installed V1 authority-surface binding
P12 verifies the Git-tracked V1 authority/runtime files actually used by the P11 bridge are unchanged since before P00, then seals their aggregate canonical hash and Git blobs in the final implementation receipt. A legacy root `AlphaLab.ps1` wrapper is included in the binding when present but is not required when absent from the current clean HEAD. Any later authority-surface change fails final status.
