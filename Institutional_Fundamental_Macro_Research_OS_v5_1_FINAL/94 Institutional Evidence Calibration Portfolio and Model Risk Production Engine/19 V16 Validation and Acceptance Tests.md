# V16 Validation and Acceptance Tests

A release fails if any of these fail:
- manifest points to more than one live full-production prompt;
- a forbidden legacy launcher is selected;
- V14 baseline prompt remains `execution-ready` inside the canonical Vault;
- evidence graph contains duplicate node IDs, unknown parents or cycles;
- same-root descendants are counted as independent votes in a test case;
- numeric probability is emitted under COLD_START without a calibrated source;
- portfolio gate claims diversification with UNKNOWN material factor exposures;
- operational expired/stale permission returns BUY/SELL;
- Timing creates direction;
- execution trigger creates direction;
- outcome write mutates original run state;
- validator mode claims independence while using same-model blind pass;
- DJIA/ USDJPY production books are missing;
- V16 prompt or schemas fail manifest/preflight checks.

See `validation/V16_Acceptance_Cases.json` and run `tools/alphalab_preflight.py` plus tool self-tests.
