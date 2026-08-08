---
title: "V17 D1 End-to-End Production Workflow"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, workflow, production, d1]
---

# End-to-end workflow

1. Run D1 runtime preflight.
2. Freeze run ID, analysis cutoff, manifest version and requested symbol.
3. Build smallest-sufficient retrieval plan through the existing V16.1 firewall.
4. Convert retrieved evidence to governed Fact Records.
5. Validate source tier, clocks, class, lineage and vintage.
6. Build the Decision Evidence Pack.
7. Audit same-root dependencies and decision-critical gaps.
8. Produce the Fact Coverage Receipt.
9. If the D1 gate is `HOLD/BLOCK`, stop before live permission.
10. Otherwise delegate to V16.1 scientific synthesis:
   - V11/V13 Fundamental direction;
   - V12 Narrative transmission clearance;
   - V15.1 Timing clearance;
   - V16.1 evidence/materiality decision gate;
   - shadow Calibration/Portfolio;
   - enforced Operational gate.
11. Emit BUY/SELL/NO_TRADE with validity/review times and coverage receipt.
12. Donchian-20 M1 + 4ATR + candle-close trail remains external execution.
13. Append immutable outcome/learning telemetry.

D1 therefore sits **upstream** of the existing decision stack and does not replace its validated science.
