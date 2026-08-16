# Live Run

`python tools/run_gold_live_acquisition.py --horizon ALL --json` performs P02 acquisition. The receipt reports source attempts, observation states, blocking omissions/failures, explicit gaps and whether analysis may start. Exit 3 = BLOCKED, 2 = DEGRADED, 0 = PASS. P02 itself is not the analysis engine.

## REV 3.2.3 operational rule

A 403, TLS error, timeout or parser failure on a primary source may activate a declared fallback. The receipt must preserve which source actually supported the observation and the resulting directness/state. If all admissible paths fail for a blocking Fact, analysis remains BLOCKED.

