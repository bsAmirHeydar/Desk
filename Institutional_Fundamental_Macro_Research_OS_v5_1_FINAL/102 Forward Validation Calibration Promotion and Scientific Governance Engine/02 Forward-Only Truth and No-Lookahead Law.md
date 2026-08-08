# Forward-Only Truth and No-Lookahead Law

Every D4 observation is frozen **before** the evaluated outcome is known.

Required freeze elements include:
- analysis cutoff and state timestamp;
- vault commit and production-prompt hash;
- Fact/Evidence Pack identifiers;
- Fundamental Direction/Force/Consumption/Persistence;
- Narrative and Timing states;
- D2 states;
- D3 integration vectors and adjudication;
- pre-D3 and post-D3 permissions;
- execution-profile version;
- promotion-registry version visible at the time.

Outcome records are separate append-only objects. They can reference a frozen observation, but can never rewrite it.

### Vintage law
A later data revision may be used in an ex-post *revision study* but never substituted into the historical live decision state.

### Policy-version law
A rule is judged under the policy version that actually existed at decision time. Backfilling a newer policy across old decisions must be labelled `REPLAY_RESEARCH`, not `FORWARD_LIVE`.
