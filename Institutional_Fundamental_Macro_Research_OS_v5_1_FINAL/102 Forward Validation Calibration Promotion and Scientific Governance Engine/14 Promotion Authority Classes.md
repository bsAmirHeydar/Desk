# Promotion Authority Classes

D4 promotion is granular. A validated modifier receives only the authority justified by evidence.

Authority classes:
- `REPORT_ONLY`
- `CONFIDENCE_CAP`
- `VALIDITY_SHORTEN`
- `DELAY_PERMISSION`
- `SUPPRESS_PERMISSION`
- `CAPACITY_BLOCK`
- `RESTORE_EXISTING_DIRECTION_PERMISSION`
- `CREATE_PERMISSION_WITH_EXISTING_FUNDAMENTAL_DIRECTION`

The final class is the most demanding. It may create BUY/SELL only when Fundamental already provides a valid BULLISH/BEARISH direction and all other required gates are satisfied. It can never create direction from `NEUTRAL`, `UNRESOLVED`, or `NO_FUNDAMENTAL_EDGE`.
