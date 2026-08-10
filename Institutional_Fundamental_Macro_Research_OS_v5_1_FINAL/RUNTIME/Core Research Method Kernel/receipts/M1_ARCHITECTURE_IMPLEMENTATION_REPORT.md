# Alpha Lab — M1 Core Research Method & Epistemology Hardening

## Architecture / Implementation Report

### Detected baseline

- Scientific stack: **V21.3.0**
- Runtime: **R4.0.0**
- Commissioning: **C1.0.0**
- APL-A: **INSTALLED_SHADOW_FORWARD_VALIDATION_REQUIRED / SHADOW_ONLY**
- Baseline R4 surface: **sha256:1907e99708730e7f81b1bfe32789c520a89a9e8f9b5d9442569bbbb1d728e758**
- Baseline APL-A: 26/26 self-test, 30/30 acceptance, parity PASS.

### Installed architecture

M1 is installed as a **cross-cutting research-method governance layer**, not as R5 and not as a parallel Fundamental Engine. It uses the existing R1/R2/R3/R4 boundaries and stores Method Plan/validation artifacts in the **META world**.

The architecture is **Invariant Constitution + Adaptive Protocol Shell**:

- invariant research constitution: no-lookahead, provenance, fact/inference separation, UNKNOWN preservation, no fake precision, causal authority discipline, contradiction visibility, source-dependency visibility, versioned/auditable method behavior;
- adaptive protocols: 13 explicit research classes with LIGHT/STANDARD/DEEP/CRITICAL rigor routing and asset/horizon-aware selection.

### Reused instead of duplicated

- R1 point-in-time visibility, storage, lineage and sealing;
- R2 prompt/process orchestration and Decision World;
- R3 operational/learning boundaries;
- R4 fingerprinting/certification;
- V21.3 evidence/cognitive and hypothesis discipline;
- existing Direction and Permission authorities;
- APL-A as a separate perspective/challenger layer.

### New operational components

- machine-readable claim ontology and claim lifecycle;
- evidence/source dependency contract and pseudo-independence detection;
- uncertainty / precision governance;
- causal-claim and identification governance;
- explicit rival-hypothesis / invalidation discipline;
- adaptive protocol router;
- Method Plan and Method Receipt schemas;
- exception and quarantine schemas/policies;
- proxy contracts and model-method cards;
- runtime phase validation hooks;
- 12 required adversarial fixtures plus flexibility/authority/parity checks;
- R4 inherited certification binding (`R4-004 M1_METHOD`).

### Runtime integration

1. **PRE-RESEARCH / R2 bootstrap:** create Method Plan in META.
2. **Post-evidence:** validate point-in-time, UNKNOWN, source dependence, directness/proxy/model semantics.
3. **Post-cognition:** validate causal/claim/contradiction/hypothesis discipline.
4. **PRE-DECISION:** validate method integrity before sealing.
5. Only hard methodological invalidity can block pre-seal. Soft perspective concerns cannot directly change Direction or Permission.

### Authority boundary

M1 authority is deliberately conservative:

- Fact authority: **NONE**
- Direction authority: **NONE**
- Permission authority: **NONE**
- Broker write: **NONE**
- Scientific mutation: **NONE**
- Hard methodological invalidity: **BLOCK_PRESEAL_ONLY**

APL-A remains **SHADOW_ONLY**. APL-B is **NOT IMPLEMENTED**.

### Decision parity

Method parity test: **PASS**. For valid runs, Decision World artifacts are byte-identical and lifecycle event sequence is identical with M1 enabled/disabled; M1 artifacts are META-only.

### Certification

- M1 self-test: **33/33 PASS**
- M1 acceptance: **33/33 PASS**
- M1 parity: **PASS**
- R1/R2/R3 preflights: **PASS**
- C1 self-test: **31/31 PASS**
- APL-A: **26/26 self-test, 30/30 acceptance, parity PASS**
- R4 preflight: **PASS**
- R4 CORE: **CORE_CERTIFIED**, 47 cases
- R4 FULL: **FULL_OFFLINE_CERTIFIED**, 47 cases
- Certified surface: **sha256:520c86dfaa7299dc73d7d6d1ac2543050199551c5a009ac701d48784f6b4245a**, 491 authoritative files

### Taleb vault boundary

The supplied Taleb vault matches the APL extraction receipt **696/696 by SHA-256**. Existing dispositions remain: **183 INTEGRATED / 433 CONTEXT_ONLY / 80 DEFER_TO_APL_B**. No APL-B runtime was added.

### Performance / complexity budget

Synthetic R2 bootstrap median increased from **19.676 ms** to **36.483 ms** (approximately **+16.807 ms** in this local fixture). This is a bootstrap microbenchmark, not a provider/production latency claim. Heavy methodological checks remain conditional rather than forcing deep review for trivial questions.

### Explicit non-changes

- no new Direction Science;
- no parallel Fundamental Engine;
- no Taleb score or Epistemology score;
- no APL-A promotion;
- no APL-B;
- no broker authority;
- no silent historical rewrite;
- no changes to valid BUY/SELL/NO_TRADE behavior.

### Remaining limitations / gates

1. C1 host/environment certification is still host-specific and pending.
2. Six-market production-shadow certification remains a real-environment gate.
3. M1 requires forward validation before any new behavioral authority.
4. APL-A requires its own forward validation before any future promotion decision.
5. Final APL certification/promotion is intentionally not part of this deployment.
