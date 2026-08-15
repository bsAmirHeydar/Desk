# Point-in-time forward commitment

A P07 commitment must be sealed **before** the outcome it will later score.

The commitment binds:
- P06 run ID and canonical V2 state hash;
- base V1 capsule reference;
- analysis cutoff and seal time;
- Gold/horizon/mode;
- immutable P02–P05 feature snapshot;
- independent episode key;
- sample provenance (`TRUE_FORWARD`, `DEVELOPMENT_CASE`, or `HISTORICAL_RECONSTRUCTION`).

Outcome fields such as MFE, MAE, realized R, future price, exit reason or later release state are forbidden inside the commitment.

A historical reconstruction can never be relabeled TRUE_FORWARD after the fact.
