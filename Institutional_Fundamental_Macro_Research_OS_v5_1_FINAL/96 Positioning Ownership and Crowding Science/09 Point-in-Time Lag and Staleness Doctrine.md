# Point-in-Time, Lag and Staleness

For every positioning observation preserve:
- position reference time;
- source publication time;
- first-seen time;
- retrieval/ingestion time;
- revision/vintage where applicable;
- next expected update;
- stale-after policy.

A slow source can remain useful for structural context while being explicitly stale for intraday tactical claims. Staleness changes epistemic role, not the historical fact itself.
