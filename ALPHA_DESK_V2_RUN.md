# ALPHA DESK V2 — LEGACY V2 PRODUCTION / ROLLBACK CONTRACT

V2 remains the authorized production fallback while V3 is `SHADOW_COMMISSIONING` and remains available for rollback after future promotion.

Do not call V2 directly for ordinary operation. Use:

```powershell
.\AlphaDesk.ps1 run Gold
```

P10 resolves production authority and currently routes that production request to V2 until V3 is explicitly promoted.

The V2 P11 prompt cluster is **legacy V2 authority only**. It has no V3 semantic, causal, decision-calibration, or orchestration authority. V3 uses P03/P06/P07/P08/P09/P10.
