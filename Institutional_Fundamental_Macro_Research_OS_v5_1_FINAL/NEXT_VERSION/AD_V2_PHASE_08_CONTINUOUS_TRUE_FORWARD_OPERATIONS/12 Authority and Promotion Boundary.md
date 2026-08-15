# Authority boundary

P08 has operational authority over only its own shadow stores and optional scheduler.

It has no authority to:
- change P02 Pressure;
- change P03 Transmission;
- change P04 Release state;
- reinterpret P05 evidence;
- rewrite P06 capsules;
- weaken P07 promotion requirements;
- modify V1 Direction or Permission;
- write to a broker.

`trade_permission = V1_INHERITED` and `broker = NONE` remain mandatory.
