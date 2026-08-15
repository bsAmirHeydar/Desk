# No outcome fabrication

Missing observations do not become flat returns. Missing evaluation profiles do not become synthetic R units. Unknown horizons do not receive guessed maturity windows.

Operational states include:
- `PENDING_OBSERVATIONS`
- `PENDING_MATURITY`
- `PROFILE_REQUIRED`
- `COVERAGE_INSUFFICIENT`
- `MATURE_LINKED`
- `UNSCORABLE`

Only `MATURE_LINKED` records enter P07 calibration as mature outcomes.
