# Failure and Recovery

P06 fails closed on:
- upstream fingerprint mismatch;
- subject/horizon mismatch;
- invalid/tampered V2 science state;
- permission override attempt;
- immutable capsule collision;
- secret-like persistence fields;
- malformed change history.

Installer rollback is HEAD-aware: pre-existing tracked files are restored from HEAD; genuinely new identical payload files are removed. This prevents the rollback defect encountered during P05 retry workflows.
