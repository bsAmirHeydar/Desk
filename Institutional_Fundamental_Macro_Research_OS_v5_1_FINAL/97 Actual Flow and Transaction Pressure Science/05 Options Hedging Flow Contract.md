# Options Hedging Flow Contract

Options-related flow has separate epistemic layers:
- observed trades and OI;
- estimated customer/dealer side;
- option greeks;
- inferred hedge requirement;
- inferred hedge execution.

A theoretical delta/gamma hedge need is not an observed cash/futures transaction. Record expected hedge pressure separately from realized identified flow.

Zero-DTE or expiry concentration can alter the horizon and convexity but does not itself create Fundamental Direction.
