# Failure contract

There is no silent fallback from V2 to a fabricated result. If P11 cannot compile/fetch/validate the V2 evidence stages, it returns a fail-closed receipt while preserving the completed V1 base run.

An explicit `--input-pack` remains available for deterministic/manual replay. P11 bridges directly to the frozen V1 Unified Research Interface. A legacy `AlphaLab.ps1` wrapper, if present in the installed V1 release, remains untouched and independently usable.