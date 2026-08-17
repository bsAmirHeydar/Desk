# ALPHA DESK — CANONICAL RUN CONTRACT

## Active subject: Gold only

`Run` means `Run Gold`.

```powershell
.\AlphaDesk.ps1 run Gold
```

The P10 canonical router resolves production authority. While V3 remains `SHADOW_COMMISSIONING`, the production command routes to retained V2. It does **not** mean V3 is production.

Explicit V3 shadow commissioning uses the same P10 orchestrator:

```powershell
.\AlphaDesk.ps1 commission Gold
```

Latest authorized production output:

```powershell
.\AlphaDesk.ps1 report Gold
.\AlphaDesk.ps1 open Gold
```

Latest V3 shadow output:

```powershell
.\AlphaDesk.ps1 commission-report Gold
.\AlphaDesk.ps1 commission-open Gold
```

V3 runtime status:

```powershell
.\AlphaDesk.ps1 v3-runtime-status
```

Gold is the only active Alpha Desk subject. Non-Gold requests fail closed. P10 is orchestration only: P03 remains causal authority, P06 semantic authority, P07/P02 data authority, P08 decision-calibration authority, P09 forward-validation authority, and P04 Control Room authority. Trade execution authority remains NONE.
