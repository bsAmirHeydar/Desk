# Artifact and Provenance Contract

Every stored object is referenced through `ArtifactRef`.

Required concepts:

- `artifact_hash` — SHA-256 content identity.
- `logical_name` — semantic role inside the run.
- `world` — `DECISION`, `OUTCOME`, `LEARNING`, or `META`.
- `stage` — evidence/market-state/cognition/decision/execution/outcome/learning.
- `media_type` and original filename.
- producing run/process metadata where known.
- byte length.

Source snapshots add:

- `source_id`;
- fact/requirement identity;
- time clocks;
- vintage integrity;
- revision/supersession relation;
- materiality and applicability;
- source semantics.

An artifact reference is not the artifact itself. Verification always recomputes the referenced object's content hash.
