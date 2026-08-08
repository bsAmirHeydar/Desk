# Model Prompt Vault and Source Version Provenance

Point-in-time reproducibility includes the reasoning environment.

Every production run must record where available:
`model_id`, `model_configuration`, `prompt_file`, `prompt_sha256`, `production_manifest_sha256`, `vault_git_commit`, `authority_map_version`, `tool_contract_version`, `source_snapshot_manifest_sha256`, `analysis_cutoff_utc`.

If an identifier is unavailable, store `UNAVAILABLE`; never invent it. A later model/version change defines a new model regime for calibration and must be segmented in performance analysis.
