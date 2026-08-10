# C1 True-Forward Activation — TF1.0.0

TF1 extends C1 and FV1 with real chronological evidence acquisition. It does not add Direction, permission, or broker authority.

A true-forward commitment is immutable, stored outside the source tree under `ALPHALAB_DATA_ROOT/forward/commitments`, and cryptographically sealed before outcomes are linked. Outcomes and reviews are separate linked objects. R4 certifies source code/configuration; runtime forward evidence uses independent record seals and is intentionally excluded from the R4 source fingerprint.

Truth labels are explicit. Historical replay and walk-forward runs can never be relabeled as true-forward. A `TRUE_FORWARD` commitment requires a live chronological `SHADOW_LIVE` run, an existing decision seal, M1 method artifacts, APL-A shadow artifacts, no outcome artifact at seal time, and cutoff ordering consistent with a pre-outcome commitment.

APL-A remains `SHADOW_ONLY`; M1 gains no Direction authority; broker execution remains disabled.
