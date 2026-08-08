# Systematic, Passive and Rebalance Flow Estimation

Modelled CTA, vol-control, risk-parity or passive-index demand is `MODEL_INFERENCE` unless a direct transaction source identifies it.

Every estimate declares:
- model/version;
- rebalance clock;
- assets and weights;
- signal/volatility inputs;
- AUM assumption or range;
- participation/impact assumption;
- uncertainty range;
- realized-flow confirmation status.

An announced index change can create an expected mechanical flow state; only the actual transaction/auction evidence upgrades realized-flow status.
