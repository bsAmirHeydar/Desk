# Governance Change Control and Two-Key Promotion

Production authority changes are explicit releases, not conversational drift.

A promotion requires two distinct records:
1. `PROMOTION_PROPOSAL` from calibration/governance review;
2. `VALIDATOR_DECISION` from independent validation.

Only then may a `REGISTRY_CHANGE` activate authority.

The runtime engine never writes to the promotion registry itself. Registry mutation is an explicit reviewed change that can be diffed, committed and rolled back.
