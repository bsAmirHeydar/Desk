# Permission Transformation Law

Input: `pre_d3_permission ∈ {BUY, SELL, NO_TRADE}`.

## If pre-D3 permission is NO_TRADE
Final permission remains `NO_TRADE` in V19. D3 may emit `promotion_readiness=HIGH` for D4 validation, but may not create exposure.

## If pre-D3 permission is BUY/SELL
D3 may:
- maintain it;
- maintain with confidence/validity constraints;
- delay it → `NO_TRADE` until trigger;
- suppress it → `NO_TRADE`;
- capacity-block it → `NO_TRADE`;
- block on decision-critical unknown → `NO_TRADE`.

It may never invert BUY ↔ SELL.
