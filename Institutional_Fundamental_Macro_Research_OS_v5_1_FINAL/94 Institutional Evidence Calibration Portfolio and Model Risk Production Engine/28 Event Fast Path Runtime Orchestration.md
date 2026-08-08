# Event Fast Path Runtime Orchestration

The fast path is now a runtime artifact, not only a prose rule.

Use `tools/alphalab_event_fastpath.py`:
1. `prepare` creates an immutable pre-event pack containing consensus vintage, scenario tree, surprise dimensions, causal leaders, required cross-assets, timing/hazard boundaries, invalidations and source IDs.
2. `validate` checks event time, preparation time, pack age and hash integrity.
3. `release` appends first-release surprise and immediate transmission without rewriting the frozen pre-event pack.

If a required major-event pack is absent or stale, only the affected micro horizon becomes `UNDETERMINED`; it does not automatically invalidate longer horizons unless the event is decision-critical to them.
