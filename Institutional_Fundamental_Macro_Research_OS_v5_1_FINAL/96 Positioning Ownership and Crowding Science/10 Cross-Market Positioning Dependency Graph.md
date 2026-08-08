# Cross-Market Positioning Dependency Graph

Cross-market positioning claims must avoid double counting the same economic bet across instruments.

Examples of potentially linked risk:
- NQ futures, QQQ, mega-cap basket and related options;
- EUR futures and EURUSD OTC exposure;
- gold futures, gold ETF ownership and physical holdings.

The graph records `economic_risk_root_id`, participant overlap if known, hedge relationships and source independence. Independence is never inferred merely from multiple tickers.
