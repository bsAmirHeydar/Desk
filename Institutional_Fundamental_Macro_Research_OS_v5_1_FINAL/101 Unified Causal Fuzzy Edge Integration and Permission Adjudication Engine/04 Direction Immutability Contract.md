# Direction Immutability Contract

`final_direction == fundamental_direction`

Always.

D3 outputs may be:
- maintain the existing direction and permission;
- maintain direction but reduce edge quality;
- maintain direction but return `NO_TRADE`;
- maintain direction but delay until a named trigger;
- mark insufficient evidence.

D3 can never convert BULLISH Fundamental Direction into SELL, nor BEARISH into BUY.
