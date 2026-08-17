# 01 Architecture Ownership Boundary

The architecture registry separates scientific, acquisition, reasoning, deployment, governance, generated, runtime, documentation, legacy, and historical surfaces. `AlphaDesk.ps1` is deployment-owned and may evolve only through versioned downstream governance; that does not mutate P01 science.
