# 06 — Gold Knowledge Compiler

The P01 compiler reads the canonical registry plus declared Gold knowledge surfaces in the Vault. It does not call the internet.

It produces a coverage receipt containing:

- registered fact count and families;
- explicit/private/paid fact inventory;
- all discovered Gold knowledge surfaces;
- which fact IDs appear on each surface;
- explicit governance/validation surfaces that are allowed to contain no direct fact family;
- missing required surfaces;
- V2 freeze verification;
- P02 handoff readiness.

`ZERO UNACCOUNTED GOLD KNOWLEDGE` in P01 is enforced at the surface/family boundary: every discovered pre-V3 Gold surface must either map to registered fact families or be explicitly predeclared GOVERNANCE_ONLY; unmatched Gold surfaces fail closed. Registry term matching is diagnostic rather than proof that every phrase in a document is a distinct fact. It does **not** mean every fact is observable or live. That stronger claim belongs to P02.


## V3.1.1 interface-contract hardening
Gold-surface discovery is case-insensitive and platform-invariant. Windows and Linux must enumerate the same pre-V3 Gold knowledge surfaces.

A Gold-named JSON Schema is not automatically a market-fact surface and is never silently downgraded to governance. A schema may be classified `INTERFACE_CONTRACT_ONLY` only when it is explicitly listed in `gold_interface_contract_registry.json`, its exact content hash matches the audited version, and its top-level required/property contract matches the audited field map. Hash or field drift fails closed and requires a new semantic audit.

The five audited V2 schemas for Gold precommit, response observation, integrated shadow-run input/receipt, and canonical Control Room are transport/orchestration/rendering contracts. They can carry registered Gold facts and derived states, but they define no new Gold market fact by themselves.

Backup/VCS roots such as `.alphalab_patch_backups` and `.git` are non-canonical and excluded from Gold knowledge discovery. Backup copies must never inflate coverage, duplicate evidence, or resurrect superseded knowledge.
