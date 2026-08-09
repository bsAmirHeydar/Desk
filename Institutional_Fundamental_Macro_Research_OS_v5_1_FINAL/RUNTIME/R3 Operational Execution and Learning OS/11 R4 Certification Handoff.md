# R4 Certification Handoff — ACTIVE

R3 operational execution is now consumed by R4 certification. R4 has zero new market-direction or permission authority. It validates R1/R2/R3, enforces prompt/context drift guards and separates offline runtime certification from actual production-environment attestation.

`R3 → R4` handoff contract:
- R3 remains `BLOCK_ONLY` operational authority.
- R4 may block certification; it may not create a market direction or trade permission.
- Production provider/model and source bindings remain un-certified until environment attestation.
- Reproduction requires exact visibility and invocation parity; decision parity is certified against the actual bound host.
