# AD-V3-P07 — Live Intraday Gold Data Kernel

## Mission
Separate the complete Gold knowledge universe from the synchronous session-critical acquisition path without changing Gold science. P07 plans what/when to refresh; P02 remains the only acquisition/parser/observation authority.

## Invariants
- Knowledge Universe != Live Kernel.
- Available != Fresh for the active horizon.
- Fetch time != economic time.
- Structural context != current impulse.
- Direct DXY is never silently replaced by a USD proxy.
- Pressure != Price.
- No lookahead, semantic hallucination, promotion, or trade execution authority.

## Operational model
NORMAL = refresh Live Kernel, reuse valid Context cache, conditionally escalate specialist gaps. FULL_REFRESH = comprehensive governed acquisition. CACHE_ONLY = zero external network requests.
