# Backend Abstraction and Scale Boundary

R1 intentionally uses the smallest reliable local stack:

```text
Python standard library
Filesystem content-addressed object store
SQLite control-plane catalog
```

R3 will add Parquet/DuckDB for analytics.

## Explicit non-goals in R1

- Kubernetes
- Kafka
- microservices
- distributed databases
- cloud lakehouse
- large vector database
- remote workflow engine

## Migration boundary

Runtime contracts are backend-neutral. Future implementations may replace:

```text
Filesystem → S3/object storage
SQLite → PostgreSQL
Local process → distributed executor
```

without changing RunRequest, artifact, visibility or seal semantics.


## Default local placement

When the Vault is inside a Git repository, R1 places the default `AlphaLab_Data` beside the repository, not inside it. This prevents live/backtest run data from appearing as Git working-tree noise. CLI or `ALPHALAB_DATA_ROOT` may override the location.
