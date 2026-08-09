# Prompt, Model and Context Drift Certification

R4 closes a last-mile reproducibility gap: once R2 pins a prompt for a run, the prompt and canonical context used by R3 must remain identical to the pinned job.

Hard rules:
- prompt bytes must match `job.prompt_sha256` at materialization time;
- every canonical context file has a hash in the context bundle;
- materialization recomputes and verifies each context hash;
- a changed prompt/context after job creation fails before host invocation;
- model/provider identity is recorded in Host Receipt;
- production model changes require environment re-certification, not silent continuation;
- no free conversation memory is allowed.

This does not freeze the Vault forever. It freezes the **information set of a specific run**. A new Vault commit or Prompt Pack creates a new certified run basis.
