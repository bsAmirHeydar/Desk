#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,json,sys,tempfile
BASE=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BASE.parent))
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.run_overlay import compose,IntegrationError
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.change_detector import detect
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.v2_memory import build_extension,persist,verify,status
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.report_model_v2 import build as build_report
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.render_v2 import render_html

def load(n): return json.loads((BASE/'tests/fixtures'/n).read_text(encoding='utf-8'))
def main():
 checks=[]
 def ck(name,ok,detail=None): checks.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
 b=load('base_capsule_current.json'); p=load('p02_pressure_current.json'); t=load('p03_transmission_current.json'); l=load('p04_latent_current.json'); g=load('p05_gold_current.json')
 try: s=compose(b,p,t,l,g); ck('compose_valid_stack',s.get('status')=='PASS')
 except Exception as e: ck('compose_valid_stack',False,str(e)); s=None
 if s:
  ck('permission_inherited',s['execution']['permission']==b['permission'] and s['execution']['v2_override_allowed'] is False)
  ck('broker_none',s['execution']['broker_authority']=='NONE')
  ck('pressure_owner',s['authority']['pressure']=='AD-V2-P02')
  ck('transmission_owner',s['authority']['transmission']=='AD-V2-P03')
  ck('latent_owner',s['authority']['latent_release']=='AD-V2-P04')
  ck('gold_owner',s['authority']['gold_specialization']=='AD-V2-P05')
  ck('portable_non_authoritative',s['portable_memory'].get('authoritative') is False)
  ck('pressure_price_separation',s['integrity'].get('pressure_price_separation_preserved') is True)
  r=build_report(s,None); ck('report_pressure_separated',r['ux']['pressure_price_separated'] is True); ck('report_readiness_not_permission',r['ux']['release_readiness_is_permission'] is False)
  with tempfile.TemporaryDirectory() as td:
   hp=render_html(r,Path(td)/'x.html'); txt=Path(hp).read_text(encoding='utf-8'); ck('html_rendered',Path(hp).is_file()); ck('html_contains_pressure', 'Directional Pressure' in txt); ck('html_contains_transmission','Price Transmission' in txt); ck('html_contains_permission','Release Readiness' in txt and 'Permission' in txt)
  # semantic delta and price-only protection: alter no pressure field, only transmission response-window extra non-registry value
  prev=copy.deepcopy(s); curr=copy.deepcopy(s); curr['science_v2']['transmission']['actual_target_response']={'price_return':999}; d=detect(prev,curr); ck('price_only_not_pressure_change',d['pressure_changed'] is False)
  # explicit pressure change is detected
  curr2=copy.deepcopy(s); curr2['science_v2']['pressure']['pressure_core']['class']='BUY_VERY_HIGH'; d2=detect(prev,curr2); ck('pressure_change_detected',d2['pressure_changed'] is True and any(x['field']=='pressure_class' for x in d2['items']))
  # persistence
  with tempfile.TemporaryDirectory() as td:
   ext=build_extension(s); rec=persist(td,ext); ck('persist_pass',rec['status']=='PASS'); ck('verify_persisted',verify(rec['path'])['status']=='PASS'); ck('status_pass',status(td)['status']=='PASS');
   try: persist(td,ext); ck('immutable_collision_blocked',False)
   except Exception: ck('immutable_collision_blocked',True)
   # tamper
   pp=Path(rec['path']); o=json.loads(pp.read_text()); o['quality_status']='TAMPER'; pp.write_text(json.dumps(o),encoding='utf-8'); ck('tamper_detected',verify(pp)['status']=='FAIL')
  bad=copy.deepcopy(t); bad['upstream_pressure_reference']['fingerprint']='bad'
  try: compose(b,p,bad,l,g); ck('p03_p02_mismatch_blocked',False)
  except Exception: ck('p03_p02_mismatch_blocked',True)
  bad=copy.deepcopy(l); bad['upstream_transmission_reference']['fingerprint']='bad'
  try: compose(b,p,t,bad,g); ck('p04_p03_mismatch_blocked',False)
  except Exception: ck('p04_p03_mismatch_blocked',True)
  bad=copy.deepcopy(g); bad['upstream_references']['pressure_fingerprint']='bad'
  try: compose(b,p,t,l,bad); ck('p05_upstream_mismatch_blocked',False)
  except Exception: ck('p05_upstream_mismatch_blocked',True)
  bad=copy.deepcopy(b); bad['subject']='NASDAQ100'
  try: compose(bad,p,t,l,g); ck('non_gold_blocked',False)
  except Exception: ck('non_gold_blocked',True)
  bad=copy.deepcopy(b); bad['horizon']='MULTI_DAY_2_10D'
  try: compose(bad,p,t,l,g); ck('horizon_mismatch_blocked',False)
  except Exception: ck('horizon_mismatch_blocked',True)
  bad=copy.deepcopy(l); bad['release_readiness']['trade_permission_granted']=True
  try: compose(b,p,t,bad,g); ck('latent_permission_grant_blocked',False)
  except Exception: ck('latent_permission_grant_blocked',True)
  bad=copy.deepcopy(g); bad['integrity']['trade_permission_granted']=True
  try: compose(b,p,t,l,bad); ck('gold_permission_grant_blocked',False)
  except Exception: ck('gold_permission_grant_blocked',True)
  # secret scan
  with tempfile.TemporaryDirectory() as td:
   ext=build_extension(s); ext['API_KEY']='x'
   try: persist(td,ext); ck('secret_persistence_blocked',False)
   except Exception: ck('secret_persistence_blocked',True)
 # static files/config/schema checks
 for rel in ['config/run_integration_policy.json','config/change_detection_registry.json','config/persistence_policy.json','config/ux_pressure_price_policy.json','config/artifact_name_registry.json','config/history_policy.json','schemas/AlphaDesk_V2_GoldRunState.schema.json','schemas/AlphaDesk_V2_RunCapsuleExtension.schema.json','schemas/AlphaDesk_V2_ChangeSet.schema.json','schemas/AlphaDesk_V2_ReportModel.schema.json']:
  try: json.loads((BASE/rel).read_text(encoding='utf-8')); ck('json:'+rel,True)
  except Exception as e: ck('json:'+rel,False,str(e))
 # hard invariants in policy
 pol=json.loads((BASE/'config/run_integration_policy.json').read_text()); inv=set(pol['hard_invariants'])
 for x in ['NO_UPSTREAM_MUTATION','NO_PERMISSION_OVERRIDE','NO_DECISION_WORLD_WRITE','NO_V1_CAPSULE_REWRITE','PRICE_ONLY_CHANGE_NOT_PRESSURE_CHANGE','RELEASE_READINESS_NOT_PERMISSION']:
  ck('invariant:'+x,x in inv)
 failed=[x for x in checks if x['status']!='PASS']; out={'schema_version':'1.0.0','phase':'AD-V2-P06','status':'PASS' if not failed else 'FAIL','passed':len(checks)-len(failed),'failed':len(failed),'checks':checks}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if not failed else 2
if __name__=='__main__': raise SystemExit(main())
