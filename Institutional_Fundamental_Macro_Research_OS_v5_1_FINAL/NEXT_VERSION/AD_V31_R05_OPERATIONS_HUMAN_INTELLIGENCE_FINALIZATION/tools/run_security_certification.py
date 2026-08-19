\
from __future__ import annotations
import json,sys,subprocess,re,os
from pathlib import Path
HERE=Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1]

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
 c=[]
 # leverage canonical P11 adversarial security acceptance
 cp=subprocess.run([sys.executable,str(NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/tools/run_phase11_acceptance.py')],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=300)
 try:p11=json.loads(cp.stdout)
 except Exception:p11={}
 checks={x.get('name'):x.get('status') for x in p11.get('checks',[])}
 c.append(ck('XSS/HTML injection escaping PASS',cp.returncode==0 and checks.get('XSS evidence is escaped and never executable')=='PASS'))
 c.append(ck('unsafe source URL blocking PASS',checks.get('unsafe source URLs blocked')=='PASS'))
 # secret scan committed source candidate (exclude baseline hashes/cert data; search clear credential assignments/tokens)
 bad=[]; pats=[re.compile(r'(?i)(api[_-]?key|token|password|secret)\s*[=:]\s*[\"\']?[A-Za-z0-9_\-]{20,}'),re.compile(r'(?i)bearer\s+eyJ[A-Za-z0-9._-]+'),re.compile(r'sk-[A-Za-z0-9]{20,}')]
 for base in [PH,NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN',NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM']:
  for p in base.rglob('*'):
   if not p.is_file() or p.suffix.lower() not in {'.py','.json','.md','.ps1','.html','.txt'}:continue
   if '__pycache__' in p.parts or 'artifacts' in p.parts:continue
   t=p.read_text(encoding='utf-8',errors='ignore')
   if any(x.search(t) for x in pats):bad.append(str(p.relative_to(REPO)))
 c.append(ck('committed-source obvious secret scan clean',not bad,bad[:20]))
 # no secrets logged by operations runtime
 rt='\n'.join(x.read_text(encoding='utf-8',errors='ignore') for x in (PH/'runtime').glob('*.py')); c.append(ck('operations logs/status do not emit credential values',"get('OPENAI_API_KEY')" in rt and "return 'CONFIGURED'" in rt and 'print(os.environ' not in rt and 'json.dumps(os.environ' not in rt))
 # report path safety / CLI command injection: no shell=True and governed report opening retained
 alpha=(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/tools/alpha_desk.py').read_text(encoding='utf-8');c.append(ck('launcher does not use shell=True','shell=True' not in alpha));c.append(ck('subject remains Gold-scoped',"not in ('gold','xau','xauusd')" in alpha.lower()))
 c.append(ck('no broker/trade execution controls introduced','place_order' not in rt.lower() and 'broker_order' not in rt.lower()))
 ok=all(x['status']=='PASS' for x in c);out={'record_type':'AD_V31_R05_SECURITY_CERTIFICATION','status':'PASS' if ok else 'FAIL','check_count':len(c),'checks':c};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
