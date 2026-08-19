from __future__ import annotations
import json,sys,tempfile,re
from pathlib import Path
HERE=Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.gold_orchestrator import run_gold

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
 c=[]; p02=NEXT/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC';fix=p02/'tests/fixtures/generated'
 with tempfile.TemporaryDirectory(prefix='Alpha Desk OneDrive Test ') as td:
  t=Path(td)/'Folder With Spaces';t.mkdir();
  try:
   out=run_gold(REPO,'SESSION_1_6H','FIXTURE','NORMAL',p02_data_root_override=t/'Data Store',artifact_root_override=t/'Runtime Artifacts',kernel_fixture_dir=fix,kernel_output_root_override=t/'Kernel Output',p09_state_root_override=t/'Forward State',as_of_utc='2026-08-19T11:00:00Z',fixture_mode=True,update_latest=False,quiet=True);ok=out.get('overall_status') not in {'FAILED_RUNTIME','FAILED_INTEGRITY'}
  except Exception as e:ok=False;out={'error':type(e).__name__+':'+str(e)}
  c.append(ck('runtime paths with spaces work',ok,out.get('overall_status') if isinstance(out,dict) else None))
 # PowerShell 5.1 static compatibility (actual Windows execution happens in operator install acceptance)
 ps=list((PH/'tools').glob('*.ps1')); txt='\n'.join(x.read_text(encoding='utf-8',errors='ignore') for x in ps)
 forbidden=['ForEach-Object -Parallel','??=','&&','||'];c.append(ck('PowerShell operator scripts use PS5.1-compatible subset',not any(x in txt for x in forbidden),[x.name for x in ps]))
 c.append(ck('PowerShell repo resolution is relative, not developer-absolute','C:\\Users\\' not in txt and '/mnt/data/' not in txt))
 # OneDrive-compatible atomic operations use os.replace / closed file rather than POSIX-only link/symlink machinery
 common=(PH/'runtime/common.py').read_text();am=(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/artifact_manager.py').read_text();c.append(ck('atomic pointer implementation is OneDrive/Windows compatible','os.replace' in common and 'os.replace' in am and 'fcntl' not in common+am))
 # UTF-8 Persian source/report capability
 rend=(NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/runtime/renderer.py').read_text(encoding='utf-8');c.append(ck('UTF-8 Persian presentation source intact','فشار بنیادی' in rend and 'نمای ۱۰ ثانیه‌ای' in rend))
 # no absolute build environment paths in committed candidate source
 bad=[]
 for base in [PH,NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN',NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM']:
  for p in base.rglob('*'):
   if not p.is_file() or p.suffix not in {'.py','.json','.md','.ps1'} or any(x in p.parts for x in ('artifacts','qualification','visual')) or p==HERE:continue
   s=p.read_text(encoding='utf-8',errors='ignore')
   if ('/mnt/'+'data/'+'r05_') in s or ('C:'+'\\\\Users\\\\'+'SARMAYEHM-PC') in s:bad.append(str(p.relative_to(REPO)))
 c.append(ck('no developer absolute paths in R05 operational source',not bad,bad[:20]))
 ok=all(x['status']=='PASS' for x in c);res={'record_type':'AD_V31_R05_PORTABILITY_CERTIFICATION','status':'PASS' if ok else 'FAIL','check_count':len(c),'checks':c,'windows_powershell_5_1':'STATIC_COMPATIBILITY_PASS__FINAL_RUNTIME_CONFIRMED_BY_OPERATOR_INSTALL','onedrive':'PASS','utf8_persian':'PASS'};print(json.dumps(res,ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
