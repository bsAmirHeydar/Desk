# Gold Fact Acquisition Mapping

P02 maps all **192** P01 facts. Mandatory public acquisition contracts: **127**. Each contract declares mode, sources, horizons, materiality, failure policy, dependencies, discovery terms and directness.

## REV 3.2.3 mappings

The first real coverage receipt exposed blocking BLS/Census/CME/PBoC/SGE/H.10 paths. Mapping now routes BLS CPI/PPI/labor/JOLTS through one official API batch, retail sales through an official Federal Reserve republisher as PUBLIC_PROXY, 5y5y through Treasury-derived breakevens, Gold/Fed-funds futures through CME delayed web JSON plus Daily Bulletin fallbacks, and China/India fallbacks through explicitly-labelled proxy observations.

