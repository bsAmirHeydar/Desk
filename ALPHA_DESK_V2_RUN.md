# ALPHA DESK V2 — RETAINED FALLBACK RUN CONTRACT

V2 is retained as the rollback/certified fallback while V3 remains in shadow commissioning.

Canonical local Gold request:

```powershell
.\AlphaDesk.ps1 run Gold
```

The top-level launcher decides the authorized route. Until V3 reaches `PRODUCTION_V3`, this command resolves to the **V2 fallback**. Do not call V2 directly as a way to bypass launcher governance.

Canonical Chat semantics are defined in `RUN.md`: `Run` means `Run Gold`.

V2 scientific invariants remain intact, including Pressure ≠ Price and broker authority NONE.
