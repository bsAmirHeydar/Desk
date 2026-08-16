# 07 — P02 Handoff: Total Live Data Requirements

P01 intentionally stops before acquisition.

P02 must consume the master fact registry and, for every applicable fact, define:

- primary and backup source;
- public/paid/private status;
- endpoint or retrieval procedure;
- cadence and publication lag;
- `reference_period`, `event_time`, `published_at`, `first_seen_at`, `retrieved_at`, revisions;
- direct/proxy/model classification;
- expected availability and next release;
- retry/fallback rules;
- materiality-aware `BLOCKED`/`DEGRADED` policy;
- proof that every expected public source was **attempted** before analysis begins.

The scientific chain after P02 must be traceable as:

`Decision → Interpretation → Causal Path → Fact → Source → Timestamp/Vintage`.
