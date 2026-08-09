#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,tempfile,sys,csv
try: import jsonschema
except Exception: jsonschema=None
R=Path(__file__).resolve().parents[2];M=R/'102 Forward Validation Calibration Promotion and Scientific Governance Engine';checks=[]
def ck(n,c,d=None):checks.append({'name':n,'pass':bool(c),'detail':d})
m=json.loads((R/'CURRENT_PRODUCTION_MANIFEST.json').read_text());ck('stack_v20_or_v21',m.get('current_stack') in {'V20.0.0','V21.0.0','V21.1.0','V21.2.0','V21.3.0'},m.get('current_stack'));ck('direction_fundamental_only',m.get('decision_authority',{}).get('direction')=='FUNDAMENTAL_ONLY')
reg=json.loads((M/'config/promotion_registry.json').read_text());ck('registry_exists',isinstance(reg.get('records'),list))
with tempfile.TemporaryDirectory() as td0:
 td=Path(td0)
 # Empty registry preserves base permission and shadows candidate.
 ip=td/'i.json';ip.write_text(json.dumps({'instrument':'NASDAQ100','analysis_cutoff_utc':'2026-08-08T00:00:00Z','fundamental_direction':'BULLISH','v19_d3_permission':'NO_TRADE','active_strategy_horizon':'SESSION_1_6H','promotion_candidates':[{'modifier_id':'FLOW_SUPPORT_X','proposed_permission':'BUY'}]}))
 q=subprocess.run([sys.executable,str(M/'tools/alphalab_d4_authority_gate.py'),'--input',str(ip),'--registry',str(M/'config/promotion_registry.json')],capture_output=True,text=True)
 try:o=json.loads(q.stdout);ok=o.get('final_permission')=='NO_TRADE' and 'FLOW_SUPPORT_X' in o.get('shadow_candidate_ids',[])
 except:ok=False
 ck('empty_registry_preserves_base',q.returncode==0 and ok,q.stdout[-500:])
 # Cluster bootstrap uses root when roots exist.
 cp=td/'c.csv';rows=[]
 for split in ['DEVELOPMENT','HOLDOUT']:
  for r in range(4):
   for k in range(2):rows.append({'modifier_id':'M1','sample_split':split,'delta_r':str(.2+r*.01),'actual_r':'.3','counterfactual_r':'.1','independent_root_id':f'{split}_R{r}','trading_day':f'2026-08-{r+1:02d}','run_id':f'{split}_{r}_{k}','regime':'RISK_ON','outcome_status':'REALIZED','hypothesis_family_id':'HF1','hypotheses_tested_in_family':'2','chronological_split_attested':'true','execution_profile':'E1'})
 with cp.open('w',newline='',encoding='utf-8') as fh:
  wr=csv.DictWriter(fh,fieldnames=rows[0]);wr.writeheader();wr.writerows(rows)
 op=td/'cal.json';q=subprocess.run([sys.executable,str(M/'tools/alphalab_d4_calibrate.py'),'--input',str(cp),'--modifier-id','M1','--output',str(op)],capture_output=True,text=True);z=json.loads(op.read_text());ck('cluster_bootstrap_root',q.returncode==0 and z['development']['resampling_unit']=='independent_root_id' and z['development']['resampling_cluster_n']==4,z);ck('calibration_required_fields',all(k in z for k in ['calibration_id','policy_version','promotion_eligibility','created_at_utc']),z)
 if jsonschema:
  try:
   sch=json.loads((M/'schemas/AlphaLab_D4_Calibration_Report.schema.json').read_text());jsonschema.validate(z,sch);ok_schema=True
  except Exception as ex:ok_schema=False;schema_detail=str(ex)
  ck('calibration_output_matches_schema',ok_schema,None if ok_schema else schema_detail)

 # Runtime authority effects and precedence.
 regp=td/'registry.json'
 reg={'version':'TEST','records':[
  {'promotion_id':'P_CAP','modifier_id':'CAP1','status':'ACTIVE','authority_class':'CONFIDENCE_CAP','activated_at_utc':'2026-01-01T00:00:00Z','scope':{'instruments':['NASDAQ100'],'horizons':['SESSION_1_6H']},'effect_parameters':{'cap_label':'CROWDING_VALIDATED_CAP'}},
  {'promotion_id':'P_VAL','modifier_id':'VAL1','status':'ACTIVE','authority_class':'VALIDITY_SHORTEN','activated_at_utc':'2026-01-01T00:00:00Z','scope':{'instruments':['NASDAQ100']},'effect_parameters':{'validity_action':'SHORTEN_TO_NEXT_CAUSAL_REVIEW'}},
  {'promotion_id':'P_STOP','modifier_id':'STOP1','status':'ACTIVE','authority_class':'SUPPRESS_PERMISSION','activated_at_utc':'2026-01-01T00:00:00Z','scope':{'instruments':['NASDAQ100']}},
  {'promotion_id':'P_CREATE','modifier_id':'CREATE1','status':'ACTIVE','authority_class':'CREATE_PERMISSION_WITH_EXISTING_FUNDAMENTAL_DIRECTION','activated_at_utc':'2026-01-01T00:00:00Z','scope':{'instruments':['NASDAQ100']}}
 ]};regp.write_text(json.dumps(reg))
 aip=td/'authority_input.json'
 aip.write_text(json.dumps({'instrument':'NASDAQ100','analysis_cutoff_utc':'2026-08-08T12:00:00Z','active_strategy_horizon':'SESSION_1_6H','fundamental_direction':'BULLISH','v19_d3_permission':'BUY','promotion_candidates':[{'modifier_id':'CAP1'},{'modifier_id':'VAL1'}]}))
 q=subprocess.run([sys.executable,str(M/'tools/alphalab_d4_authority_gate.py'),'--input',str(aip),'--registry',str(regp)],capture_output=True,text=True);z=json.loads(q.stdout);ck('authority_cap_and_validity_effects',q.returncode==0 and 'CROWDING_VALIDATED_CAP' in z.get('confidence_caps',[]) and z.get('validity_action')=='SHORTEN_TO_NEXT_CAUSAL_REVIEW',z)
 aip.write_text(json.dumps({'instrument':'NASDAQ100','analysis_cutoff_utc':'2026-08-08T12:00:00Z','active_strategy_horizon':'SESSION_1_6H','fundamental_direction':'BULLISH','v19_d3_permission':'NO_TRADE','promotion_candidates':[{'modifier_id':'CREATE1','proposed_permission':'BUY'}]}))
 q=subprocess.run([sys.executable,str(M/'tools/alphalab_d4_authority_gate.py'),'--input',str(aip),'--registry',str(regp)],capture_output=True,text=True);z=json.loads(q.stdout);ck('validated_positive_authority_respects_fundamental_direction',q.returncode==0 and z.get('final_permission')=='BUY' and 'P_CREATE' in z.get('applied_promotion_ids',[]),z)
 aip.write_text(json.dumps({'instrument':'NASDAQ100','analysis_cutoff_utc':'2026-08-08T12:00:00Z','active_strategy_horizon':'SESSION_1_6H','fundamental_direction':'BULLISH','v19_d3_permission':'NO_TRADE','promotion_candidates':[{'modifier_id':'STOP1','proposed_permission':'NO_TRADE'},{'modifier_id':'CREATE1','proposed_permission':'BUY'}]}))
 q=subprocess.run([sys.executable,str(M/'tools/alphalab_d4_authority_gate.py'),'--input',str(aip),'--registry',str(regp)],capture_output=True,text=True);z=json.loads(q.stdout);ck('risk_constraint_precedes_positive_authority',q.returncode==0 and z.get('final_permission')=='NO_TRADE' and 'P_STOP' in z.get('applied_promotion_ids',[]) and 'P_CREATE' not in z.get('applied_promotion_ids',[]),z)

err=[x for x in checks if not x['pass']];print(json.dumps({'status':'PASS' if not err else 'FAIL','tests':len(checks),'passed':len(checks)-len(err),'checks':checks},indent=2));sys.exit(0 if not err else 2)
