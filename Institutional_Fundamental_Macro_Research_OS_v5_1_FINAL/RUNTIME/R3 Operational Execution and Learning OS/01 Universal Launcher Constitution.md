# Universal Launcher Constitution

The launcher is a compiler, not a researcher. It resolves aliases and presets and emits the exact R1 Universal Run Request. It cannot summarize the market, infer direction, select evidence opportunistically, or modify a final permission.

## Supported launch families
- Single LIVE
- SHADOW_LIVE
- HISTORICAL_REPLAY
- RESEARCH_REPLAY
- REPRODUCTION_REPLAY
- six-market daily basket
- event episode with strict micro-window checkpoints
- bulk historical replay
- cross-run meta reconciliation

A production instrument launch always resolves to one of XAUUSD, NASDAQ100, SP500, DJIA, EURUSD, USDJPY. Unknown aliases fail closed.

The `analysis_cutoff` is `NOW` only for live modes. Historical modes require an explicit aware timestamp. The compiled request always carries STRICT_POINT_IN_TIME.


## Executable Plans

R3 can execute a previously compiled event/daily/bulk plan through `run-plan`; the exact Run Request objects are not reinterpreted at execution time. `daily-six-run` executes six independent component runs and then performs a non-authoritative meta reconciliation. REPRODUCTION_REPLAY is intentionally not accepted by the generic execution path: frozen-source cognitive reproduction remains separately controlled and is certified in R4.
