# Host Nondeterminism, Retry and Provider Drift

Retry policy is consequence-sensitive:
- transient transport failure: retry within policy;
- schema-repairable output: limited retry;
- lookahead, identity, authority or forbidden-context violation: never retry as if it were transient.

Every model invocation records provider, model, model version, request hash, response hash, attempt and timestamps. R4 does not claim identical LLM outputs unless the bound host provides and passes that property.

Provider/model changes are environment drift and require re-certification. A model change is not a harmless implementation detail because it can alter scientific decisions while all prompts/data remain fixed.
