# Outcome maturity

Automatic maturity starts at the forward-commitment seal, never before it.

For a bound evaluation profile P08 requires:
- a reference observation at or shortly after the commitment;
- observation coverage through the complete predeclared maturity window;
- no data gap larger than the profile's maximum gap;
- an intact P07 commitment hash.

BUY pressure uses upside as favorable excursion and downside as adverse excursion. SELL pressure is symmetric. P08 computes MFE_R, MAE_R and time-to-MFE from the immutable future path, then delegates joining/persistence to P07.
