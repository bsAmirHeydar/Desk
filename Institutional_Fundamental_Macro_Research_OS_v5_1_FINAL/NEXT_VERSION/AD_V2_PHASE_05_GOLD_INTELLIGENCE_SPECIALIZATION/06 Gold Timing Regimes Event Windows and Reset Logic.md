# Gold Timing Regimes, Event Windows and Reset Logic

P05 does not hard-code a universal session story. It registers clocks and requires the active run to identify the relevant timing regime.

## Timing families

- Asia physical / regional demand window;
- London OTC / benchmark window;
- COMEX/US listed-liquidity window;
- U.S. macro release windows;
- U.S. cash-market cross-asset reset;
- Treasury auction/result windows;
- CME expiry/roll/settlement windows;
- month/quarter-end allocation windows;
- unscheduled geopolitical / policy-event window.

## Event-reset rule

A material event does not automatically change Pressure before its outcome. It can:

- cap Release Readiness;
- shorten the expiration of the current expected signature;
- require a post-event P02/P03 recomputation;
- invalidate stale flow/mechanics evidence.

Exact event time must come from the appropriate source calendar for the date/run. Registry templates are not substitutes for the current official calendar.
