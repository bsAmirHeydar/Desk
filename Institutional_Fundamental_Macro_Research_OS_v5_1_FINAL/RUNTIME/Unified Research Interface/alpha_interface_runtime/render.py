from pathlib import Path
import json,html,subprocess,shutil
from .util import now

FA={'BULLISH':'صعودی','STRONGLY_BULLISH':'صعودی قوی','BEARISH':'نزولی','STRONGLY_BEARISH':'نزولی قوی','NEUTRAL':'خنثی','MIXED':'ترکیبی','UNRESOLVED':'حل‌نشده','UNDETERMINED':'نامشخص','BUY':'فقط خرید','SELL':'فقط فروش','NO_TRADE':'بدون معامله','HIGH':'بالا','MODERATE':'متوسط','LOW':'پایین','VERY_HIGH':'خیلی بالا','VERY_LOW':'خیلی پایین','FAVORABLE':'مطلوب','HIGHLY_FAVORABLE':'بسیار مطلوب','DEGRADED':'کاهش‌یافته','BALANCED':'متعادل','INSUFFICIENT_EVIDENCE':'شواهد ناکافی','CONTESTED':'مورد اختلاف'}
def f(x):
    if x is None:return 'نامشخص'
    if isinstance(x,(dict,list)):return html.escape(json.dumps(x,ensure_ascii=False))
    return html.escape(FA.get(str(x).upper(),str(x)))
def _li(vals):
    return ''.join('<li>'+f(x)+'</li>' for x in (vals or [])) or '<li>مورد مهمی ثبت نشده است.</li>'
def explorer_html(model,view='EXPLORER'):
    h=model['header'];d=model['decision_strip'];cards=model['analytical_cards'];prs=model['pressure'];pers=model['perspective'];mh=model['method_health']
    card_html=''.join(f'''<details class="card"><summary><b>{html.escape(c['id'])}</b><span>{f(c.get('state'))}</span></summary><p>{f(c.get('summary_fa'))}</p><pre>{html.escape(json.dumps(c.get('detail'),ensure_ascii=False,indent=2))}</pre></details>''' for c in cards)
    scen=''.join(f'''<details><summary>{f(s.get('role'))} — {f(s.get('direction'))}</summary><p><b>شرایط:</b></p><ul>{_li(s.get('conditions'))}</ul><p><b>ابطال:</b></p><ul>{_li(s.get('invalidation'))}</ul></details>''' for s in model['scenarios']) or '<p>سناریوی ساختاریافته‌ای برای این اجرا موجود نیست.</p>'
    apl='<p>شکنندگی مهمی از لایه APL-A ثبت نشده است.</p>' if pers.get('quiet') else '<ul>'+_li(pers.get('material_findings'))+'</ul>'
    audit=html.escape(json.dumps(model['audit'],ensure_ascii=False,indent=2));evid=html.escape(json.dumps(model['evidence_explorer'],ensure_ascii=False,indent=2))
    return f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Alpha Lab — {html.escape(str(h.get('subject')))}</title><style>
:root{{--bg:#f4f0e7;--ink:#111;--muted:#6b665d;--gold:#9a7b38;--panel:#fffdf8;--line:#d8d0c1}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:Tahoma,"Segoe UI",sans-serif;line-height:1.85}}main{{max-width:1180px;margin:auto;padding:38px 28px 80px}}header{{border-bottom:1px solid var(--line);padding-bottom:24px;margin-bottom:24px}}h1{{font-size:31px;margin:0 0 8px}}.eyebrow{{color:var(--gold);letter-spacing:.08em;font-size:12px}}.muted{{color:var(--muted)}}.strip{{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:10px;margin:20px 0 32px}}.metric{{background:#111;color:#fff;padding:14px 16px;border-radius:10px}}.metric small{{display:block;color:#c8b98d}}.metric b{{font-size:18px}}section{{margin:34px 0}}h2{{font-size:20px;border-right:3px solid var(--gold);padding-right:10px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:12px}}details{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 15px;margin:8px 0}}summary{{cursor:pointer;display:flex;justify-content:space-between;gap:10px}}pre{{direction:ltr;text-align:left;white-space:pre-wrap;overflow:auto;background:#171717;color:#eee;padding:12px;border-radius:8px;font-size:11px}}.note{{border-right:3px solid var(--gold);background:#fff9ea;padding:12px 16px}}table{{width:100%;border-collapse:collapse}}td,th{{border-bottom:1px solid var(--line);padding:8px;text-align:right}}@media(max-width:600px){{main{{padding:22px 14px}}h1{{font-size:25px}}}}
</style></head><body><main><header><div class="eyebrow">ALPHA LAB · {html.escape(view)}</div><h1>{html.escape(str(h.get('subject')))}</h1><div class="muted">{html.escape(str(h.get('original_request') or ''))}</div><div class="muted">برش زمانی: {html.escape(str(h.get('as_of')))} · افق: {html.escape(str(h.get('horizon')))}</div></header>
<div class="strip"><div class="metric"><small>جهت</small><b>{f(d.get('direction'))}</b></div><div class="metric"><small>اجازه</small><b>{f(d.get('permission'))}</b></div><div class="metric"><small>قدرت فشار</small><b>{f(d.get('pressure_strength'))}</b></div><div class="metric"><small>مصرف</small><b>{f(d.get('consumption'))}</b></div><div class="metric"><small>فشار باقی‌مانده</small><b>{f(d.get('remaining_pressure'))}</b></div><div class="metric"><small>ریسک برگشت</small><b>{f(d.get('reversal_risk'))}</b></div></div>
<section><h2>لایه‌های تحلیلی</h2><div class="grid">{card_html}</div></section>
<section><h2>چه چیزی بازار را حرکت می‌دهد؟</h2><table><tr><th>محرک اصلی</th><td>{f(model['drivers'].get('primary'))}</td></tr><tr><th>محرک دوم</th><td>{f(model['drivers'].get('secondary'))}</td></tr><tr><th>نیروی مخالف</th><td>{f(model['drivers'].get('opposing'))}</td></tr></table></section>
<section><h2>فشار، مصرف و ادامه حرکت</h2><table><tr><th>Force</th><td>{f(prs.get('force'))}</td></tr><tr><th>Consumption</th><td>{f(prs.get('consumption'))}</td></tr><tr><th>Remaining pressure</th><td>{f(prs.get('remaining_pressure'))}</td></tr><tr><th>Persistence</th><td>{f(prs.get('persistence'))}</td></tr><tr><th>Reversal</th><td>{f(prs.get('reversal'))}</td></tr></table></section>
<section><h2>سناریوها</h2>{scen}</section>
<section><h2>سلامت روش و شواهد</h2><div class="note">این بخش کیفیت تحقیق را توصیف می‌کند و جهت بازار را تعیین نمی‌کند.</div><p>وضعیت M1: <b>{f(mh.get('status'))}</b> · کلاس تحقیق: {f(mh.get('research_class'))} · سطح سخت‌گیری: {f(mh.get('rigor_tier'))}</p><details><summary>جزئیات Method/Evidence</summary><pre>{html.escape(json.dumps(mh,ensure_ascii=False,indent=2))}</pre></details></section>
<section><h2>Perspective / Fragility Check</h2><div class="note"><b>APL-A فقط Shadow Perspective است و Direction را تعیین نمی‌کند.</b></div>{apl}</section>
<section><h2>Evidence Explorer</h2><details><summary>ردیابی شواهد و artifactها</summary><pre>{evid}</pre></details></section>
<section><h2>Scientific Audit</h2><details><summary>جزئیات کامل audit</summary><pre>{audit}</pre></details></section>
</main></body></html>'''

def render_files(out_dir,model,profile='EXPLORER'):
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True);rid=model['audit']['run_id'];stem=rid+'_'+profile.lower();jp=out/(stem+'.report.json');hp=out/(stem+'.html');jp.write_text(json.dumps(model,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8');hp.write_text(explorer_html(model,profile),encoding='utf-8')
    return {'report_model_path':str(jp),'html_path':str(hp),'pdf_path':None,'profile':profile}

def render_pdf_from_html(html_path,pdf_path):
    candidates=[shutil.which('msedge'),shutil.which('msedge.exe'),shutil.which('chrome'),shutil.which('chrome.exe'),shutil.which('chromium'),shutil.which('chromium-browser')]
    exe=next((x for x in candidates if x),None)
    if not exe:return {'status':'PENDING','reason':'NO_HEADLESS_BROWSER_FOUND','pdf_path':None}
    p=Path(pdf_path).resolve();u=Path(html_path).resolve().as_uri();q=subprocess.run([exe,'--headless','--disable-gpu','--no-pdf-header-footer','--print-to-pdf='+str(p),u],capture_output=True,text=True,timeout=120)
    return {'status':'PASS' if q.returncode==0 and p.is_file() else 'FAIL','pdf_path':str(p) if p.is_file() else None,'stderr':q.stderr[-2000:]}
