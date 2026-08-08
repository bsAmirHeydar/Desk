# Fuzzy Edge State Machine

D3 adds a second dimension to the existing research edge: `d3_edge_quality`.

States:
- `AMPLIFIED`
- `CONFIRMED`
- `MAINTAINED`
- `FRAGILE`
- `CONSTRAINED`
- `DELAYED`
- `SUPPRESSED`
- `CAPACITY_BLOCKED`
- `INSUFFICIENT_EVIDENCE`

The original `research_edge` remains compatible with the V16/V18 vocabulary. D3 quality explains *why* an active edge remains usable or not.

### Key rule
A positive D3 quality can confirm an existing `EDGE_ACTIVE`, but cannot turn a pre-D3 `EDGE_CONDITIONAL`, `BIAS_ONLY`, `NO_EDGE`, `EVENT_OR_FRAGMENTED`, or `INSUFFICIENT_EVIDENCE` into a new live BUY/SELL in V19.
