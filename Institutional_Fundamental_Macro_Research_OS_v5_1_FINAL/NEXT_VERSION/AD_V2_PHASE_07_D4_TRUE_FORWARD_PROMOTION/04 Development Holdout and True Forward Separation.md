# Development / Holdout / True-Forward separation

Three evidence classes are permanently distinct.

## DEVELOPMENT_CASE
Historical or hand-selected examples used to design hypotheses. They may include the user's prior trades. They cannot satisfy promotion floors.

## HOLDOUT
Chronologically separated historical data not used to design the rule. Useful for pre-forward falsification, but still not equivalent to true forward.

## TRUE_FORWARD
A commitment sealed before outcome, then matured later. Only this class can satisfy P07 promotion maturity floors.

The system forbids relabeling development rows as true-forward and reports source counts separately.
