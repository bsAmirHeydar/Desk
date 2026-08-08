# Production Preflight and Fail-Closed Contract

Before any BUY/SELL can be emitted, preflight must pass:
1. production manifest valid and current;
2. required canonical files present;
3. sole live full-production prompt allowlisted;
4. forbidden legacy entrypoints not selected;
5. six-market profile exactly resolved;
6. state schema and permission schema available;
7. analysis cutoff and model/run provenance fields created;
8. no stale permission reuse;
9. calibration/portfolio modes explicitly declared;
10. operational gate available.

`tools/alphalab_preflight.py` returns exit code 0 only on PASS. Any required check failure means no new permission.
