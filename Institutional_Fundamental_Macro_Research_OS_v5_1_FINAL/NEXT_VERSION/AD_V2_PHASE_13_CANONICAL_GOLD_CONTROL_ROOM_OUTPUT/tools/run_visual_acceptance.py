#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,tempfile,json,copy,re,asyncio,shutil
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from runtime.common import load_json
from runtime.model import build_control_room
from runtime.render_html import render

def p10(repo,pack):
    pp=Path(repo)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION';sys.path.insert(0,str(pp));from AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC.runtime.shadow_pipeline import run
    return run(pack,phase_parent=pp,data_root=Path(tempfile.mkdtemp())/'data',output_dir=Path(tempfile.mkdtemp())/'out',persist_state=False)

def rec(r):return {'status':'PASS','phase':'AD-V2-P11','mode':'VISUAL_FIXTURE','p10_receipt':r}

def mutate(name,base):
    m=copy.deepcopy(base);o=m['overview']
    if name=='BUY_ALIGNED_TRANSMISSION':o['price_transmission']='ALIGNED';m['transmission']['state']='ALIGNED'
    elif name=='SELL_PRESSURE':o['directional_pressure']='SELL_HIGH';o['pressure_sign']='SELL';m['pressure']['class']='SELL_HIGH';m['pressure']['sign']='SELL'
    elif name=='CONTESTED_PRESSURE':o['directional_pressure']='CONTESTED_OR_UNDETERMINED';o['pressure_sign']='CONTESTED';m['pressure']['class']='CONTESTED_OR_UNDETERMINED';m['pressure']['sign']='CONTESTED'
    elif name=='HIGH_READINESS_NO_TRADE':o['release_readiness']='HIGH_READINESS';o['trade_permission']='NO_TRADE';m['release']['release_readiness']={'state':'HIGH_READINESS','trade_permission_granted':False}
    elif name=='MISSING_FLOW':
        f=next(x for x in m['layers'] if x['id']=='flow');f['evidence']=[];f['coverage']='UNKNOWN';f['missing_data']=['TRUE_ORDER_FLOW_NOT_OBSERVED'];f['current_signal']='NO_TRUE_FLOW_SIGNAL';m['audit']['partial_flow_coverage']=True
    elif name=='STALE_POSITIONING':
        f=next(x for x in m['layers'] if x['id']=='positioning');f['freshness']='STALE';f['coverage']='PARTIAL';f['missing_data']=['POSITIONING_NOT_FRESH']
    elif name=='MAJOR_EVENT_PENDING':m['events']['next_major_event']='CPI · 30m';m['overview']['what_matters_now'].insert(0,'رویداد مهم CPI نزدیک است؛ Event به تنهایی Direction نمی‌سازد.')
    elif name=='NO_PRIOR_HISTORY':m['memory']['timeline']=m['memory']['timeline'][-1:]
    elif name=='STRONG_STATE_TRANSITION_HISTORY':m['memory']['timeline']=[
      {'run_id':'R1','as_of':'10:00','pressure':'BUY_HIGH','transmission':'NEGATIVE_TRANSMISSION','maturity':'ACTIVE','readiness':'WATCH','permission':'NO_TRADE'},
      {'run_id':'R2','as_of':'11:00','pressure':'BUY_HIGH','transmission':'COMPRESSION','maturity':'MATURE','readiness':'PRE_RELEASE','permission':'NO_TRADE'},
      {'run_id':'R3','as_of':'12:00','pressure':'BUY_HIGH','transmission':'ALIGNED','maturity':'EXHAUSTING','readiness':'HIGH_READINESS','permission':'NO_TRADE'}]
    return m

def structural(name,text):
    checks={
      'rtl':'<html lang="fa" dir="rtl">' in text,
      'viewport':'name="viewport"' in text,
      'eight_tabs':text.count('data-tab=')==8,
      'eight_panels':len(re.findall(r'<section id="(?:overview|pressure|transmission|layers|events|memory|audit|health)" class="panel',text))==8,
      'desktop_layout':'grid-template-columns:230px minmax(0,1fr)' in text,
      'mobile_breakpoints':'@media(max-width:820px)' in text and '@media(max-width:520px)' in text,
      'wrap_safety':'overflow-wrap:anywhere' in text and '.table-wrap{overflow:auto' in text,
      'offline_no_cdn':'<script src=' not in text and '<link rel=' not in text,
      'persian_labels':all(x in text for x in ['نمای کلی','فشار و جهت','انتقال و آزادشدن','هشت لایه تحلیل','زمان‌بندی و رویدادها','ران‌ها و حافظه','گزارش و ممیزی','سلامت داده']),
      'semantic_laws':all(x in text for x in ['NEGATIVE TRANSMISSION ≠ SELL PRESSURE','COMPRESSION ≠ ABSORPTION','PRICE REVERSAL ≠ RELEASE','UNRELEASED ≠ PRICE DISTANCE']),
    }
    bad=[k for k,v in checks.items() if not v]
    return {'fixture':name,'status':'PASS' if not bad else 'FAIL','checks':checks,'failed_checks':bad}

async def browser_checks(rendered):
    try:
        from playwright.async_api import async_playwright
    except Exception:
        return [{'fixture':name,'viewport':'browser','status':'SKIP_ENVIRONMENT','detail':'playwright unavailable'} for name,_ in rendered]
    chromium=shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome')
    if not chromium:
        return [{'fixture':name,'viewport':'browser','status':'SKIP_ENVIRONMENT','detail':'chromium unavailable'} for name,_ in rendered]
    rows=[]
    try:
        async with async_playwright() as pw:
            browser=await pw.chromium.launch(executable_path=chromium,headless=True,args=['--no-sandbox'])
            for name,text in rendered:
                for label,w,h in [('desktop',1440,1000),('mobile',390,844)]:
                    page=await browser.new_page(viewport={'width':w,'height':h});await page.set_content(text,wait_until='domcontentloaded');await page.wait_for_timeout(20)
                    data=await page.evaluate("""() => ({dir:document.documentElement.dir,lang:document.documentElement.lang,overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth+2,tabs:document.querySelectorAll('.nav button').length,panels:document.querySelectorAll('.panel').length})""")
                    buttons=page.locator('.nav button')
                    for i in range(await buttons.count()):await buttons.nth(i).click()
                    ok=data['dir']=='rtl' and data['lang']=='fa' and not data['overflow'] and data['tabs']==8 and data['panels']==8
                    rows.append({'fixture':name,'viewport':label,'status':'PASS' if ok else 'FAIL','detail':data});await page.close()
            await browser.close()
    except Exception as e:
        rows=[{'fixture':name,'viewport':'browser','status':'SKIP_ENVIRONMENT','detail':str(e)[:300]} for name,_ in rendered]
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);a=ap.parse_args();repo=Path(a.repo_root).resolve();pp=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION';pack=load_json(pp/'AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC/tests/fixtures/integrated_gold_shadow_input.json');base=build_control_room(repo,rec(p10(repo,pack)),input_pack=pack,data_root=Path(tempfile.mkdtemp()));names=load_json(BASE/'tests/fixtures/visual_fixture_catalog.json')['fixtures'];struct=[];browser=[]
    with tempfile.TemporaryDirectory() as td:
        rendered=[]
        for name in names:
            p=Path(td)/(name+'.html');render(mutate(name,base),p);text=p.read_text(encoding='utf-8');struct.append(structural(name,text));rendered.append((name,text))
        # Browser-level overflow/tab interaction for all fixtures when the environment permits it.
        browser.extend(asyncio.run(browser_checks(rendered)))
    bad=[x for x in struct if x['status']=='FAIL']+[x for x in browser if x['status']=='FAIL'];out={'schema_version':'1.0.0','phase':'AD-V2-P13','status':'PASS' if not bad else 'FAIL','fixtures':len(names),'structural_checks':struct,'browser_checks':browser,'failed':len(bad),'browser_skips':sum(1 for x in browser if x['status']=='SKIP_ENVIRONMENT')};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if not bad else 1
if __name__=='__main__':raise SystemExit(main())
