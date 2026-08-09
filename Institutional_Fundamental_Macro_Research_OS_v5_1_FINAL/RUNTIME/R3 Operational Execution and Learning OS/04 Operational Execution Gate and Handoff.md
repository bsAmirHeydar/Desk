# Operational Execution Gate and Handoff

P63 creates the scientific final permission. R3 does not edit that artifact. After R1 Decision Seal, R3 creates a separate execution handoff.

R3 may block execution because the permission is NO_TRADE, expired, invalid, shadow-only, or the execution profile is unavailable. This is **BLOCK_ONLY operational authority**, not market direction authority.

The default file-outbox adapter emits a machine JSON permission signal and places no order. A broker/EA adapter may consume it separately. Order placement remains disabled unless an explicit external adapter is configured.

Thus `scientific_permission` and `operational_status` remain distinct and auditable.
