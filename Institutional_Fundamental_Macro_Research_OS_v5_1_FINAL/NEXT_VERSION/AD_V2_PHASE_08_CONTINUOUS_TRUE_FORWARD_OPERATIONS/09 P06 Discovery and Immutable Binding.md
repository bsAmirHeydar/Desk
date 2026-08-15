# P06 discovery and operating binding

P08 reads P06 `alpha_desk_v2/runs/index.jsonl`, verifies each referenced capsule extension with P06's verifier, and loads the canonical P06 state.

When a P07 forward commitment is created, P08 also seals a `P08_OPERATING_BINDING` containing:
- P06 run/capsule reference;
- P07 commitment ID/hash;
- admission latency measurements;
- evaluation-profile ID/hash if one was already active;
- whether automatic scoring is enabled.

The binding is immutable and is never changed after future observations appear.
