# AD-V3-P02 C2 Price Anchor Operational Closure

This is an operational observation hotfix, not a Direction-science revision.

- Preferred WGC Goldhub remains first. A successful page fetch without a certified numeric spot value is **not** a price observation.
- `GOLDPRICEDEV_XAU_SPOT_PROXY` is a public numeric fallback only when preferred surfaces do not expose a usable number.
- The fallback is `PUBLIC_PROXY`, `TRANSMISSION_ONLY`, and has `causal_direction_authority=false`.
- It exists solely to make point-in-time True-Forward outcome measurement evaluable.
- Price still cannot feed back into causal Direction.
