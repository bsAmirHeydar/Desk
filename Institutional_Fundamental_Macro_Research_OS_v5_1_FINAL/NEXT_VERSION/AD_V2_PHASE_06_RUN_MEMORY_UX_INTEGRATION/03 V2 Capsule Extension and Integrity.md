# V2 Capsule Extension

P06 does not replace the closed V1 Run Capsule. It creates a sibling **V2 Capsule Extension**.

The extension stores:
- base capsule hash/reference;
- exact upstream science fingerprints;
- canonical V2 state hash;
- change-set hash;
- portable-memory payload;
- P06 quality/integrity receipt;
- immutable capsule-extension hash.

The extension is written atomically and cannot be overwritten. Tamper verification recomputes the canonical hash.

No secret-like fields are allowed in persisted V2 state.
