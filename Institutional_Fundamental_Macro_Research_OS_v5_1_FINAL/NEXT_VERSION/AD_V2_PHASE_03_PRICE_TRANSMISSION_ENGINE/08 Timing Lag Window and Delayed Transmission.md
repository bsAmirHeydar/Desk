---
title: "Timing Lag Window and Delayed Transmission"
type: scientific-contract
status: shadow-development
---
# Timing and Lag

Transmission is horizon- and mechanism-specific.

A CPI surprise can transmit into front-end rates within seconds while ETF allocation or physical demand can take hours or days to appear in the target.

The expected signature must therefore declare:

- earliest material-response time;
- latest expected lag;
- response-window start/end;
- active horizon;
- event/session context where material.

## Interpretation discipline

No response before the earliest expected time is not evidence of failure.

No response after the expected lag can be `COMPRESSION` or `UNDER_TRANSMISSION`, depending on sign and magnitude.

A late response after a prior disagreement does not retroactively erase the earlier disagreement; each snapshot remains point-in-time and append-only for later calibration.
