# Recovery boundary

P12 rollback is HEAD-aware and source-only. It must never delete or rewrite P06 capsules, P07 commitments/outcomes, P08 observations/cycles, P09 learning cases or P10 commissioning receipts. Scientific history and source rollback are separate.

## Installed V1 launcher binding
The root `AlphaLab.ps1` is not pinned to the byte hash of an earlier repository snapshot. P12 verifies the installed launcher is Git-tracked, semantically V1-only, unchanged since before P00, then seals its actual canonical hash and Git blob in the final implementation receipt. Any later launcher change fails final status.
