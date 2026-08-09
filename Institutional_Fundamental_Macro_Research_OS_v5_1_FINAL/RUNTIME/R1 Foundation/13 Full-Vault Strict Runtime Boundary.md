# Full-Vault Strict Runtime Boundary

R1 does not yet execute the prompt graph, but it defines the coverage semantics R2 must obey.

`STRICT_FULL` does **not** mean blindly loading every Vault file into model context. It means every mandatory scientific domain and material dependency is accounted for, and every exclusion has an explicit reason.

## Future R2 invariants

- all mandatory domains are considered;
- all 16 V21.3 observability families are evaluated for applicability/materiality;
- all material causal dependencies are resolved or explicitly unresolved;
- source/coverage receipts are stored;
- no material dimension is silently omitted;
- unavailable/private data remain unavailable/private;
- proxies remain proxies;
- inferences remain inferences;
- retrieval expands when material ambiguity requires it;
- analysis stops on epistemic completion, not arbitrary report length.

The runtime therefore combines **universal coverage with contextual materiality**.
