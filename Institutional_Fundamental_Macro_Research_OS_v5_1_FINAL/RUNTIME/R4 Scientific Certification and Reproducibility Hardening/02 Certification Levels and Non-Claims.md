# Certification Levels and Non-Claims

## CORE_CERTIFIED
Required for every installed R4 baseline. Includes inherited preflights, temporal attacks, authority checks, prompt/context pinning, seal/tamper checks, source-gap semantics and integrity-surface fingerprint verification.

## FULL_OFFLINE_CERTIFIED
Adds isolated destructive tests: SQLite corruption detection, repeated catalog migrations, concurrent event writes, close-seal immutability, ledger projection tamper/rebuild and cache-key collision tests.

## ENVIRONMENT_CERTIFIED
Requires the actual provider/model binding and retrieval adapters. It records provider/model/version/tool profile, required source-binding state, secret-policy compliance and a deterministic/non-deterministic capability declaration.

## SHADOW_PRODUCTION_CERTIFIED
Requires live/shadow evidence capture followed by frozen historical reproduction using the same source snapshots, Vault commit, Prompt Pack, schemas and model profile. Input parity must be exact. Decision variance must be zero or explicitly accounted for by a reproducibility variance receipt.

## PRODUCTION_READY
Requires explicit sign-off. It is never auto-granted by a self-test.

## Not certified by R4
- profitability;
- expected return;
- win rate;
- market forecast correctness;
- immunity to regime change;
- absence of unknown unknowns;
- private/licensed data that are not actually connected.
