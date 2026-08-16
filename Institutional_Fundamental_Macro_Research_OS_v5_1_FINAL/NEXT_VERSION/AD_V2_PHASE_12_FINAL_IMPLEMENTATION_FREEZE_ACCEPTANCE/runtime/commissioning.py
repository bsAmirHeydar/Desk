from pathlib import Path
import json,hashlib,subprocess,sys,tempfile,os
from .freeze import verify,load,v1_binding
from .final_status import status
from datetime import datetime,timezone
def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def hobj(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
def run(repo,data_root,phase_root,r4_profile='FULL'):
 repo=Path(repo).resolve();v=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL';p=Path(phase_root);checks=[]
 def call(name,cmd):
  q=subprocess.run(cmd,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});checks.append({'name':name,'status':'PASS' if q.returncode==0 else 'FAIL','stdout_tail':q.stdout[-1500:],'stderr_tail':q.stderr[-1000:]});return q.returncode==0
 f=verify(repo,p);checks.append({'name':'FINAL_FREEZE','status':'PASS' if f['status']=='PASS' else 'FAIL'})
 try:
  launcher_binding=v1_binding(repo);checks.append({'name':'V1_LAUNCHER_BINDING','status':'PASS'})
 except Exception as e:
  launcher_binding={'status':'FAIL','error':str(e)};checks.append({'name':'V1_LAUNCHER_BINDING','status':'FAIL','error':str(e)})
 p11=v/'NEXT_VERSION/AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION';p10=v/'NEXT_VERSION/AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC';p09=v/'NEXT_VERSION/AD_V2_PHASE_09_SCIENTIFIC_LEARNING_EVOLUTION_GOVERNANCE';p08=v/'NEXT_VERSION/AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS'
 call('P11_ACCEPTANCE',[sys.executable,str(p11/'tools/run_phase11_acceptance.py'),'--repo-root',str(repo)])
 call('P10_ACCEPTANCE',[sys.executable,str(p10/'tools/run_phase10_acceptance.py'),'--repo-root',str(repo)])
 call('P09_VALIDATOR',[sys.executable,str(p09/'tools/validate_phase09.py'),'--repo-root',str(repo)])
 call('P08_VALIDATOR',[sys.executable,str(p08/'tools/validate_phase08.py'),'--repo-root',str(repo)])
 cert=v/'RUNTIME/R4 Scientific Certification and Reproducibility Hardening/tools/alpha_certify.py';call('R4_'+r4_profile.upper(),[sys.executable,str(cert),'--vault-root',str(v),'certify','--profile',r4_profile.upper()])
 bad=[x for x in checks if x['status']!='PASS'];receipt={'schema_version':'1.0.0','phase':'AD-V2-P12','record_type':'FINAL_IMPLEMENTATION_RECEIPT','status':'PASS' if not bad else 'FAIL_CLOSED','implementation_version':'2.0.0-RC1-SHADOW','generated_at_utc':now(),'checks':checks,'v1_launcher_binding':launcher_binding,'implementation_complete':not bad,'empirical_validation_complete':False,'promotion_granted':False,'v1_authoritative':True,'trade_permission':'V1_INHERITED','broker':'NONE','fixed_roadmap_closed':True,'default_next_phase':None};receipt['receipt_hash']=hobj(receipt)
 out=Path(data_root)/'alpha_desk_v2'/'p12_finalization';out.mkdir(parents=True,exist_ok=True);rp=out/'final_implementation_receipt.json'
 if rp.exists():
  old=json.loads(rp.read_text(encoding='utf-8'))
  if old.get('status')=='PASS' and receipt['status']=='PASS':
   ob=old.get('v1_launcher_binding') or {};cb=receipt.get('v1_launcher_binding') or {}
   if ob.get('canonical_sha256')==cb.get('canonical_sha256') and ob.get('git_blob')==cb.get('git_blob'):return old
   return {'schema_version':'1.0.0','phase':'AD-V2-P12','record_type':'FINAL_IMPLEMENTATION_RECEIPT','status':'FAIL_CLOSED','reason':'V1_LAUNCHER_BINDING_CHANGED_AFTER_FINALIZATION','stored_binding':ob,'current_binding':cb}
 rp.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return receipt
