# Current Production Manifest and Retrieval Firewall

Production must begin by reading `CURRENT_PRODUCTION_MANIFEST.yaml`. No launcher, prompt or legacy note may become live authority merely because retrieval surfaced it.

## Enforced rules
1. Exactly one `current_stack` is legal.
2. The manifest names the sole full-production entry point and every canonical science owner.
3. Any file listed under `forbidden_live_entrypoints` is history-only.
4. A production run fails closed if the manifest is missing, malformed, references a missing file, or the requested production prompt is not allowlisted.
5. Baseline V14 prompts are retained for lineage but are `archived-superseded`, never live authority.
6. The preflight validator must run before a production permission can be emitted.

The executable check is `tools/alphalab_preflight.py`.

## V17 D1 production routing

`CURRENT_PRODUCTION_MANIFEST.json` now routes live production to Module 95. The V16.1 integrated production prompt is allowlisted as a delegated live subengine. Retrieval still uses this module's smallest-sufficient firewall; Module 95 adds epistemic admission and coverage receipts before decision synthesis.

## V19 D3 delegation
Module 101 is the enforced D2-to-edge causal integration layer. Module 94 continues retrieval, evidence, calibration, portfolio and operational governance and must reject direction-authority drift.
