# Final freeze boundary

P12 freezes the critical V2 science/runtime/orchestration surfaces. Any future change to P02 Pressure, P03 Transmission, P04 Release, P05 Gold roles, P06 memory, P07/P08/P09 evidence governance, P10 RC integration or P11 unified command requires an evidence-driven challenger/revision with a new versioned surface. Silent mutation is forbidden.

## Installed V1 launcher binding
The root `AlphaLab.ps1` is not pinned to the byte hash of an earlier repository snapshot. P12 verifies the installed launcher is Git-tracked, semantically V1-only, unchanged since before P00, then seals its actual canonical hash and Git blob in the final implementation receipt. Any later launcher change fails final status.
