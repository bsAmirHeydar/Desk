# V2 Run Envelope and Upstream Binding

P06 binds one V1 RUN2 result to one coherent V2 science stack.

## Required inputs
- V1 `AlphaLab_Run_Capsule` or equivalent canonical base capsule;
- P02 Directional Pressure state;
- P03 Price Transmission state;
- P04 Latent/Release state;
- P05 Gold Intelligence state.

## Binding rules
- subject must be Gold/XAUUSD;
- active horizon must be identical across P02, P03, P04 and the base run horizon;
- P03 must reference the exact supplied P02 fingerprint;
- P04 must reference the exact supplied P02 and P03 fingerprints;
- P05 upstream fingerprints must match the exact supplied P02/P03/P04 states;
- any mismatch fails closed;
- base trade permission is copied verbatim and never recalculated by P06.

P06 creates a new immutable envelope; it never edits the V1 capsule.
