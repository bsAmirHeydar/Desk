# راه‌اندازی سریع Alpha Desk V3.1

## اجرای Desk پژوهشی V3.1
```powershell
.\AlphaDesk.ps1 commission Gold
```

## دیدن گزارش آخر
```powershell
.\AlphaDesk.ps1 commission-report Gold
.\AlphaDesk.ps1 commission-open Gold
```

## سلامت سیستم
```powershell
.\AlphaDesk.ps1 v31-ops-status
```

## معنی وضعیت‌ها
- **انتظار (WAIT):** سیستم سالم است، اما شرایط پژوهشی برای اقدام کافی نیست.
- **نامشخص (UNKNOWN):** شواهد برای جهت قطعی کافی نیست؛ خطای نرم‌افزاری نیست.
- **DEGRADED:** بخشی از داده/Provider ناقص است؛ گزارش می‌گوید آیا تحلیل ادامه یافته است.
- **BLOCKED:** یک integrity یا زیرساخت حیاتی مشکل دارد؛ ابتدا دلیل را در Ops Status بررسی کنید.

## اگر Run شکست خورد
آخرین گزارش موفق حفظ می‌شود. ابتدا:
```powershell
.\AlphaDesk.ps1 v31-recovery-status
```

## زمان‌بندی اختیاری
R05 هیچ Scheduleای خودکار نصب نمی‌کند. ابزار نصب اختیاری در پوشه R05/tools قرار دارد.

## Backup
از `backup_alpha_desk_state.ps1` برای PIT/Forward/Qualification استفاده کنید. Git جای Backup داده علمی runtime را نمی‌گیرد.

## Production
V3 فعلاً **SHADOW / پژوهشی** است. Promotion فقط وقتی ممکن است که Forward Quality واقعی همه Gateها را پاس کند و operator صریحاً approval بدهد.
