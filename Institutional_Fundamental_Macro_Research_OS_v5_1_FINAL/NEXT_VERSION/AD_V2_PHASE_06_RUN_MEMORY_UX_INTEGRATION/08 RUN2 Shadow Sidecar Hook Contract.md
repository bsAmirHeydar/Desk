# RUN2 Shadow Sidecar Hook

Because V1 is closed, P06 does not edit the active V1 executor.

Instead it defines a deterministic sidecar hook that may be called **after** a RUN2 Gold run has produced its closed/base capsule and P02–P05 shadow states.

The sidecar can:
- compose the V2 state;
- persist a V2 capsule extension;
- generate change/history records;
- render the V2 Explorer;
- optionally attach presentation/outcome artifacts to the existing AlphaRuntime run when the run is not close-sealed.

It writes no Decision-world artifact and grants no execution authority.

Promotion of this hook into the one-command mainline executor is explicitly deferred to P07 certification/promotion.
