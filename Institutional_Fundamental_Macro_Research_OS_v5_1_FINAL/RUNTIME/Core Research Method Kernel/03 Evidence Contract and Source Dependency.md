# Evidence Contract and Source Dependency

The method evidence adapter consumes existing D1 `Fact_Record` and `Decision_Evidence_Pack` objects without redefining them. It adds an audit view that preserves source identity, root source, availability, materiality and point-in-time fields. `build_dependency_graph` groups evidence by underlying roots; distinct URLs are not treated as independent by default.

Missing new method metadata on legacy-valid D1 facts is a warning/research route, not an automatic hard failure. Explicit future leakage, unavailable-as-zero collapse, or corrupted decision-critical provenance is hard invalidity.
