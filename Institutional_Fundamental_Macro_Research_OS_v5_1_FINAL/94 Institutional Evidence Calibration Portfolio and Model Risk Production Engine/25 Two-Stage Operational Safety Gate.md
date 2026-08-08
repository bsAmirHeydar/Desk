# Two-Stage Operational Safety Gate

Operational safety is separate from research truth.

## Stage 1 — `PERMISSION_INGEST`
Required for a new permission to enter the bridge:
- symbol/reference mapping valid;
- market state known and execution venue open for a new entry;
- permission exactly `BUY|SELL|NO_TRADE`;
- permission expiry valid and in the future;
- clock drift present and within configured tolerance;
- state checksum/integrity valid;
- no declared hard transport/feed incident.

## Stage 2 — `ENTRY_TRIGGER`
Run again when Donchian fires. In addition to Stage 1 require:
- live feed connected;
- quote timestamp present and fresh under broker-specific policy;
- finite positive price;
- finite positive ATR used for sizing/stop;
- spread/cost hard-limit check passed;
- duplicate-order protection clear;
- broker position state synchronized.

Missing required operational fields are `UNKNOWN`, not silently assumed healthy. The gate is a detector for the fields it receives and an aggregator for explicit incidents; it must never claim to detect infrastructure it has not been connected to.
