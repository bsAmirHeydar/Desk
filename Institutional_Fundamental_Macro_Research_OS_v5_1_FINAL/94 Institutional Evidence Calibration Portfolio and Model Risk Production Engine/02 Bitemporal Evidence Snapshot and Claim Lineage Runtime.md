# Bitemporal Evidence Snapshot and Claim Lineage Runtime

The existing Vault already defines point-in-time and bitemporal theory. V16 makes it a runtime contract.

Each load-bearing evidence object must carry:
- `evidence_id`, `root_cause_id`, `claim_ids`;
- `event_time`, `published_at`, `first_seen_at`, `retrieved_at`;
- `valid_from`, `valid_to`, `revision_number`, `revision_state`;
- `source_id`, `source_tier`, `url_or_locator`;
- `raw_snapshot_sha256` when a snapshot is legally/technically retained;
- `parser_version`, `model_visible_at_analysis_time`;
- `observability_class`: OBSERVED / OFFICIAL_FIRST_RELEASE / MARKET_IMPLIED / PUBLIC_PROXY / MODEL_IMPLIED / STRUCTURED_JUDGMENT / UNAVAILABLE / UNDETERMINED.

No source timestamp means no load-bearing claim. A URL without retrieval/vintage metadata is insufficient for historical validation.

Use `schemas/AlphaLab_Evidence_Object.schema.json` and `tools/alphalab_snapshot_manifest.py`.
