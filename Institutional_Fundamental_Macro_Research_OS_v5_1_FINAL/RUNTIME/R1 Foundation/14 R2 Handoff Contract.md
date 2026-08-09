# R2 Handoff Contract

R2 may begin only after R1 is certified.

R2 will consume these stable R1 interfaces:

- Universal RunRequest and RunManifest;
- runtime data-root resolution;
- content-addressed ArtifactStore;
- RunStore logical artifact registration;
- lifecycle state transitions;
- visibility receipts and snapshot manifests;
- Decision/Outcome World separation;
- Decision Seal;
- replay/reproduction request.

R2 must not change R1 scientific meaning. If a new prompt process needs new data, it extends typed artifacts; it does not bypass the Run Contract.

R2 will add:

```text
Prompt Registry
Prompt Packs
Process DAG
Stage Directors
Independent Workers
Adversaries / Validators
Completion Gate
Decision Freeze integration
```
