# Host / Model Execution and Stateless Invocation

R2 defines model capability profiles; R3 binds them to concrete host executions. The host is provider-neutral and receives a self-contained invocation: immutable prompt hash, prompt text/reference, typed artifact inputs, canonical Vault dependencies, schemas, model profile, analysis cutoff and authority constraints.

The host must not rely on hidden conversational memory. Every response produces a host receipt with request/response hashes and, when available, provider/model/version/request-id/token/latency metadata.

Production adapters are COMMAND and HTTP_JSON. FIXTURE is test-only and R3 refuses it for production modes.

Secrets are never committed to the Vault. They are supplied through environment variables or local host configuration outside Git.
