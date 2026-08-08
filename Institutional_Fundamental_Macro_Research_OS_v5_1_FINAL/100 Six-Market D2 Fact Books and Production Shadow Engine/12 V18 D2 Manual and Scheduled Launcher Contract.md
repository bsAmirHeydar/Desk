# V18 D2 Launcher Contract

Manual launcher input:
- symbol/instrument;
- `LIVE_NOW` or historical cutoff;
- desired horizon;
- existing production objective.

Launcher instruction:
1. invoke the V18 D2 full-vault production prompt;
2. freeze cutoff before retrieval;
3. run D1 evidence admission;
4. produce the five D2 shadow states and coverage receipt;
5. preserve existing final-permission authority;
6. report next review time/trigger.

Historical mode must use only evidence visible at the supplied cutoff.
