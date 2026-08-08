# Development, Holdout and Walk-Forward Contract

Every promotion hypothesis must predeclare development and holdout windows or a deterministic walk-forward schedule.

## Rules
- Holdout labels are frozen before holdout outcomes are inspected for promotion.
- Failed hypotheses remain in the ledger.
- A holdout may not be recycled as development and then described as untouched holdout.
- Policy changes create a new version and a new validation clock.
- Rolling walk-forward may be used after initial validation, but each fold preserves chronological order.

D4 distinguishes:
`DISCOVERY`, `DEVELOPMENT`, `HOLDOUT`, `FORWARD_POST_PROMOTION`, and `REPLAY_RESEARCH`.
