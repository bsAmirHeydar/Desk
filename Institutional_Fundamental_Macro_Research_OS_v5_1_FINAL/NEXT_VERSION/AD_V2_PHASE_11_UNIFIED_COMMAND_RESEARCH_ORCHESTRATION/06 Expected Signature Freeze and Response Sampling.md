# Expected signature freeze

P11 mechanically inserts the P02 Pressure fingerprint and the seal timestamp into the expected signature. A new observation window starts only after that seal.

Default response sampling is short and configurable. A short window may legitimately produce `NOT_YET_OBSERVABLE` or `DELAYED`; P11 must not fake a mature transmission state for convenience.