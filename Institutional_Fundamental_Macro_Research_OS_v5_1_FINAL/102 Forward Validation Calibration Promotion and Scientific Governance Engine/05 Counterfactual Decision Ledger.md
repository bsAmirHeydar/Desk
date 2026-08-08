# Counterfactual Decision Ledger

D4 evaluates both what happened and what a frozen alternative policy would have done.

## Canonical branches
- `ACTUAL_V20`: decision actually emitted.
- `PRE_D3_BASELINE`: what the pre-D3 stack would have emitted.
- `V19_D3_BASELINE`: the V19 D3 decision before any D4 registry promotion.
- `REMOVE_MODIFIER`: what would happen if one specific D3 modifier were absent.
- `POSITIVE_PROMOTION_SHADOW`: what would happen if a currently shadow-only supportive modifier were allowed to create/restore permission.
- `DELAY_ALTERNATIVE`: delayed entry only when the same execution policy produces a valid later trigger.

## Counterfactual discipline
Counterfactuals must be deterministic from the frozen state and a versioned policy. They may not cherry-pick an entry after seeing the future path.

A hypothetical branch is `UNSCORABLE` when the branch would not have produced a valid execution trigger under the frozen execution rules.
