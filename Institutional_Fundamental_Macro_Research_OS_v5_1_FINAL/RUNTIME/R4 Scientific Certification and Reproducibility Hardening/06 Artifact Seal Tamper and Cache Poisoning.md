# Artifact Seal, Tamper and Cache-Poisoning Certification

R4 verifies:
- content-addressed object hash integrity;
- decision artifact-set integrity;
- ref/catalog agreement;
- decision seal re-verification;
- close-seal integrity;
- post-seal decision mutation rejection;
- post-close outcome/learning mutation rejection;
- D4 ledger chain and JSONL projection integrity;
- exact hash cache semantics.

Cache reuse is valid only when the full cache key matches. Approximate similarity, matching subject, matching date or matching prompt ID are insufficient. A different input artifact hash, prompt hash, context hash, scientific stack or Prompt Pack must produce a different job/cache key.
