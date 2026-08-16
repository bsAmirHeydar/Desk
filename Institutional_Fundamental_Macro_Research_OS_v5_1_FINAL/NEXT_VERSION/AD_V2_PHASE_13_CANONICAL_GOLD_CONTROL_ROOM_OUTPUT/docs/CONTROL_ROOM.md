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
