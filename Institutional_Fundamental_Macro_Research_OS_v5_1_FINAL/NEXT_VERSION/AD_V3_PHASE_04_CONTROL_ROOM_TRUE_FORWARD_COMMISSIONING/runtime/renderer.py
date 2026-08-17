from __future__ import annotations
import json, html
from .common import human_effect

def esc(x): return html.escape(str(x if x is not None else '—'))

def human_status(v):
    return {
        'SHADOW_COMMISSIONING':'در حال کمیسیون‌گذاری',
        'NO_AUTHORITY':'بدون اختیار معاملاتی',
        'UNTESTED':'تأییدنشده',
        'UNKNOWN':'اثبات‌نشده',
        'LOW':'پایین','MEDIUM':'متوسط','HIGH':'بالا',
        'UNCALIBRATED':'هنوز کالیبره نشده',
        True:'بله', False:'خیر'
    }.get(v,str(v))
def pill(x):
    c='gold' if x in ('BULLISH_GOLD','BEARISH_GOLD') else 'muted'
    return f'<span class="pill {c}">{esc(human_effect(x))}</span>'
def help_btn(key,label='؟'): return f'<button class="help" data-help="{esc(key)}" aria-label="راهنما">{esc(label)}</button>'
def render(model,help_registry):
    e=model['executive_state']; q=model['model_quality']; perm=model['permission']; life=model.get('lifecycle') or {}; tf=model.get('true_forward') or {}
    changes=''.join(f"<div class='change'><b>{esc(x['label'])}</b><span>{esc(x.get('from'))}</span><span>→</span><span>{esc(x.get('to'))}</span></div>" for x in model.get('what_changed',[]))
    material_roots=[r for r in model.get('causal_roots',[]) if r.get('classification') in ('DOMINANT','BACKGROUND')]
    unresolved_roots=[r for r in model.get('causal_roots',[]) if r.get('classification') not in ('DOMINANT','BACKGROUND')]
    def root_html(r): return f"<details class='root'><summary><div><b>{esc(r['root_id'].replace('_',' '))}</b><small>{esc(r.get('classification'))}</small></div>{pill(r.get('direction'))}</summary><div class='rootbody'><p>جهت فعال: <b>{esc(r.get('direction_human'))}</b></p><p>پس‌زمینه: <b>{esc(r.get('background_human'))}</b></p><p class='mono'>Evidence: {esc(', '.join(r.get('evidence_fact_ids') or r.get('background_evidence_fact_ids') or []) or 'none')}</p></div></details>"
    roots=''.join(root_html(r) for r in material_roots)
    if unresolved_roots: roots += f"<details class='root'><summary><div><b>سایر ریشه‌های بررسی‌شده</b><small>{len(unresolved_roots)} unresolved</small></div></summary><div class='rootbody'>{''.join(root_html(r) for r in unresolved_roots)}</div></details>"
    planes=[]
    names=[('causal_fundamental','فشار بنیادی علّی','DIRECTIONAL_PRESSURE'),('realized_transaction','فشار تراکنشی','TRANSACTION_PRESSURE'),('mechanical_forced','فشار مکانیکی','MECHANICAL_PRESSURE'),('structural_carry','ساختار بلندتر','STRUCTURAL_CARRY')]
    for k,name,hk in names:
        p=model['pressure_planes'][k]; planes.append(f"<div class='card'><div class='cardhead'><span>{esc(name)}</span>{help_btn(hk)}</div><h3>{esc(p['direction_human'])}</h3><small>Strength · {esc(p['strength'])}</small></div>")
    lifecycle=''.join(f"<div class='kv'><span>{esc(k.replace('_',' '))}</span><b>{esc(v)}</b></div>" for k,v in (life.get('consumption_vector') or {}).items() if isinstance(v,(str,int,float)))
    unresolved=''.join(f'<span class="tag">{esc(x)}</span>' for x in q.get('unresolved_fact_ids',[])[:24]) or '<span class="muted">موردی نمایش داده نشده</span>'
    helps=json.dumps(help_registry,ensure_ascii=False).replace('</','<\\/')
    raw=json.dumps(model,ensure_ascii=False,indent=2).replace('</','<\\/')
    return f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Alpha Desk V3 · Control Room</title><style>
:root{{--bg:#f7f7f4;--paper:#fff;--ink:#151515;--muted:#77736b;--line:#e8e5dd;--gold:#9b7a37;--goldbg:#f7f1e4;--shadow:0 18px 55px rgba(25,20,10,.055)}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:Tahoma,"Segoe UI",Arial,sans-serif;line-height:1.85}}.wrap{{width:min(1420px,94%);margin:auto;padding:22px 0 80px}}.top{{position:sticky;top:10px;z-index:10;display:flex;justify-content:space-between;gap:16px;align-items:center;padding:13px 17px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.9);backdrop-filter:blur(18px);box-shadow:var(--shadow)}}.brand b{{letter-spacing:.08em}}.brand small,.muted,small{{color:var(--muted);font-size:11px}}.status{{display:flex;gap:7px;flex-wrap:wrap}}.pill,.tag{{display:inline-flex;padding:5px 9px;border-radius:999px;background:#f1f0ec;color:#5c5953;font-size:11px;font-weight:700}}.pill.gold{{background:var(--goldbg);color:#76591e}}.hero{{margin-top:18px;background:var(--paper);border:1px solid var(--line);border-radius:25px;padding:30px;box-shadow:var(--shadow)}}.eyebrow{{color:var(--gold);font-size:11px;font-weight:800;letter-spacing:.08em}}h1{{font-size:34px;margin:5px 0 8px;line-height:1.55}}h2{{font-size:21px;margin:0}}h3{{font-size:18px;margin:10px 0 2px}}.lead{{max-width:1050px;color:#403d37;font-size:15px}}.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:11px;margin-top:18px}}.metric,.card,.box{{border:1px solid var(--line);background:var(--paper);border-radius:17px;padding:16px}}.metric span,.cardhead{{font-size:11px;color:var(--muted)}}.metric b{{display:block;font-size:17px;margin-top:5px}}.section{{margin-top:16px;background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:22px;box-shadow:0 10px 36px rgba(30,24,14,.03)}}.head{{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:13px}}.help{{border:1px solid #d8c9a5;background:#fffaf0;color:#795b20;width:25px;height:25px;border-radius:50%;cursor:pointer;font-weight:900}}.cardhead{{display:flex;justify-content:space-between;align-items:center}}.change{{display:grid;grid-template-columns:1.2fr 1fr 30px 1fr;gap:8px;padding:10px 0;border-bottom:1px solid var(--line);font-size:12px}}.root{{border-bottom:1px solid var(--line);padding:5px 0}}.root summary{{display:flex;justify-content:space-between;gap:12px;align-items:center;cursor:pointer;padding:10px 4px}}.root small{{display:block}}.rootbody{{padding:0 12px 12px;color:#494640}}.mono{{direction:ltr;text-align:left;font-family:Consolas,monospace;font-size:10px;color:#777}}.kv{{display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid var(--line);font-size:12px}}.tags{{display:flex;gap:6px;flex-wrap:wrap}}.tag{{font-family:Consolas,monospace;font-size:9px;font-weight:500}}.note{{background:#fbf8f1;border-right:3px solid var(--gold);padding:13px 15px;border-radius:11px;color:#4c473e}}details.tech summary{{cursor:pointer;font-weight:700}}pre{{direction:ltr;text-align:left;white-space:pre-wrap;word-break:break-word;background:#111;color:#ddd;border-radius:14px;padding:16px;max-height:620px;overflow:auto;font-size:10px}}.drawer{{position:fixed;top:14px;bottom:14px;right:14px;width:min(450px,calc(100vw - 28px));background:#fff;border:1px solid #ded4bd;border-radius:22px;box-shadow:0 28px 90px rgba(20,17,10,.2);z-index:30;transform:translateX(calc(100% + 30px));transition:.2s;overflow:auto;padding:20px}}.drawer.open{{transform:translateX(0)}}.drawer .close{{float:left;border:0;background:#eee9dc;border-radius:50%;width:32px;height:32px;cursor:pointer}}@media(max-width:900px){{.grid4{{grid-template-columns:1fr 1fr}}h1{{font-size:27px}}.change{{grid-template-columns:1fr}}}}@media(max-width:520px){{.grid4{{grid-template-columns:1fr}}.hero,.section{{padding:17px}}}}
</style></head><body><div class="wrap"><header class="top"><div class="brand"><b>ALPHA DESK V3</b><small>GOLD · SHADOW CONTROL ROOM</small></div><div class="status"><span class="pill">{esc(human_status(model['deployment_mode']))}</span><span class="pill">{esc(human_status(perm['official_permission']))}</span></div></header>
<section class="hero"><div class="eyebrow">CURRENT GOLD STATE</div><h1>{esc(e['summary'])}</h1><p class="lead">این صفحه نتیجه‌ی P01–P03 را ترجمه می‌کند؛ خودش Direction جدید نمی‌سازد. اگر evidence کافی نباشد، UNKNOWN همان پاسخ معتبر سیستم است.</p><div class="grid4"><div class="metric"><span>فشار جهت‌دار {help_btn('DIRECTIONAL_PRESSURE')}</span><b>{esc(e['direction_human'])}</b></div><div class="metric"><span>پس‌زمینه {help_btn('BACKGROUND_BIAS')}</span><b>{esc(e['background_human'])}</b></div><div class="metric"><span>انتقال قیمت {help_btn('PRICE_TRANSMISSION')}</span><b>{esc(human_status(e['price_transmission']))}</b></div><div class="metric"><span>Desk Action {help_btn('PERMISSION')}</span><b>{esc(e['desk_action_human'])}</b></div></div></section>
<section class="section"><div class="head"><h2>چه چیزی نسبت به Run قبل تغییر کرد؟</h2><span class="muted">Change-first view</span></div>{changes}</section>
<section class="section"><div class="head"><h2>چهار Pressure Plane</h2><span class="muted">جدا و غیرقابل ادغام</span></div><div class="grid4">{''.join(planes)}</div></section>
<section class="section"><div class="head"><h2>Rootهای علّی</h2><span class="muted">Intake exhaustive · Decision sparse</span></div>{roots}</section>
<section class="section"><div class="head"><h2>Transmission و کیفیت مدل</h2>{help_btn('MODEL_COMPLETENESS')}</div><div class="grid4"><div class="metric"><span>Model Completeness</span><b>{esc(human_status(q.get('model_completeness')))}</b></div><div class="metric"><span>Missing Driver Risk {help_btn('MISSING_DRIVER')}</span><b>{esc(human_status(q.get('missing_driver_risk')))}</b></div><div class="metric"><span>Resolved Roots</span><b>{esc(q.get('resolved_root_families'))}</b></div><div class="metric"><span>Semantic Unknowns</span><b>{esc(q.get('semantic_unknown_items'))}</b></div></div><div class="grid4"><div class="metric"><span>Semantic Mode</span><b>{esc(q.get('semantic_mode'))}</b></div><div class="metric"><span>Semantic Validated</span><b>{esc(q.get('semantic_validated_items'))}</b></div><div class="metric"><span>Semantic Rejected / Fallback</span><b>{esc(str(q.get('semantic_rejected_items'))+' / '+str(q.get('semantic_fallback_items')))}</b></div><div class="metric"><span>Semantic Host</span><b>{esc(q.get('semantic_model_host_state'))}</b></div></div><h3>Unresolved / blind spots</h3><div class="tags">{unresolved}</div></section>
<section class="section"><div class="head"><h2>Lifecycle</h2>{help_btn('PERSISTENCE')}</div>{lifecycle or '<p class="muted">Lifecycle هنوز قابل اثبات نیست.</p>'}</section>
<section class="section"><div class="head"><h2>True-Forward Commissioning</h2>{help_btn('TRUE_FORWARD')}</div><div class="grid4"><div class="metric"><span>Sample State</span><b>{esc(human_status(tf.get('sample_state')))}</b></div><div class="metric"><span>Total Capsules</span><b>{esc(tf.get('total_capsules'))}</b></div><div class="metric"><span>Evaluated Outcomes</span><b>{esc(tf.get('outcomes_evaluated'))}</b></div><div class="metric"><span>Promotion Ready</span><b>{esc(human_status(tf.get('promotion_ready')))}</b></div></div><p class="note">قبل از آینده precommit ثبت می‌شود. هیچ درصد اعتماد مصنوعی از sample کوچک ساخته نمی‌شود.</p></section>
<section class="section"><details class="tech"><summary>جزئیات فنی و Lineage</summary><pre>{esc(raw)}</pre></details></section></div><aside class="drawer" id="drawer"><button class="close" id="close">×</button><div id="helpbody"></div></aside><script>const H={helps};document.querySelectorAll('[data-help]').forEach(b=>b.onclick=()=>{{const x=H[b.dataset.help]||{{title:b.dataset.help,short:'',body:''}};document.getElementById('helpbody').innerHTML=`<div class="eyebrow">INLINE GUIDE</div><h2>${{x.title}}</h2><p class="note">${{x.short}}</p><p>${{x.body}}</p>`;document.getElementById('drawer').classList.add('open')}});document.getElementById('close').onclick=()=>document.getElementById('drawer').classList.remove('open');</script></body></html>'''

def brief(model):
    e=model['executive_state']; q=model['model_quality']; p=model['permission']; tf=model['true_forward']; comp=model.get('comparison') or {}
    reason=e['summary']
    uncertainty=[]
    if q.get('model_completeness') in ('LOW','UNKNOWN'): uncertainty.append('کامل‌بودن مدل محدود است')
    if q.get('missing_driver_risk') in ('MEDIUM','HIGH'): uncertainty.append('ریسک Driver گمشده معنادار است')
    if e.get('transaction_direction')=='UNKNOWN': uncertainty.append('فلو تراکنشی جهت قابل اتکایی نمی‌دهد')
    if e.get('mechanical_direction')=='UNKNOWN': uncertainty.append('فشار مکانیکی حل نشده است')
    why_wait='؛ '.join(uncertainty) if uncertainty else 'محدودیت اضافه‌ای ثبت نشده است'
    compared=(f"مقایسه با Run {comp.get('compared_to_run_id')}" if comp.get('available') else 'Run مقایسه‌ای قبلی در دسترس نیست')
    return '\n'.join([
        'ALPHA DESK V3 — GOLD',
        reason,
        '',
        f"جمع‌بندی عملیاتی: {e['desk_action_human']}",
        f"چرا؟ {why_wait}.",
        f"Price Transmission: {human_status(e['price_transmission'])}",
        f"Model Completeness: {human_status(q.get('model_completeness'))}",
        f"Missing Driver Risk: {human_status(q.get('missing_driver_risk'))}",
        f"Semantic: {q.get('semantic_mode')} · validated {q.get('semantic_validated_items',0)} · rejected {q.get('semantic_rejected_items',0)} · fallback {q.get('semantic_fallback_items',0)}",
        compared,
        '',
        f"True-Forward: {human_status(tf.get('sample_state'))} · {tf.get('outcomes_evaluated')} outcome evaluated",
        'Official trade permission: ' + human_status(p.get('official_permission')),
        'Production trade execution authority: FALSE'
    ])+'\n'
