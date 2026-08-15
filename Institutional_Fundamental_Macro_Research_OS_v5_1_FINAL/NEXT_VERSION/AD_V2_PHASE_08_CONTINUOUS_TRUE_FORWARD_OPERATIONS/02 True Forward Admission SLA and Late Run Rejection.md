# True-forward admission SLA

A P06 run is eligible for automated TRUE_FORWARD admission only when:
- P06 capsule-extension integrity passes;
- subject is XAUUSD;
- deployment is an expected shadow state;
- analysis-to-P06-seal latency is within the configured bound;
- P06-seal-to-P08-freeze latency is within the configured bound;
- no prior P07 commitment exists for the run.

Default bounds are conservative: 15 minutes analysis-to-P06 seal and 5 minutes P06-seal-to-P08 freeze.

A late run is recorded as `LATE_TRUE_FORWARD_REJECTED`. It is never silently relabeled TRUE_FORWARD. Historical reconstruction remains available through P07's explicit non-promotable provenance paths.

## Activation cutoff
On the first P08 cycle an immutable activation receipt is sealed. Runs older than the activation cutoff are treated as the pre-P08 baseline and ignored rather than being mass-labeled as late failures. The default cutoff looks back five minutes so a very recent P06 run can still be admitted if it satisfies all timing gates.
