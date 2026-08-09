# Temporal and No-Lookahead Attack Suite

R4 attacks the temporal boundary rather than merely checking a policy string.

Mandatory attack classes:
- first-available time after cutoff;
- publication before cutoff but retrieval after cutoff;
- retrieval before cutoff but ingestion after cutoff;
- superseded vintage at cutoff;
- current-only series in historical replay;
- official vintage archive admissibility;
- reconstructed-with-provenance in strict historical mode;
- ambiguous/nonexistent DST local timestamps;
- live pre-intake with no synthetic future cutoff;
- component cutoff mismatch in multi-market meta runs;
- outcome-world injection before decision seal;
- post-cutoff revision injection into replay.

A failure in any decision-critical temporal attack invalidates `CORE_CERTIFIED`.
