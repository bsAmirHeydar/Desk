# Dependence-aware recurrence

Hourly runs inside one economic episode are not independent evidence. P09 aggregates by `independent_episode_key` inherited from P07.

Default recurrence gate for a true-forward hypothesis proposal:
- at least 5 independent TRUE_FORWARD episodes;
- at least 3 distinct trading days;
- at least 2 regimes;
- no single episode contributes more than one vote to recurrence counts.

Historical/development cases may motivate research but never satisfy true-forward recurrence gates.