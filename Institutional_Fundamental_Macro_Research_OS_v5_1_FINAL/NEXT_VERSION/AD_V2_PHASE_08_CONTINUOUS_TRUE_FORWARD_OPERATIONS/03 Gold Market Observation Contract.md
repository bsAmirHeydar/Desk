# Gold market observation contract

P08 never fetches or fabricates market outcomes by inference.

Future price observations enter through an append-only `GOLD_MARKET_OBSERVATION` contract with:
- XAUUSD subject;
- UTC observation timestamp;
- explicit source/provider/provenance;
- positive numeric price;
- quality status;
- immutable observation ID/hash.

Conflicting observations with the same source/timestamp are rejected. Future-dated observations beyond clock-skew tolerance are rejected. P08 may consume files dropped by an external market-data process, but P08 itself does not pretend missing observations exist.
