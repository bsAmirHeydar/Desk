from __future__ import annotations
import argparse,json,pathlib,sys

def main():
 ap=argparse.ArgumentParser();ap.add_argument('html');ap.add_argument('--screenshots');a=ap.parse_args();hp=pathlib.Path(a.html).resolve();outdir=pathlib.Path(a.screenshots).resolve() if a.screenshots else None
 if outdir:outdir.mkdir(parents=True,exist_ok=True)
 try:
  from playwright.sync_api import sync_playwright
 except Exception as e:
  print(json.dumps({'status':'NOT_RUN_ENVIRONMENT_UNAVAILABLE','reason':str(e)},ensure_ascii=False,indent=2));return 0
 viewports=[('1920',1920,1080),('1440',1440,900),('1366',1366,768),('tablet',768,1024),('mobile',390,844)];checks=[]
 try:
  with sync_playwright() as p:
   b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
   for name,w,h in viewports:
    page=b.new_page(viewport={'width':w,'height':h});page.set_content(hp.read_text(encoding='utf-8'),wait_until='load')
    m=page.evaluate('''() => ({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,dir:document.documentElement.dir,lang:document.documentElement.lang,decision:!!document.querySelector('.decision-strip'),evidence:!!document.querySelector('#evidence'),focusables:document.querySelectorAll('a,summary,input,select,button').length})''')
    ok=m['sw']<=m['cw']+2 and m['dir']=='rtl' and m['lang']=='fa' and m['decision'] and m['evidence'] and m['focusables']>5
    checks.append({'viewport':name,'width':w,'height':h,'status':'PASS' if ok else 'FAIL','metrics':m})
    if outdir and name in {'1440','mobile'}:page.screenshot(path=str(outdir/f'{name}.png'),full_page=True)
    page.close()
   b.close()
 except Exception as e:
  print(json.dumps({'status':'NOT_RUN_ENVIRONMENT_UNAVAILABLE','reason':str(e),'checks':checks},ensure_ascii=False,indent=2));return 0
 ok=all(x['status']=='PASS' for x in checks);print(json.dumps({'status':'PASS' if ok else 'FAIL','checks':checks},ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
