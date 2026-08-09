# End-to-End Shadow Certification Protocol

Production-environment certification must use actual shadow runs, not synthetic confidence.

Minimum protocol:
1. run live/shadow with strict pre-run intake;
2. freeze cutoff and Decision Seal;
3. archive source snapshot hashes, Vault commit, Prompt Pack, model receipts and invocation hashes;
4. after the episode, launch reproduction from the frozen source run;
5. require exact visibility and invocation parity;
6. compare process outputs and final permission;
7. if provider is declared deterministic, any output difference fails certification;
8. if provider is non-deterministic, create a variance receipt and require that variance remains inside governance thresholds;
9. repeat across quiet, scheduled-event, unscheduled-shock and missing-source cases;
10. only then consider `SHADOW_PRODUCTION_CERTIFIED`.

R4 does not prescribe a fake sample count for profitability. D4 promotion floors remain the authority for empirical edge promotion.
