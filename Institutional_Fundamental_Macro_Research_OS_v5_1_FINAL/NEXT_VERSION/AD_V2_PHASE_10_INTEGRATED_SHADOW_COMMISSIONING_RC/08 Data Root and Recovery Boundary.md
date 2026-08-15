# Data-root boundary

P10 source stays in Git. Mutable P06–P09 state stays under `AlphaLab_Data/alpha_desk_v2`. P10 commissioning receipts live under `alpha_desk_v2/p10_commissioning`.

P10 never deletes P06–P09 data. Recovery validates stores and may create inventory/check receipts, but it does not rewrite historical capsules, commitments, outcomes, cycles or learning cases.