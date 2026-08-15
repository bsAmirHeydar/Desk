# Dependence-aware evidence

Hourly runs are not automatically independent observations.

P07 clusters evidence by an `independent_episode_key`. By default Gold observations from the same trading day, horizon and dominant causal-root set share an episode unless an explicit event/episode key is supplied before outcome.

Promotion floors use independent episodes and trading days, not raw run count.

This prevents twenty hourly snapshots of one macro impulse from being counted as twenty independent confirmations.
