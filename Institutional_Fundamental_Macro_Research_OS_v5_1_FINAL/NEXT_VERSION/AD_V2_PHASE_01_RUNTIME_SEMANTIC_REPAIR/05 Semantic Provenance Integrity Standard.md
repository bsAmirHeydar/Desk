---
title: "Semantic Provenance Integrity Standard"
type: quality-standard
status: shadow-development
---
# Semantic Provenance Integrity Standard

Every load-bearing V2 semantic field carries:

- `owner`;
- `artifact`;
- `source_path` or `source_paths`;
- `horizon` when horizon-specific;
- `status`;
- raw value/range without undocumented reinterpretation.

## Shadow hard gate — SEMANTIC_OWNERSHIP_INTEGRITY

Hard fail if:

1. the declared owner does not match the ownership registry;
2. the source artifact/path is not permitted for that semantic field;
3. a forbidden field class appears in a source path;
4. active-horizon state is substituted from another horizon;
5. Remaining Asymmetry populates Remaining Pressure;
6. Driver Transition populates Force or Persistence;
7. P01 invents a force class without a declared mapping contract;
8. target-price behavior appears as a direct Force source.

## Shadow hard gate — NO_SEMANTIC_SUBSTITUTION

`substitutions_used` must be empty.

## Shadow hard gate — V1_CLOSED_BASELINE_INTEGRITY

All fingerprinted V1 runtime/science files must remain byte-identical to the closed baseline.
