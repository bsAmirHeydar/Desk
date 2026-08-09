# Storage Constitution

## Storage layers

```text
AlphaLab_Data/
├── objects/sha256/        immutable content-addressed bytes
├── runs/                  run metadata and artifact references
├── catalog/               transactional SQLite control plane
├── warehouse/             future Parquet/DuckDB analytical layer (R3)
├── locks/                 runtime coordination locks
└── tmp/                   atomic-write staging only
```

R1 implements objects, runs, catalog and locks. Warehouse contracts are reserved for R3; no premature analytical platform is introduced.

## Content-addressed object rule

Object bytes are stored at a deterministic path derived from SHA-256. A duplicate payload is not stored twice. Object identity is bytes-based; metadata do not change the object hash.

## Run directory

```text
runs/YYYY/MM/DD/<scope>/<subject>/<episode>/<run_id>/
├── meta/
│   ├── request.ref.json
│   ├── manifest.json
│   ├── manifest_history/
│   ├── events.jsonl
│   └── artifact_index.json
├── decision_world/
│   ├── 10_evidence/
│   ├── 20_market_state/
│   ├── 30_cognition/
│   └── 40_decision/
├── outcome_world/
│   ├── 50_execution/
│   └── 60_outcome/
├── learning_world/
│   └── 70_learning/
└── seals/
```

Files under the run directory are lightweight artifact references. Canonical bytes live in the object store.

## Mutability classes

### Immutable
- raw source bytes;
- source snapshots;
- decision-world artifacts after Decision Seal;
- Decision Seal;
- Run Close Seal.

### Append-only
- event history;
- outcome attachments;
- counterfactuals;
- calibration/learning attachments before Run Close.

### Rebuildable/mutable
- indexes;
- caches;
- warehouse tables;
- materialized exports.

Scientific evidence is never overwritten to "update history".


## Default local placement

When the Vault is inside a Git repository, R1 places the default `AlphaLab_Data` beside the repository, not inside it. This prevents live/backtest run data from appearing as Git working-tree noise. CLI or `ALPHALAB_DATA_ROOT` may override the location.
