---
title: "Validation and Acceptance Tests"
type: qa-standard
status: canonical-operational
version: 14.1.0
---
# Validation and Acceptance Tests

A production run passes only if:
- all six markets have fresh timestamps and full required fields;
- horizon states are not copied mechanically across horizons;
- V11/V12/V13 authority boundaries are preserved;
- consumption is not inferred from time or price distance alone;
- remaining pressure is not `100 - consumption`;
- narrative dominance is not equated with validity;
- mechanical/correlated confirmations are not double-counted;
- unavailable order-book/dealer/flow data are not fabricated;
- every conditional Edge has complete `Why Not Active?` disclosure;
- every Active Edge has explicit validity window;
- event risk is classified as veto vs expiry constraint when relevant;
- permission mapping is deterministic and fail-closed;
- prior-call learning reviews only matured horizons;
- hindsight firewall is respected;
- no single case is promoted directly to canonical science;
- HTML contains Learning/Prior-Call Review;
- email contains no attachments and no deep-analysis dump;
- state archive and learning ledger persistence succeed or failure is disclosed.
