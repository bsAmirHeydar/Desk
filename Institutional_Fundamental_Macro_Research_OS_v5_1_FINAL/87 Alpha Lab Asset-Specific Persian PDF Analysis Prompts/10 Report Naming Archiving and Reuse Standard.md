---
title: "Alpha Lab Report Naming Archiving and Reuse Standard"
type: archive-standard
status: canonical
version: 10.2.0
created: 2026-07-30
updated: 2026-07-31
language: en
tags: [alpha-lab, archive, reports]
---
# Alpha Lab Report Naming Archiving and Reuse Standard

## File naming

```text
Alpha_Lab_[MARKET]_[LIVE_or_HISTORICAL]_Fundamental_Report_[YYYY-MM-DD].pdf
```

Examples:

- `Alpha_Lab_NASDAQ_100_LIVE_Fundamental_Report_2026-07-30.pdf`
- `Alpha_Lab_SP500_LIVE_Fundamental_Report_2026-07-30.pdf`
- `Alpha_Lab_GOLD_XAUUSD_HISTORICAL_Fundamental_Report_2025-01-15.pdf`
- `Alpha_Lab_EURUSD_LIVE_Fundamental_Report_2026-07-30.pdf`

## Suggested repository archive

```text
reports/
  alpha-lab/
    fundamental/
      nasdaq-100/
      sp500/
      gold/
      eurusd/
```

## Report metadata

Every report should retain:

- market and instrument definition;
- LIVE or HISTORICAL mode;
- exact as-of timestamp and timezone;
- data cutoff;
- prompt version;
- Vault version;
- internal QA state;
- source and evidence appendix;
- PDF-generation date.

## Reuse rule

Do not silently overwrite a prior report. Preserve each dated report so changes in thesis, evidence and confidence can be audited over time.


## Daily reports

Use:

```text
Alpha_Lab_[MARKET]_[PROFILE]_[SESSION]_Daily_Fundamental_Report_[YYYY-MM-DD].pdf
```

Store daily reports by date and profile. Do not overwrite the pre-market report with a later session update; the sequence is part of the research audit trail.
