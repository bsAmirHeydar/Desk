# Final Operator Guide

## Normal operation

```powershell
.\AlphaDesk.ps1 run Gold
.\AlphaDesk.ps1 report Gold
.\AlphaDesk.ps1 open Gold
```

While V3 remains pending forward evidence, production is V2. To run the certified V3 shadow stack:

```powershell
.\AlphaDesk.ps1 commission Gold
```

## Status

```powershell
.\AlphaDesk.ps1 v3-certification-status
.\AlphaDesk.ps1 v3-promotion-status
.\AlphaDesk.ps1 v3-forward-status
.\AlphaDesk.ps1 v3-freeze-status
```

Promotion is explicit and fail-closed. Do not use fixture/replay data as forward evidence.
