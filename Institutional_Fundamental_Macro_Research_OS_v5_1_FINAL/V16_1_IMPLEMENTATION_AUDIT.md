# V16.1 Implementation Audit

This release addresses the integration audit findings: narrative-direction leakage, over-veto from generic incompleteness, materiality ambiguity, legacy retrieval contamination, shallow DJIA/USDJPY routing, calibration/schema mismatch, train-holdout leakage risk, direction-blind portfolio counting, incomplete operational detection, permissive state contracts, repository-wide runtime preflight, duplicate manifest authority, prose-only event fast path and insufficient executable acceptance coverage.

The design intentionally leaves Calibration and Portfolio SHADOW. V16.1 improves their measurement and diagnostics but does not pretend unvalidated thresholds are institutional truth.
