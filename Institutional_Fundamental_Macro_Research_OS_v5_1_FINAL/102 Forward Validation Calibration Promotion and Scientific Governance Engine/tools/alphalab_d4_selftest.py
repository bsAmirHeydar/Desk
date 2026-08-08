#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,tempfile,sys,hashlib
R=Path(__file__).resolve().parents[2];M=R/'102 Forward Validation Calibration Promotion and Scientific Governance Engine';checks=[]
def ck(n,c,d=None):checks.append({'name':n,'pass':bool(c),'detail':d})
m=json.loads((R/'CURRENT_PRODUCTION_MANIFEST.json').read_text())
ck('stack_v20',m.get('current_stack')=='V20.0.0',m.get('current_stack'))
ck('direction_fundamental_only',m.get('decision_authority',{}).get('direction')=='FUNDAMENTAL_ONLY')
d4=m.get('d4_forward_validation') or {}
ck('d4_governance_enforced',d4.get('authority_mode')=='GOVERNANCE_ENFORCED')
ck('direction_flip_forbidden',d4.get('direction_flip_allowed') is False)
ck('positive_permission_registry_only',d4.get('positive_permission_creation')=='PROMOTED_REGISTRY_ONLY')
reg=json.loads((M/'config/promotion_registry.json').read_text())
ck('initial_registry_empty',reg.get('records')==[])
ck('runtime_registry_mutation_forbidden',json.loads((M/'config/d4_governance_policy.json').read_text()).get('runtime_registry_mutation_allowed') is False)
# registry validator
q=subprocess.run([sys.executable,str(M/'tools/alphalab_d4_registry_validate.py'),'--registry',str(M/'config/promotion_registry.json')],capture_output=True,text=True);ck('registry_validate',q.returncode==0,q.stdout[-500:])
# authority gate preserves V19 with empty registry
with tempfile.TemporaryDirectory() as td:
    ip=Path(td)/'i.json';ip.write_text(json.dumps({'instrument':'NASDAQ100','fundamental_direction':'BULLISH','v19_d3_permission':'NO_TRADE','promotion_candidates':[{'modifier_id':'FLOW_SUPPORT_X','proposed_permission':'BUY'}]}))
    q=subprocess.run([sys.executable,str(M/'tools/alphalab_d4_authority_gate.py'),'--input',str(ip),'--registry',str(M/'config/promotion_registry.json')],capture_output=True,text=True)
    try:o=json.loads(q.stdout);ok=o.get('final_v20_permission')=='NO_TRADE' and o.get('applied_promotion_ids')==[] and o.get('shadow_candidate_ids')==['FLOW_SUPPORT_X']
    except:ok=False
    ck('empty_registry_preserves_v19',q.returncode==0 and ok,q.stdout[-500:])
# hash-chain ledger round trip
with tempfile.TemporaryDirectory() as td:
    led=Path(td)/'l.jsonl'
    for i in range(2):
        rec=Path(td)/f'r{i}.json';rec.write_text(json.dumps({'record_type':'FORWARD_OBSERVATION','record_id':f'R{i}','x':i}))
        q=subprocess.run([sys.executable,str(M/'tools/alphalab_d4_append_ledger.py'),'--ledger',str(led),'--record',str(rec)],capture_output=True,text=True)
        ck('ledger_append_'+str(i),q.returncode==0,q.stdout[-300:])
    q=subprocess.run([sys.executable,str(M/'tools/alphalab_d4_validate_ledger.py'),'--ledger',str(led)],capture_output=True,text=True);ck('ledger_validate',q.returncode==0,q.stdout[-500:])
# key contracts exist
for rel in ['schemas/AlphaLab_D4_Forward_Observation.schema.json','schemas/AlphaLab_D4_Counterfactual.schema.json','schemas/AlphaLab_D4_Promotion_Record.schema.json','schemas/AlphaLab_V20_StateBundle.schema.json','31 V20 D4 Full-Vault Production Prompt.md']:
    ck('exists_'+rel,(M/rel).exists())
err=[x for x in checks if not x['pass']]
print(json.dumps({'status':'PASS' if not err else 'FAIL','tests':len(checks),'passed':len(checks)-len(err),'checks':checks},indent=2));sys.exit(0 if not err else 2)
