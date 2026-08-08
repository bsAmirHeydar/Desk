# Signed Transactions and Trade Classification

When transaction-level data exist, signed flow may be derived using venue flags, aggressor markers or an explicit classification algorithm.

Required lineage:
- raw trade source;
- timestamp granularity and clock convention;
- correction/cancel policy;
- classification method/version;
- quote synchronization method if quote-based;
- aggregation interval;
- known dark/OTC/missing venue limitations.

Classifier output is a `DERIVED_FACT`, not an observed participant identity unless the source identifies the actor.
