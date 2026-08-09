# D4 Ledger, Calibration and Promotion Firewall

R3 maintains an append-only hash-chained D4 ledger indexed in SQLite. Forward observation, outcome, counterfactual and calibration records are stored with stable record hashes.

Calibration follows the V21.2/D4 policy: paired delta-R is primary, censoring is explicit, cluster dependence is respected, independent-root clusters are preferred, then trading day, then labeled observation fallback. Bootstrap is deterministic from the dataset hash.

The calibrator may only mark `ELIGIBLE_FOR_REVIEW`. R3 never writes the promotion registry automatically. Independent validator authority remains mandatory.


## Runtime Hardening

The canonical D4 ledger payload lives transactionally in SQLite and is hash chained. JSONL is a deterministic rebuildable projection. Verification recomputes payload hashes, chain hashes, previous links, and projection equality. Calibration resampling uses connected independent-root clusters when root IDs exist, then trading-day clusters, and only then a labeled observation-level fallback. Promotion eligibility remains review-only and never mutates the registry.


## Scientific Schema Gate

Forward observations, outcomes, counterfactual outcomes, and calibration reports are validated against the canonical D4 JSON Schemas **before** immutable storage or ledger append. Runtime convenience schemas cannot weaken the scientific D4 contract.
