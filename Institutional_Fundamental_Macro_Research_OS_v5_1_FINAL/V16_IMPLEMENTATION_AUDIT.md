# V16 Implementation Audit

## Audit-to-code mapping
- Legacy retrieval contamination → `CURRENT_PRODUCTION_MANIFEST.yaml` + preflight + archived V14 baseline metadata.
- Bitemporal/source reproducibility → Evidence Object schema + snapshot manifest tool.
- Cross-layer double counting → Evidence Graph schema + cycle/root dependency validator.
- Uncalibrated Edge → forward outcome contract + calibrator; COLD_START blocks fake probability.
- Portfolio hidden beta → factor concentration gate; SHADOW default.
- Operational failure risk → ENFORCED operational gate and fail-closed expiry/mapping checks.
- Self-validation → explicit validator-mode taxonomy; same-model pass cannot claim independence.
- Learning overfit → promotion record requirements + holdout/root-event/regime requirements.
- Micro horizon latency → event fast-path contract.
- DJIA/USDJPY depth → dedicated production books.

No claim is made that V16 is profitable or statistically calibrated at installation. It makes the missing evidence observable and the future calibration executable.
