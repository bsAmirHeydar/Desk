---
title: "End-of-Day Attribution and Carry-Forward"
type: canonical-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [end-of-day, attribution, carry-forward]
---
# End-of-Day Attribution and Carry-Forward

## End-of-day state

Every open day ends with an immutable `END_OF_DAY_STATE` that reports:

- direction and practical usability at the close;
- main driver and rival explanation;
- how much of the catalyst was absorbed or consumed;
- whether price action was fundamental, flow-led or liquidity-distorted;
- cross-asset confirmation at the close;
- what changed since the baseline;
- errors in the pre-market or prior-session model;
- what carries into the next day;
- active invalidation and expiry conditions;
- next known catalyst.

## Attribution categories

Separate:

- new information;
- expectation revision;
- policy-path change;
- cash-flow/earnings or physical-balance change;
- valuation/risk-premium change;
- positioning/flow amplification;
- liquidity/funding distortion;
- unexplained residual.

## Carry-forward packet

The next `DAILY_BASELINE` must cite the previous `END_OF_DAY_STATE`, not reconstruct it from later outcomes. Carry-forward fields include unresolved driver, remaining pressure, incomplete repricing, active multi-day bridge, contradictions, data gaps and next catalyst.
