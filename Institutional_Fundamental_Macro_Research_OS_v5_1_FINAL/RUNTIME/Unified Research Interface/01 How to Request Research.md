# How to Request Research

The canonical human entrypoint is `AlphaLab.ps1 research`. The user supplies a subject and natural-language request; prompt IDs, R2 stages, and M1 class IDs are implementation details.

Examples:

```powershell
.\AlphaLab.ps1 research --subject NASDAQ100 --request "جهت امروز و مقدار فشار باقی‌مانده را بررسی کن." --mode LIVE --output EXPLORER
```

```powershell
.\AlphaLab.ps1 research --subject XAUUSD --request "چرا طلا بعد از CPI حرکت کرد و آیا ادامه دارد؟" --mode LIVE --output EVENT
```

For operations/certification/scheduler use `AlphaLab_Commission.ps1`, not the research interface.

Certified runtime subjects are defined by R3 launcher profiles. An un-certified subject compiles to NEW_ASSET_RESEARCH but production execution remains blocked until separately certified.
