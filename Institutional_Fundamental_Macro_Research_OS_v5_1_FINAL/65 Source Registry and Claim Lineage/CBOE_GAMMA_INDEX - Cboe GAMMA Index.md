---
source_id: CBOE_GAMMA_INDEX
tier: PUBLIC_PROXY
status: ACTIVE_CONTEXT_ONLY
release: V21.3.0
---

# CBOE_GAMMA_INDEX — Cboe GAMMA Index

## Role

Public options-gamma context for index/ETF mechanics. It is admitted only as a **proxy/derived market-state input**, never as a direct observation of a dealer book.

## Admitted facts

- published index/dashboard value and its timestamp when actually observed;
- change in that published metric;
- product methodology/version when available.

## Hard boundaries

- `gamma proxy != dealer inventory`;
- `gamma proxy != identified hedge flow`;
- `published index != complete listed + OTC option book`;
- a sign or level may inform mechanics/fragility only after asset/horizon mapping.

## Runtime use

Contextual or proxy evidence inside `OPTIONS_DEALER_CONVEXITY`; it can support, constrain, or trigger a review through D3, but never create Fundamental direction.
