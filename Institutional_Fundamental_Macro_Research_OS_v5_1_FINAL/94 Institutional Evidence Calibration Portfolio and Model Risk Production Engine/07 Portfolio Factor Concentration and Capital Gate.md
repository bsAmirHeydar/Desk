# Portfolio Factor Concentration and Capital Gate

Six instrument permissions are not six independent bets. V16 creates a portfolio gate after final research Edge.

Each candidate must disclose its current root-risk factors using **ordinal risk-control loadings**, not fake betas: `STRONG_NEGATIVE`, `NEGATIVE`, `NEUTRAL`, `POSITIVE`, `STRONG_POSITIVE`, `UNKNOWN`.

Canonical factor families include USD, US_REAL_RATES, US_NOMINAL_RATES, EQUITY_BETA, GROWTH, INFLATION, VOLATILITY_RISK, GOLD_SAFE_HAVEN, JPY_POLICY, GLOBAL_FUNDING and market-specific factors.

## Current deployment mode
The gate is `SHADOW` unless `config/portfolio_gate_policy.json` is explicitly changed to `ENFORCED` after forward validation. Hard operational constraints may always block.

When enforced, the gate may only return `ALLOW` or `BLOCK` under the current binary execution bridge. `REDUCE` is informational until the bridge supports variable risk.

Unknown material factor exposure prevents the gate from claiming diversification.

Use `tools/alphalab_portfolio_gate.py`.
