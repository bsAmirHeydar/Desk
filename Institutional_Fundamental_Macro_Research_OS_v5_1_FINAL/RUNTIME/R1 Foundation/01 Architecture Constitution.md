# Architecture Constitution

## Purpose

R1 establishes the runtime rules that all later Alpha Lab execution must obey. Scientific reasoning remains owned by the V21.3 Vault. Runtime code may coordinate and validate, but it may not invent facts, change scientific authority or infer market direction.

## Constitutional principles

1. **One runtime for live and historical work.** Live and replay use the same `RunRequest`, lifecycle and artifact contracts. Only mode and time differ.
2. **Decision World is isolated from Outcome World.** Future outcomes are structurally inaccessible before Decision Freeze.
3. **Point-in-time truth is mandatory.** A fact is admissible only under explicit visibility and vintage rules at `analysis_cutoff`.
4. **No silent omissions.** Every declared decision-critical/material requirement receives an explicit coverage/visibility state.
5. **Immutable scientific history.** Raw snapshots, frozen evidence, cognition and decisions are immutable after their freeze boundary. Later information is append-only.
6. **Content-addressed evidence.** Bytes are identified by SHA-256; identical bytes are stored once.
7. **Provenance before convenience.** Every run artifact points to its producing run, logical role and source object hash.
8. **Strict facts, flexible interpretation.** Temporal visibility, identity, hashes and lookahead rules are strict. Materiality, applicability and reasoning depth remain context-sensitive and auditable.
9. **Version everything that can change meaning.** Vault stack, Git commit, runtime version, schema version, future prompt pack/model profile and source snapshot manifest are pinned in the run record.
10. **Failure is a state, not a reason to fabricate completion.** Missing, unavailable or undetermined inputs remain explicit.
11. **Reproduction is a first-class product.** A historical reproduction must identify the exact snapshots and versions required to recreate the decision world.
12. **No runtime authority beyond evidence.** R1 creates no BUY/SELL/NO_TRADE and no scientific conclusion.

## Separation of concerns

```text
ALPHA VAULT     scientific canon and authority
ALPHA RUNTIME   execution substrate and contracts
ALPHA RUN STORE immutable evidence, states and outcomes
```

The separation is architectural, not cosmetic. Runtime data must be movable to another storage backend without changing scientific semantics.
