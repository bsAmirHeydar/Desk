# R3 Acceptance and Certification Standard

R3 acceptance requires:
- R1 preflight PASS;
- R2 preflight PASS;
- R3 selftest PASS;
- launcher live/historical schema parity;
- production fixture host rejection;
- stateless invocation materialization;
- raw retrieval capture + visibility receipt;
- historical CURRENT_ONLY rejection;
- Decision Seal required before execution/outcome;
- operational gate BLOCK_ONLY;
- no-trade/no-trigger/outcome lifecycle correctness;
- counterfactual frozen-policy enforcement;
- D4 ledger hash-chain verification;
- deterministic calibration bootstrap;
- SQLite analytics queryability;
- optional DuckDB/Parquet absence does not reduce correctness;
- in-memory Python syntax validation on Windows-compatible code;
- no hidden tzdata dependency introduced;
- no `.pyc` compilation required for verification.
