# Deployment versus Runtime Preflight

V16.1 splits preflight into two modes.

## Deployment preflight
Run on install/update and CI. It may scan the entire Vault and checks:
- manifest/mirror drift;
- all canonical/required files;
- unallowlisted execution-ready prompts;
- forbidden legacy production status;
- schemas/configs/tools;
- retrieval policy;
- Python compilation and executable acceptance tests.

## Runtime preflight
Run before every live analysis. It is intentionally small and latency-aware:
- canonical manifest and generated mirror integrity;
- selected production entrypoint/sub-engine;
- required runtime contracts;
- exact six-market universe and mode declarations;
- retrieval policy and asset-book mapping.

An unrelated historical note must not stop a live run merely because it exists. Deployment governance catches repository contamination; runtime governance protects the actual selected decision path.
