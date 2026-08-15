---
title: "Cross-Asset Pathway and Leader Confirmation"
type: scientific-contract
status: shadow-development
---
# Cross-Asset Pathway Diagnostics

P03 may compare declared expected pathway signatures with subsequent observations.

For Gold, a policy/discount-rate Pressure model may expect later observations in channels such as:

- front-end yields;
- real yields;
- broad USD;
- rates volatility;
- identified flow or funding channels.

These are **transmission diagnostics**, not new P02 votes.

## Independence groups

Mechanically or economically overlapping observations must share an `independence_group`.

Examples:

- XAUUSD and front-month GC price are same-underlying target proxies and cannot count as two independent pathway confirmations;
- DXY and EURUSD are heavily mechanically overlapping;
- OIS and 2Y may be overlapping policy-path observations.

P03 records raw channel agreement but computes pathway coherence using one effective contribution per independence group.

## Pathway states

- `COHERENT`
- `PARTIAL`
- `FRAGMENTED`
- `UNKNOWN`

Pathway fragmentation can raise model-disagreement risk. It does not mutate Pressure.
