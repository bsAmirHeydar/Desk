from __future__ import annotations
import html,json

def e(x): return html.escape('' if x is None else str(x))
def li(items,empty='مورد مهمی ثبت نشده است.'):
    vals=[x for x in (items or []) if str(x).strip()]
    return ''.join('<li>'+e(x)+'</li>' for x in vals) if vals else '<li class="muted">'+e(empty)+'</li>'

def metric(label,value,sub=None):
    extra=f'<small>{e(sub)}</small>' if sub else ''
    return f'<div class="metric"><span>{e(label)}</span><strong>{e(value)}</strong>{extra}</div>'

def layer1(model):
    h=model['header'];l=model['layer1'];focus=l['focus']
    return f'''<section class="hero layer layer-1" id="layer-1" aria-labelledby="snapshot-title">
<div class="hero-top"><div><div class="eyebrow">ALPHA LAB · L1 · {e(model.get('ux',{}).get('active_view','EXPLORER'))}</div><h1 id="snapshot-title">{e(h.get('subject'))}</h1><p class="request">{e(h.get('original_request'))}</p></div><div class="asof"><span>{e(h.get('as_of'))}</span><small>{e(h.get('horizon'))}</small></div></div>
<div class="focus-answer"><span>{e(focus.get('label_fa'))}</span><strong>{e(focus.get('answer_fa'))}</strong></div>
<div class="metrics">{metric('جهت',l.get('direction_fa'))}{metric('اجازه',l.get('permission_fa'))}{metric('قدرت فشار',l.get('force_fa'))}{metric('چقدر مصرف شده',l.get('consumption_fa'))}{metric('فشار باقی‌مانده',l.get('remaining_pressure_fa'))}{metric('دوام',l.get('persistence_fa'))}{metric('ریسک برگشت',l.get('reversal_risk_fa'))}{metric('بررسی بعدی',l.get('next_review_fa'))}</div>
<div class="now-grid"><div class="now-card"><span>الان مهم‌ترین چیز چیست؟</span><p>{e(l.get('what_matters_now_fa'))}</p></div><div class="now-card"><span>چه چیزی این تحلیل را تغییر می‌دهد؟</span><p>{e(l.get('what_would_change_this_fa'))}</p></div></div>
<a class="down" href="#layer-2">دیدن تصویر کامل ↓</a></section>'''

def card(c):
    sid=c['section_id']
    return f'''<article class="analysis-card" data-state="{e(c.get('stance'))}">
<div class="card-head"><div><h3>{e(c.get('title_fa'))}</h3><span class="relation">{e(c.get('relation_fa'))}</span></div><span class="state">{e(c.get('state_fa'))}</span></div>
<p>{e(c.get('summary_fa'))}</p><div class="important"><span>مهم‌ترین نکته</span>{e(c.get('important_point_fa'))}</div>
<button class="deep-button" type="button" data-deep="{e(sid)}" aria-haspopup="dialog">جزئیات بیشتر</button></article>'''

def causal(c):
    steps=c.get('steps') or []
    if not steps:return '<p class="muted">زنجیره علّی قابل اتکایی برای نمایش ثبت نشده است.</p>'
    arrow='↓' if c.get('identified') else '⋮'
    body=('<span class="arrow">'+arrow+'</span>').join('<span>'+e(x)+'</span>' for x in steps)
    return f'<div class="causal-chain" aria-label="زنجیره اثر">{body}</div><p class="causal-note">{e(c.get("status_fa"))}</p>'

def layer2(model):
    l2=model['layer2'];drv=l2['drivers'];prs=l2['pressure'];chg=l2['changes'];sc=l2['scenarios']
    cards=''.join(card(c) for c in l2['cards'])
    change_html='<ul>'+li(chg.get('items'))+'</ul>' if chg.get('has_comparison') else '<p class="muted">'+e(chg.get('empty_message_fa'))+'</p>'
    scenarios=''.join(f'''<article class="scenario"><h4>{e(s.get('role_fa') or s.get('role'))}</h4><div class="scenario-direction">{e(s.get('direction_fa'))}</div><p><b>شرایط:</b></p><ul>{li(s.get('conditions'))}</ul><p><b>چه چیزی این مسیر را رد می‌کند؟</b></p><ul>{li(s.get('invalidation'))}</ul></article>''' for s in sc) or '<p class="muted">سناریوی ساختاریافته‌ای برای این اجرا ثبت نشده است.</p>'
    return f'''<section class="layer layer-2 shell" id="layer-2" aria-labelledby="overview-title"><div class="section-kicker">L2 · تصویر کامل</div><h2 id="overview-title">همه بخش‌های مهم، به زبان ساده</h2><p class="lead">هر کارت فقط نتیجه اصلی همان بخش را می‌گوید. برای دیدن تحلیل کامل همان بخش، «جزئیات بیشتر» را باز کنید.</p>
<div class="analysis-grid">{cards}</div>
<div class="split"><section class="panel"><h2>الان چه چیزی بازار را حرکت می‌دهد؟</h2><dl class="drivers"><div><dt>عامل اصلی</dt><dd>{e(drv.get('primary_fa') or 'نامشخص')}</dd></div><div><dt>عامل دوم</dt><dd>{e(drv.get('secondary_fa') or 'نامشخص')}</dd></div><div><dt>مهم‌ترین نیروی مخالف</dt><dd>{e(drv.get('opposing_fa') or 'نامشخص')}</dd></div></dl><h3>زنجیره اثر</h3>{causal(l2.get('causal_chain',{}))}</section>
<section class="panel"><h2>فشار و ادامه حرکت</h2><div class="pressure-list">{metric('قدرت نیروی فعلی',prs.get('force_fa'))}{metric('چقدر مصرف شده',prs.get('consumption_fa'))}{metric('فشار باقی‌مانده',prs.get('remaining_pressure_fa'))}{metric('احتمال ادامه ساختاری',prs.get('persistence_fa'))}{metric('ریسک برگشت',prs.get('reversal_fa'))}</div></section></div>
<section class="panel"><h2>از بررسی قبلی چه چیزی تغییر کرده؟</h2>{change_html}</section><section><h2>مسیرهای مهم پیش رو</h2><div class="scenario-grid">{scenarios}</div></section></section>'''

def method_and_apl(model):
    mh=model['method_health'];p=model['perspective'];apl='<p>در حال حاضر نقطه شکنندگی مهمی در تحلیل شناسایی نشده است.</p>' if p.get('quiet') else '<ul>'+li(p.get('material_findings_fa'))+'</ul>'
    return f'''<section class="shell health"><details><summary><span>کیفیت و سلامت تحلیل</span><small>این بخش جهت بازار را تعیین نمی‌کند.</small></summary><p>{e(mh.get('simple_summary_fa'))}</p><dl><div><dt>کلاس تحقیق</dt><dd>{e(mh.get('research_class'))}</dd></div><div><dt>سطح سخت‌گیری</dt><dd>{e(mh.get('rigor_tier'))}</dd></div><div><dt>تعداد خطای سخت</dt><dd>{e(mh.get('hard_failure_count'))}</dd></div></dl><details class="nested"><summary>جزئیات روش و شواهد</summary><pre>{e(json.dumps(mh,ensure_ascii=False,indent=2))}</pre></details></details>
<details><summary><span>بررسی شکنندگی تحلیل</span><small>APL-A فقط ناظر است و Direction را تعیین نمی‌کند.</small></summary>{apl}</details></section>'''

def audit(model):
    ev=e(json.dumps(model.get('evidence_explorer',{}),ensure_ascii=False,indent=2));au=e(json.dumps(model.get('audit',{}),ensure_ascii=False,indent=2))
    return f'''<section class="shell audit"><details><summary>شواهد و منابع کامل</summary><pre>{ev}</pre></details><details><summary>Scientific Audit</summary><pre>{au}</pre></details></section>'''

def deep_dialog(model):
    blob=json.dumps(model.get('layer3',{}).get('sections',{}),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    return f'''<dialog id="deep-dialog" aria-labelledby="deep-title"><div class="dialog-shell"><div class="dialog-head"><div><div class="section-kicker">L3 · تحلیل عمیق</div><h2 id="deep-title">جزئیات بخش</h2></div><button type="button" class="close" aria-label="بستن تحلیل عمیق">×</button></div><div id="deep-body"></div><div class="dialog-nav"><button type="button" id="deep-prev">بخش قبلی</button><button type="button" class="back-overview">بازگشت به نمای کلی</button><button type="button" id="deep-next">بخش بعدی</button></div></div></dialog><script id="deep-data" type="application/json">{blob}</script>'''
