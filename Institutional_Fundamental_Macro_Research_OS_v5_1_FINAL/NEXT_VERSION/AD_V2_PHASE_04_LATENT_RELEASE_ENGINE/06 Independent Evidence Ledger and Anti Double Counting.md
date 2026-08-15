---
title: "Independent Evidence Ledger and Anti Double Counting"
type: scientific-contract
status: shadow-development
---
# Independent Evidence Ledger

Every P04 observation must disclose:

- `evidence_id`;
- domain;
- role;
- strength;
- confidence;
- independence group;
- source kind and provenance reference;
- observed timestamp and freshness TTL;
- applicability/status;
- explicit `target_price_derived=false`.

## Independence

Multiple observations from the same independence group count once for threshold purposes. A GC spot proxy and another mechanically linked Gold price series cannot create two independent maturity confirmations.

## Missing evidence

`UNAVAILABLE` is not supportive evidence. It increases uncertainty. `NOT_APPLICABLE` is structurally absent and does not create uncertainty in the same way.
