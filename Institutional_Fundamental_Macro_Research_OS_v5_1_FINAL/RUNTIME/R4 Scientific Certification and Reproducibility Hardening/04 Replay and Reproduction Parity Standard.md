# Replay and Reproduction Parity Standard

R4 separates three kinds of parity:

1. **Visibility parity** — the same frozen source snapshot set produces the same admitted/not-admitted evidence set.
2. **Invocation parity** — the same run inputs, prompt hash, canonical context hashes, schemas and model profile produce the same invocation hash.
3. **Decision parity** — the final scientific permission is identical. This may depend on the actual model/provider and is therefore an environment certification question.

Input parity is a hard runtime invariant. Provider nondeterminism is never used as an excuse for input drift. If decision parity is not exact under a non-deterministic host, R4 requires a variance receipt that identifies provider/model/version, invocation hashes, differing process outputs and final-decision impact.
