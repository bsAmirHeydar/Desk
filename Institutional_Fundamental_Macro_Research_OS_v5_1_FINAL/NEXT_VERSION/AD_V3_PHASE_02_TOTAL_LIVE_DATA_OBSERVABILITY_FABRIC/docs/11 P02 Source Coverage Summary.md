# P02 Source Coverage Summary

- Gold fact contracts: **192**
- Source contracts: **79**
- Mandatory-attempt fact contracts: **127**

## Acquisition modes

- CALENDAR_DERIVED: 2
- DERIVED_FROM_FACTS: 42
- DERIVED_FROM_STORE: 1
- DIRECT_SNAPSHOT: 97
- DIRECT_STRUCTURED: 21
- LICENSED_GAP: 1
- MULTI_SOURCE_SNAPSHOT: 9
- PAID_GAP: 8
- PRIVATE_GAP: 6
- PROVIDER_GAP: 2
- STATIC_KNOWLEDGE: 3

## Source access classes

- CALENDAR: 1
- KNOWLEDGE: 1
- MODEL_DERIVED: 1
- PAID_ONLY: 3
- PAID_OR_LICENSED: 1
- PAID_OR_SOURCE_SPECIFIC: 1
- PRIVATE_UNOBSERVABLE: 1
- PUBLIC_FREE: 47
- PUBLIC_FREE_DELAYED: 7
- PUBLIC_FREE_DERIVED: 2
- PUBLIC_FREE_OR_DERIVED: 1
- PUBLIC_FREE_OR_PROVIDER: 1
- PUBLIC_FREE_OR_SOURCE_SPECIFIC: 1
- PUBLIC_OR_COMPANY: 1
- PUBLIC_OR_LICENSED: 2
- PUBLIC_OR_PROVIDER: 3
- PUBLIC_OR_SOURCE_SPECIFIC: 4
- PUBLIC_SOURCE_SPECIFIC: 1

## Rule

A public source being listed is not proof that a fact was observed. Runtime coverage requires an attempt record and a fact observation state. Paid/private/provider gaps remain explicit.

## REV 3.2.3 snapshot

- Gold Fact contracts: 192
- Source contracts: 93
- Mandatory-attempt Fact contracts: 126
- Primary objective: remove avoidable real-machine source failures without weakening Direct/Proxy/Gap semantics.

