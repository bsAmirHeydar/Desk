# Non-authority law

P10 does not patch the V1 mainline run command to change V1 Direction or Permission. It provides a V2 shadow-run wrapper and commissioning tools only.

`mainline_override=false`, `positive_permission_creation=false`, `broker_authority=NONE`, `auto_promotion=false`, and `auto_tuning=false` are hard invariants.