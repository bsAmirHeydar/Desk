# Causal Next-Review Scheduler

Review timing is part of intelligence. A fixed “check again in one hour” is inferior when the system knows what can change the state.

The scheduler considers the next scheduled event, event fast-path windows, driver-transition hazard, narrative instability, fact decay, flow reversal risk, funding changes, fixings/auctions, scenario triggers and permission expiry. It selects the earliest **decision-material** timed trigger. When no timed event is available, it emits a condition-based review trigger.

For major events the default cognitive fast path is release parsing, T+5m, T+15m and T+30m or stabilization, with additional reviews if the expected causal leader changes earlier.
