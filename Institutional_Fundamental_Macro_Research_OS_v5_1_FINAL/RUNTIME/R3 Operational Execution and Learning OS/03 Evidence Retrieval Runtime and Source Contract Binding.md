# Evidence Retrieval Runtime and Source Contract Binding

R3 operationalizes V21.3 observability without changing its science. P11 decides what is material; R3 maps those fact families to the V21.3 source registry and executes configured source adapters. Every raw capture is content-addressed in R1 before W21 snapshot audit.

## Hard rules
- registration does not imply live availability;
- licensed/private gaps remain explicit;
- proxy never silently replaces direct evidence;
- live unknown publication latency is conservatively no earlier than retrieval;
- current-only material is forbidden in strict historical replay;
- raw bytes, retrieval time, ingestion time, source id, vintage integrity and cutoff are preserved;
- decision-critical unbound evidence is never silently downgraded.

R3 creates a retrieval receipt and R1 visibility receipt. W21 still owns snapshot admission; R3 only retrieves/captures.


## Strict Live Intake Cutoff

A live run cannot fetch evidence *after* its decision cutoff and then pretend the evidence was locally known at that cutoff. R3 therefore uses a pre-run intake for LIVE/SHADOW_LIVE: source-contract snapshots are captured first, their retrieval/ingestion clocks are preserved, and only then is the run's analysis cutoff frozen. The retrieval window and source skew are recorded. This preserves R1's strict live visibility law without backdating on-demand retrieval.

Heterogeneous sources cannot always provide an atomic market-wide snapshot. R3 never hides this limitation: retrieval skew is telemetry, and a decision-critical release inside the intake window requires targeted recheck rather than fictitious simultaneity.


### No Synthetic Live Cutoff

Before live intake completes there is **no frozen decision cutoff**. Retrieval adapters therefore receive `analysis_cutoff_utc = null` plus `capture_mode = LIVE_PRE_RUN`; after capture, the actual intake-completion UTC becomes the run cutoff and every snapshot is validated against it. A synthetic far-future cutoff is forbidden.
