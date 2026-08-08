# Mechanical-Flow Dependency and Deduplication

A mechanic may cause expected flow, which may later be observed as actual flow. Those are different nodes in one causal chain, not independent votes.

Example:
`INDEX_ANNOUNCEMENT -> PASSIVE_EXPECTED_FLOW -> CLOSING_AUCTION_IMBALANCE -> REALIZED_AUCTION_VOLUME`

Module 95 root-cause lineage must keep them linked. Module 97 owns realized-flow classification; this module owns the mechanics/capacity context.
