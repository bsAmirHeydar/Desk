---
title: "Minimal Execution Permission JSON Contract"
type: machine-interface-contract
status: production
version: 14.1.0
---
# Minimal Execution Permission JSON Contract

Filename: `AlphaLab_Execution_Permissions.json`

```json
{
  "generated_at_utc":"<ISO-8601 UTC>",
  "markets":{
    "XAUUSD":{"permission":"BUY|SELL|NO_TRADE","valid_until_utc":"<ISO-8601 UTC>"},
    "NASDAQ100":{"permission":"BUY|SELL|NO_TRADE","valid_until_utc":"<ISO-8601 UTC>"},
    "SP500":{"permission":"BUY|SELL|NO_TRADE","valid_until_utc":"<ISO-8601 UTC>"},
    "DJIA":{"permission":"BUY|SELL|NO_TRADE","valid_until_utc":"<ISO-8601 UTC>"},
    "EURUSD":{"permission":"BUY|SELL|NO_TRADE","valid_until_utc":"<ISO-8601 UTC>"},
    "USDJPY":{"permission":"BUY|SELL|NO_TRADE","valid_until_utc":"<ISO-8601 UTC>"}
  }
}
```

No analytical fields belong in this execution interface. Full analysis remains in the human-facing state/HTML/archive.
