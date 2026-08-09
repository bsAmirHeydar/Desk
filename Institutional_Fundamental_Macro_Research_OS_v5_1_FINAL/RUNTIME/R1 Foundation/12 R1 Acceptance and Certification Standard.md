# R1 Acceptance and Certification Standard

R1 is certified only if all of the following pass:

1. content-addressed deduplication;
2. canonical run creation and manifest history;
3. legal lifecycle transitions;
4. future evidence exclusion;
5. revision/vintage selection;
6. strict historical vintage admissibility;
7. no-silent-gap visibility receipt;
8. Decision World sealing;
9. post-seal decision mutation rejection;
10. pre-seal Outcome World rejection;
11. post-seal Outcome World admission;
12. seal tamper detection;
13. replay visibility parity;
14. SQLite catalog integrity;
15. per-run event monotonicity;
16. ambiguous DST/local-time rejection without explicit disambiguation;
17. full R1 schema/config presence;
18. V21.3 regression/preflight preservation;
19. patch apply/verify/rollback/idempotency;
20. tampered-baseline fail-closed behavior.
21. Run Close Seal verification and post-close mutation rejection.

Certification is runtime-structural. It does not certify prediction quality or trading profitability.

22. Live retrieval/ingestion cutoffs exclude not-yet-ingested evidence.
23. Nonexistent DST local times are rejected.
24. Run-directory artifact-reference tampering is detected against the catalog.
25. Reproduction snapshot manifests retain explicit source-run/source-manifest provenance.
26. R1 self-test completes all current behavioral invariants without writing run data into the Vault.


## Windows and Python portability invariants
- Runtime source validation is in-memory syntax compilation; verification MUST NOT depend on writing temporary `.pyc` files.
- SQLite connections MUST be explicitly closed before temporary-run cleanup.
- R1 MUST operate on Windows even when the external `tzdata` Python package is absent. Current production market zones use bundled IANA TZif fallbacks; unsupported local zones fail closed and require an explicit UTC/offset timestamp.
- Verification subprocesses SHOULD set `PYTHONDONTWRITEBYTECODE=1` to avoid deployment-side cache artifacts.
