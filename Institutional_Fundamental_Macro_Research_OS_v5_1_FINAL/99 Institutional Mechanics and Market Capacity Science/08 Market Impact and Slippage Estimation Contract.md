# Market Impact and Slippage Estimation

Any expected impact model is `DERIVED_FACT`/`MODEL_INFERENCE` and must declare:
- calibration universe/window;
- volume/depth inputs;
- volatility input;
- order-size definition;
- temporary vs permanent impact if modeled;
- participation and schedule;
- confidence range;
- regime limitations.

Never infer institutional capacity solely from average daily volume. OTC FX and physical/OTC gold require venue-specific or licensed evidence for strong capacity claims.
