# True-forward lifecycle

The P07 store is append-only:

`alpha_desk_v2/p07_validation/`

It contains immutable commitments, append-only outcome links, a commitment index, an outcome index and calibration/promotion receipts.

Status reports distinguish:
- total commitments;
- true-forward commitments;
- mature true-forward records;
- independent episodes;
- trading days;
- pending/immature records;
- unscorable records.

No scheduler may fabricate maturity. If market-path/outcome data is absent, the record remains pending.
