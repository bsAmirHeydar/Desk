# Alpha Desk V2 — Gold Control Room

P13 is a presentation-only post-P12 amendment. It does not own market science.

Normal command:

```powershell
.\AlphaDesk.ps1 run Gold
```

Every successful persisted Gold run writes one canonical object:

`alpha_desk_v2.gold_control_room.v1`

and renders terminal + JSON + Persian RTL HTML from that same object.

Mutable output lives under `ALPHALAB_DATA_ROOT` when set; otherwise the repository sibling `AlphaLab_Data`.

Primary tabs are permanently ordered as: Overview, Pressure, Transmission & Release, Eight Layers, Events & Timing, Runs & Memory, Report & Audit, Data Health.

Renderer laws: Price does not alter Pressure; Volume is not Flow; OI is not Direction; Readiness is not Permission; missing data stays UNKNOWN/PARTIAL.

## Environment certification for live one-command Gold runs

`Run Gold` uses the governed V1 SHADOW runtime and therefore requires a valid C1 environment receipt. P13 release 1.0.2 checks this automatically before P11 runs.

- `./AlphaDesk.ps1 environment-status` shows the receipt state.
- `./AlphaDesk.ps1 environment-certify` performs the live environment attestation.
- `./AlphaDesk.ps1 run Gold` auto-certifies only when the receipt is missing/stale and `OPENAI_API_KEY` is available in the process environment.
- The API key is never written to the repository or AlphaLab_Data by P13.
- The legacy root `AlphaLab.ps1` wrapper is not required when the P11 frozen direct V1 runtime binding passes. No other C1 doctor failure is waived.


## Human-first presentation (P13-HF03)

The canonical Gold Control Room is read in two layers:

1. **Human layer first** — plain Persian: current thesis, why, price relationship, opposing-move state, action context, and what to watch next.
2. **Technical layer second** — canonical codes, provenance, raw evidence, and governance details behind expandable sections.

This is presentation-only. The human text is deterministic and may only translate or summarize canonical upstream states. It may not create a new Direction, Pressure, Release state, Permission, Flow inference, or missing-driver claim. `UNKNOWN` remains an acceptable human answer such as «نامشخص» or «داده کافی نداریم».

The goal is that a trader can understand the report without first decoding machine enums, while an auditor can still open the technical details and inspect the exact canonical codes.


## Contextual learning (P13-HF04)

The Persian guide is distributed across the Control Room instead of living in a separate central manual tab. Wherever a concept needs interpretation, the UI exposes a `؟ / یاد بگیر` control.

Clicking it opens an RTL contextual drawer (desktop) or bottom sheet (mobile) that explains:

- what the concept means;
- why it matters for Gold day trading;
- common interpretation mistakes;
- questions the human should ask to audit the report.

The eight analytical layers each carry their own in-place guide. Overview, Pressure, Transmission/Release, Events, Memory, Audit, and Data Health also expose local guides.

The guide registry is `config/contextual_help_fa.json`. It is presentation-only. Help text cannot calculate or mutate Direction, Pressure, Transmission, Unreleased Pressure, Maturity, Release Readiness, Permission, Flow, or source availability. It exists to teach the human how to read the canonical states, not to become another research model.
