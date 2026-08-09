# Certification Constitution

The certification engine follows these invariants:

- **Fail closed:** an unclassified integrity failure is a failure, not a warning.
- **Truth/time strictness:** timestamps, vintages, source lineage, hashes, prompt pins and authority boundaries are exact.
- **Context flexibility without authority flexibility:** materiality and analytical depth may adapt; direction/permission authority may not drift.
- **No false determinism:** LLM/provider output variance is measured and disclosed. Exact input reproduction is mandatory; exact output reproduction is required only when the bound environment claims determinism.
- **No hidden future:** outcome, future path, later revisions and post-cutoff retrieval are excluded before decision freeze.
- **No silent degradation:** missing licensed/private sources remain explicit gaps; proxies remain proxies.
- **No certification by installation:** a patch can install a certification framework and pass offline release tests, but it cannot attest a production provider or data feed it has never observed.
- **No full-tree deployment fragility:** deployment baselines cover controlled files only. Certification fingerprints cover the authoritative runtime/science surface using normalized canonical text hashes.
- **Reversible attacks:** destructive tests run only in isolated temporary data stores or shadow copies.
