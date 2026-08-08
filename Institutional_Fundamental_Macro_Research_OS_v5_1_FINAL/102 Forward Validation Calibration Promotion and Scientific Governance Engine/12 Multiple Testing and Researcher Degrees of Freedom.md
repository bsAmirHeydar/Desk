# Multiple Testing and Researcher Degrees of Freedom

D4 expects many modifier × market × horizon × regime hypotheses. This creates false-discovery risk.

Every calibration report records a `hypothesis_family_id`. Families are defined before promotion review. Benjamini–Hochberg FDR bookkeeping is available for supplied p-values, but p-values are never fabricated by the system.

If valid inferential p-values are unavailable, D4 still requires:
- number of hypotheses screened;
- predeclared primary metric;
- holdout evidence;
- effect-direction stability;
- explicit exploratory label.

No rule can be promoted by selecting whichever metric, regime or horizon happened to look best after inspection.
