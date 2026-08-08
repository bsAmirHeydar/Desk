# V16 Migration and Precedence Map

V16 preserves V11 Fundamental, V12 Narrative, V13 instrument science, V15.1 Timing and V14.1 Module 92 Edge/learning. It adds a production-control layer; it does not replace the science.

Precedence in production: `CURRENT_PRODUCTION_MANIFEST.yaml` → V11 → V12 → V13 → core candidate → V15.1 → V16 evidence dependency firewall → Research Edge → calibration shadow → portfolio shadow/enforced by config → operational hard gate → final permission.

Legacy V14/V15 production prompts are history-only. If retrieved, they may explain lineage but cannot issue live permission.
