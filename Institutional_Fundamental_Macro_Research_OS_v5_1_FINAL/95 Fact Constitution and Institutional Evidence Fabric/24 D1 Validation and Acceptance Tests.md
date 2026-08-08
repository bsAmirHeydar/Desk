---
title: "D1 Validation and Acceptance Tests"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, validation, acceptance, tests]
---

# Executable D1 acceptance catalogue

The self-test must exercise at least these properties:

1. exact official first release is eligible;
2. unresolved publication time can be a valid record but decision-critical use holds;
3. material noncritical timestamp uncertainty caps rather than blocks;
4. small clock skew inside tolerance caps;
5. material clock conflict is rejected/held;
6. future revision is excluded before visibility time;
7. replay chooses first release before revision;
8. replay chooses revised vintage after it becomes visible;
9. unresolved publication-time facts are not backfilled into historical cutoffs;
10. derived fact without parent lineage is rejected;
11. derived fact without method lineage is rejected;
12. Narrative inference cannot become Fundamental direction root;
13. unverified source cannot be load-bearing;
14. public proxy remains explicitly a proxy;
15. unresolved decision-critical root independence holds;
16. same-root descendants are detected and deduplicated;
17. D2-pending families cannot acquire decision authority;
18. six markets × ten fact families are registered;
19. Decision Evidence Pack requires cutoff and fact lineage;
20. Direction remains `FUNDAMENTAL_ONLY` and technical execution boundary is preserved.

Regression acceptance additionally requires the existing V16.1 executable self-test and production preflight to pass under the V17 wrapper.
