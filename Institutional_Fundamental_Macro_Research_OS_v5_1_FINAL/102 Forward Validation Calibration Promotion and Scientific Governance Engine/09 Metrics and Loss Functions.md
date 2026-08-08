# Metrics and Loss Functions

No single metric defines promotion.

## Return/expectancy
- mean R and median R;
- paired mean/median delta R;
- sum-positive / absolute-sum-negative profit factor where realized trades exist;
- positive-R rate, descriptive only;
- expectancy distribution and bootstrap interval.

## Path quality
- MFE R;
- MAE R;
- time-to-trigger;
- time-to-MFE;
- time-to-MAE;
- state-survival rate;
- expiry-without-trigger rate.

## Decision quality
- false-permission rate;
- veto-save rate;
- veto-missed-opportunity rate;
- delay-save rate;
- harmful-delay rate;
- support-opportunity capture rate;
- capacity-block breach rate.

## Tail/risk
- 5% lower-tail mean R;
- worst realized R;
- upper MAE quantiles;
- drawdown contribution where a portfolio sequence is defined.

Promotion uses a conjunctive evidence gate. A small mean improvement that creates materially worse tails is not automatically acceptable.
