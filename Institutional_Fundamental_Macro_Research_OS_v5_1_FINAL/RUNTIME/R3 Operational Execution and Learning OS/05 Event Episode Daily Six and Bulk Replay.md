# Event Episode, Daily Six and Bulk Replay

Event episodes use one episode id and multiple independent R1/R2 runs around the event. The default strict micro schedule includes T-120 through T+240, preserves a 30-minute grid where applicable, and adds denser T-15/T-5/T+5/T+15 checkpoints.

Daily-six launches six independent full-vault instrument runs. Cross-market meta reconciliation references their sealed outputs and may request rechecks, but cannot override instrument permissions.

Bulk replay uses the same R1/R2 graph as live. No simplified backtest brain exists. Exact hash cache reuse is allowed; time visibility and vintage rules are not relaxed for speed.


## Daily-Six Cutoff Semantics

Historical daily-six runs use the same exact historical cutoff. Live daily-six component runs each preserve their exact strict intake cutoff; the meta layer must report component cutoffs and may not claim atomic simultaneity unless the source host provides a synchronized snapshot contract.


## Executable Multi-Run Plans

`run-plan` is the common executor for event and bulk plans. `daily-six-run` is the six-market convenience launcher. A live six-market basket does not claim atomic simultaneity across heterogeneous sources: every component's exact cutoff is retained and meta reconciliation reports `EXACT` or `NON_ATOMIC_RECORDED` temporal alignment.
