# Scheduler and single-instance operation

P08 provides an optional Windows Task Scheduler installer. Source installation does not require scheduler activation, but the operator installer may activate it after a successful push.

The default scan interval is five minutes so P06 runs can be frozen before the admission SLA expires.

Every cycle uses a single-instance lock. A second cycle exits as `BUSY` rather than racing immutable stores. Crash recovery is idempotent: already-frozen runs, already-linked outcomes and identical observations are skipped safely.
