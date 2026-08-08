---
title: "EDGE_ACTIVE Definition and Validity Window"
type: canonical-operational-standard
status: canonical
version: 14.1.0
---
# EDGE_ACTIVE Definition and Validity Window

`EDGE_ACTIVE` means that **from now until an explicit expiry, the currently available evidence supports a directional asymmetric opportunity that is usable by the execution engine**.

It does not mean:
- zero risk;
- certainty;
- a guaranteed win rate;
- validity for the whole day;
- absence of a later event.

Minimum qualitative conditions:
1. direction in the execution horizon is coherent;
2. the dominant driver is actually active, not merely theoretically important;
3. transmission is intact enough for the target asset;
4. independent confirmation is adequate and contradictions are bounded;
5. meaningful remaining pressure survives;
6. consumption has not compressed the forward payoff excessively;
7. reversal risk is acceptable and invalidation is explicit;
8. there is enough time before expiry/event/liquidity reset for the mechanical execution profile to exploit the edge.

Every Active state must carry `valid_until`. Expiry may be shortened by events, session transitions, narrative-transition clocks, liquidity deterioration or data staleness.
