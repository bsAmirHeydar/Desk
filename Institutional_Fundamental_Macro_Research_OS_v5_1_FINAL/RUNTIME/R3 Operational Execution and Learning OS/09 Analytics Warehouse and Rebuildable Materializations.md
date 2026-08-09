# Analytics Warehouse and Rebuildable Materializations

Canonical authority remains the R1 object store plus SQLite catalog. R3 adds normalized analytics rows and append-only ledgers to SQLite and can export partitioned JSONL deterministically.

DuckDB/Parquet is an optional **rebuildable accelerator**, never a source of truth. If those optional libraries are absent, analytical correctness is unchanged and the runtime reports the accelerator as unavailable. This avoids making Windows deployment or scientific correctness dependent on optional binary packages.
