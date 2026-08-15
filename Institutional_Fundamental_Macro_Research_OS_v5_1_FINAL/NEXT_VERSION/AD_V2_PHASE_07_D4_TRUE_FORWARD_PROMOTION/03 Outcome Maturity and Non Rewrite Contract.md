# Outcome maturity

Outcomes are separate append-only records linked to a previously sealed commitment.

Supported maturity states:
- `IMMATURE`
- `MATURE`
- `EXPIRY_WITHOUT_TRIGGER`
- `UNSCORABLE`

A mature record may contain MFE_R, MAE_R, realized_R, time-to-trigger and time-to-MFE. P07 never edits the original commitment.

An outcome whose maturity timestamp precedes the commitment seal is invalid. A run-id mismatch is invalid. Duplicate outcome records with different content are invalid.
