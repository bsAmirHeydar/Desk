#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json

def _e(x): return html.escape(str(x if x is not None else '—'))
def _v(obj,*keys):
    cur=obj
    for k in keys:
        if not isinstance(cur,dict): return None
        cur=cur.get(k)
    return cur

def render_html(report,path):
    p=report.get('pressure') or {}; t=report.get('transmission') or {}; l=report.get('latent_release') or {}; g=report.get('gold_evidence') or {}; ex=report.get('execution') or {}; changes=(report.get('changes') or {}).get('items') or []
    change_html=''.join(f"<li><b>{_e(x.get('domain'))}</b> · {_e(x.get('field'))}: {_e(x.get('from'))} → {_e(x.get('to'))}</li>" for x in changes) or '<li>مقایسه معتبر قبلی در دسترس نیست یا تغییر معنایی مهمی ثبت نشده است.</li>'
    data=html.escape(json.dumps(report,ensure_ascii=False,separators=(',',':')))
    doc=f"""<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Alpha Desk V2 — Gold</title><style>
    :root{{--bg:#eee8dc;--paper:#fffdf8;--ink:#171511;--muted:#756f64;--gold:#9b7637;--line:#d8cebd;--dark:#11110f;--soft:#f5efe4}}
    *{{box-sizing:border-box}}body{{margin:0;background:linear-gradient(145deg,#e9e2d6,#f8f4eb 50%,#ece5da);color:var(--ink);font-family:Tahoma,"Segoe UI",sans-serif;line-height:1.85}}.wrap{{width:min(1180px,94%);margin:auto;padding:42px 0 80px}}.brand{{font-family:Georgia,serif;letter-spacing:.14em;color:var(--gold)}}h1{{font-size:44px;margin:4px 0 0}}.lead{{max-width:900px;color:#514c44}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:25px 0}}.card{{background:rgba(255,253,248,.75);border-top:2px solid var(--gold);padding:15px}}.card span,.meta{{display:block;color:var(--muted);font-size:10px}}.card b{{display:block;font-size:18px;margin:3px 0}}section{{margin-top:38px;border-top:1px solid var(--line);padding-top:18px}}h2{{font-size:25px;margin:0 0 12px}}.rows{{display:grid;grid-template-columns:210px 1fr;border-top:1px solid var(--line)}}.rows div{{padding:9px 7px;border-bottom:1px solid var(--line)}}.rows div:nth-child(odd){{font-weight:700}}.warning{{background:var(--soft);border-right:3px solid var(--gold);padding:14px}}ul{{padding-right:22px}}.pill{{display:inline-block;border:1px solid var(--line);border-radius:99px;padding:4px 9px;margin:3px;font-size:10px}}@media(max-width:800px){{.grid{{grid-template-columns:1fr 1fr}}.rows{{grid-template-columns:1fr}}h1{{font-size:34px}}}}</style></head><body><div class="wrap"><div class="brand">ALPHA DESK V2 · SHADOW</div><h1>XAUUSD</h1><p class="lead">Pressure و Price دو لایه مستقل‌اند. این صفحه Directional Pressure را از Price Transmission و Latent/Release جدا نشان می‌دهد؛ Release Readiness به‌تنهایی مجوز معامله نیست.</p>
    <div class="grid"><article class="card"><span>Directional Pressure</span><b>{_e(p.get('class'))}</b><small>{_e(p.get('trend'))}</small></article><article class="card"><span>Price Transmission</span><b>{_e(t.get('state'))}</b><small>{_e(_v(t,'efficiency','class'))}</small></article><article class="card"><span>Unreleased Pressure</span><b>{_e(_v(l,'unreleased','class'))}</b><small>{_e(_v(l,'maturity','state'))}</small></article><article class="card"><span>Release Readiness</span><b>{_e(_v(l,'readiness','state'))}</b><small>Permission: {_e(ex.get('permission'))}</small></article></div>
    <div class="warning"><b>اصل استفاده:</b> اگر Price خلاف Pressure حرکت کند، Pressure خودکار ضعیف نمی‌شود. ابتدا Transmission و Missing Driver بررسی می‌شوند. Liquidity/Absorption فقط hypothesis است مگر شواهد مستقل وجود داشته باشد.</div>
    <section><h2>Pressure</h2><div class="rows"><div>Class</div><div>{_e(p.get('class'))}</div><div>Trend</div><div>{_e(p.get('trend'))}</div><div>Acceleration</div><div>{_e(p.get('acceleration'))}</div><div>Remaining causal pressure</div><div>{_e(p.get('remaining'))}</div><div>Persistence</div><div>{_e(p.get('persistence'))}</div></div></section>
    <section><h2>Transmission</h2><div class="rows"><div>State</div><div>{_e(t.get('state'))}</div><div>Efficiency</div><div>{_e(t.get('efficiency'))}</div><div>Counterfactual residual</div><div>{_e(t.get('residual'))}</div><div>Pathway</div><div>{_e(t.get('pathway'))}</div><div>Missing Driver</div><div>{_e(t.get('missing_driver'))}</div></div></section>
    <section><h2>Latent / Release</h2><div class="rows"><div>Unreleased</div><div>{_e(l.get('unreleased'))}</div><div>Opposing Move</div><div>{_e(l.get('maturity'))}</div><div>Latent Reserve</div><div>{_e(l.get('reserve'))}</div><div>Inflection</div><div>{_e(l.get('inflection'))}</div><div>Readiness</div><div>{_e(l.get('readiness'))}</div><div>Lifecycle</div><div>{_e(l.get('lifecycle'))}</div></div></section>
    <section><h2>Gold Evidence / Coverage</h2><div class="rows"><div>Event Reset</div><div>{_e(g.get('event_reset'))}</div><div>Missing Driver Search</div><div>{_e(g.get('missing_driver_search'))}</div><div>Coverage Gaps</div><div>{_e(g.get('coverage_gaps'))}</div></div></section>
    <section><h2>Changes Since Previous Run</h2><ul>{change_html}</ul></section>
    <section><h2>Execution Authority</h2><div class="rows"><div>Permission</div><div>{_e(ex.get('permission'))}</div><div>Permission Source</div><div>{_e(ex.get('permission_source'))}</div><div>V2 Override Allowed</div><div>{_e(ex.get('v2_override_allowed'))}</div><div>Broker</div><div>{_e(ex.get('broker_authority'))}</div></div></section>
    <p class="meta">Run {_e(report.get('run_id'))} · {_e(report.get('as_of'))} · {_e(report.get('horizon'))}</p><script id="p06-data" type="application/json">{data}</script></div></body></html>"""
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(doc,encoding='utf-8',newline='\n'); return str(path)
