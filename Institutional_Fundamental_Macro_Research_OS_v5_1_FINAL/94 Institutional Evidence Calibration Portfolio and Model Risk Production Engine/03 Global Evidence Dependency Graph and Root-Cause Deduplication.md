# Global Evidence Dependency Graph and Root-Cause Deduplication

V15.1 deduplicates clocks. V16 extends the same logic across Fundamental, Narrative, Timing and cross-asset confirmation.

Every evidence node declares one relation to its parent/root:
`INDEPENDENT_EVIDENCE`, `CAUSAL_DESCENDANT`, `MECHANICAL_DESCENDANT`, `CORRELATED_OBSERVATION`, `DERIVED_MODEL_OUTPUT`, `CONTRADICTORY_EVIDENCE`, `UNKNOWN_DEPENDENCY`.

## Hard rule
A descendant of the same root event may improve transmission understanding but may not be counted as a new independent vote. Confidence cannot be raised by counting CPI, the 2Y reaction, DXY reaction and NQ reaction as four independent causes when they are one causal chain.

`UNKNOWN_DEPENDENCY` cannot increase confidence and may cap it.

Use `schemas/AlphaLab_Evidence_Graph.schema.json` and `tools/alphalab_validate_evidence_graph.py`.
