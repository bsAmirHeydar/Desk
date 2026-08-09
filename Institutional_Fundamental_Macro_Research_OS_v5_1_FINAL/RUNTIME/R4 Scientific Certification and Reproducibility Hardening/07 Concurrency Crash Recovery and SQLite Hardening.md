# Concurrency, Crash Recovery and SQLite Hardening

R4 treats the local SQLite/object-store design as a production component, not a toy database.

Certification includes:
- WAL mode and foreign-key enforcement;
- repeated idempotent schema initialization/migration;
- monotonic event sequence under concurrent writers;
- lock release after exceptions;
- checkpoint/cleanup behavior;
- corruption detection on an isolated copy;
- no mutation of live data during destructive tests;
- restart-safe immutable object reads;
- no hidden dependency on temporary `.pyc` files.

Distributed consensus is outside R4 scope. The certified target is the declared local-first runtime topology.
