---
title: "Runtime Safety, Freshness and Fail-Closed Rules"
type: runtime-safety-contract
status: production
version: 14.1.0
---
# Runtime Safety, Freshness and Fail-Closed Rules

Downstream execution must interpret any of the following as `NO_TRADE`:
- missing file/state;
- malformed JSON;
- unknown permission value;
- missing symbol;
- stale `generated_at_utc` beyond configured tolerance;
- expired `valid_until_utc`;
- time parse failure;
- incomplete write.

Writers should use temporary files plus atomic rename where possible. Readers should poll without blocking trading logic. The MT5 bridge should prefer Common Files / `FILE_COMMON` when multiple terminals or EAs need the same permission state.
