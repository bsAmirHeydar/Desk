# D2 Horizon and Staleness Matrix

Every state declares the horizon it can support:
- `EVENT_MICRO` (minutes)
- `INTRADAY`
- `SESSION`
- `DAILY`
- `MULTI_DAY`
- `STRUCTURAL`

A weekly positioning report may be high quality for structural context while stale for event-micro claims. A live transaction feed may be excellent intraday flow evidence but irrelevant to structural ownership.

Never use frequency alone as quality. Match source latency and economic meaning to the decision horizon.
