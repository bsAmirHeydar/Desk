# OpenAI GPT-5.6 Sol Max-Accuracy Host

The commissioned default model is `gpt-5.6-sol`. C1 uses the Responses API directly through Python standard-library HTTPS, so the Vault does not acquire an SDK dependency.

Model process invocations are stateless. The host receives only the process prompt, typed upstream artifacts, hash-pinned canonical Vault context, explicit runtime evidence where authorized, and output contracts. Web search is deliberately absent from cognition calls.

C1 maps R2 model profiles to GPT-5.6 Sol with pro mode. Accuracy-first profiles use `max` reasoning effort; fact/governance profiles use `xhigh`. No lower-cost fallback is automatic. The returned response model ID, response ID and usage are captured in host receipts.

Structured output is used as a transport constraint, while R2 local JSON-Schema validation remains the final contract authority. The host may perform one schema-repair attempt using the same frozen information set; it may never retrieve additional evidence during repair.

## C1 max-accuracy production settings

- Process output ceiling: 128,000 tokens (model-supported ceiling; schemas normally finish far below it).
- Public-source web retrieval: `search_context_size=high` and `return_token_budget=unlimited` in strict/deep commissioning mode.
- Automatic model downgrade is forbidden.
- Context overflow fails closed; no silent truncation.

- Every commissioned invocation explicitly uses `reasoning.context=current_turn`; C1 does not carry hidden/persisted reasoning across process jobs.
