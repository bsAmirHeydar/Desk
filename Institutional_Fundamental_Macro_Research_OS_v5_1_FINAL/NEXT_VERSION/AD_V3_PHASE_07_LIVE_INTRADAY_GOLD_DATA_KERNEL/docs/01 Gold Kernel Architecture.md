# 01 Gold Kernel Architecture

P07 is a scheduling/governance layer around P02. It does not duplicate parsers or observation schemas. It preserves a full 192-observation current snapshot for P03 while reducing external refresh work through a point-in-time-safe context cache.
