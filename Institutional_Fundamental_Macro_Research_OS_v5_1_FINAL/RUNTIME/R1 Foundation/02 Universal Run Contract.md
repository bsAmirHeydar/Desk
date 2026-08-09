# Universal Run Contract

A **Run** is the atomic research execution unit. Live, historical replay, shadow-live and reproduction are different modes of the same object.

## Identity hierarchy

- `research_program_id` — stable research/strategy lineage.
- `episode_id` — optional grouping of related runs, e.g. NFP pre-event/T0/T+5/T+15.
- `run_id` — globally unique execution identity.
- `execution_id` — optional trade-execution identity attached after a decision.

## Supported run scopes

- `INSTRUMENT`
- `MULTI_MARKET`
- `PORTFOLIO`
- `EPISODE`

## Supported run modes

- `LIVE`
- `SHADOW_LIVE`
- `HISTORICAL_REPLAY`
- `RESEARCH_REPLAY`
- `REPRODUCTION_REPLAY`

## Coverage policy

Every RunRequest declares a coverage mode:

- `STRICT_FULL` — default. Every mandatory domain/fact family is considered; no material omission is silent.
- `EVENT_FAST_STRICT` — latency-prioritized but not epistemically shallow; event-critical stages run first and reconciliation follows.
- `DEEP_ESCALATION` — invoked when conflict, model disagreement, coverage gaps or crisis states require additional canonical dependencies.

## Completion policy

R1 records `EPISTEMIC_COMPLETION` as the target completion policy. Later R2 orchestration may issue a final decision only after decision-critical questions are resolved or explicitly unresolved and material gaps are surfaced.

## Fingerprints

`request_fingerprint` binds the resolved request and version pins.

`run_fingerprint` is finalized after snapshots freeze and binds:

```text
request_fingerprint
+ snapshot_manifest_hash
+ vault stack/commit
+ runtime version
+ future prompt-pack/model-profile pins
```

The fingerprint is an audit identity, not a claim of deterministic LLM output.
