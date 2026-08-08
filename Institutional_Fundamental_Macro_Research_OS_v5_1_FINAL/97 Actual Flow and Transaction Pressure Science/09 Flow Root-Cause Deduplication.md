# Flow Root-Cause Deduplication

Do not count the same economic transaction twice because it appears in:
- ETF shares data and underlying basket activity;
- futures roll volume and open-interest changes;
- option hedge estimate and observed futures trade;
- an index rebalance announcement and closing-auction execution.

Use Module 95 `root_cause_id` and lineage. One causal chain can contain multiple observations without becoming multiple independent confirmations.
