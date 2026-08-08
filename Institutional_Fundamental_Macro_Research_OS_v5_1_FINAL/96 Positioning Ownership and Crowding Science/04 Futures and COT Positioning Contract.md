# Futures and COT Positioning Contract

## Direct facts
Regulated/public positioning reports may provide identified category-level futures/options positions under their own methodology. Store the reported vintage exactly as published.

## Derived states
Examples: percentile, z-score, week-over-week delta, concentration, gross leverage proxy, net speculative state. These are derived and must declare lookback and transformation.

## Prohibitions
- Weekly report state cannot be relabeled as current intraday state.
- Report-date positions cannot be made visible before publication time.
- `open_interest_change` alone cannot identify which side initiated risk or participant identity.
- A futures participant subset is not the entire cash/OTC market.
