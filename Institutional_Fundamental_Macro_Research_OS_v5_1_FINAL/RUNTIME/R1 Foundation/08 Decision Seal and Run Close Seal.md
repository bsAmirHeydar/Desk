# Decision Seal and Run Close Seal

## Decision Seal

The Decision Seal binds:

- run identity and analysis cutoff;
- request/run fingerprints;
- scientific stack and runtime version pins;
- snapshot-manifest hash;
- every decision-world artifact reference/hash;
- event sequence at freeze;
- canonical seal payload hash.

After the seal is committed, Decision World is immutable.

## Run Close Seal

Created only when the run has reached a legitimate close state. It binds:

- Decision Seal hash;
- final outcome-world artifact hashes;
- final learning-world artifact hashes;
- terminal run state;
- close timestamp.

The close seal does not retroactively alter the decision seal.

## Tamper detection

Verification fails if:

- an object byte changes;
- an artifact reference points to missing bytes;
- a sealed decision artifact set changes;
- seal payload recomputation differs.
