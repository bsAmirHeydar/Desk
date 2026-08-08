#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);p.add_argument('--mode',choices=['runtime','deployment'],default='runtime');a=p.parse_args();r=Path(a.vault_root);e=[];w=[]
try:m=json.loads((r/'CURRENT_PRODUCTION_MANIFEST.json').read_text(encoding='utf-8'))
except Exception as x:m={};e.append('MANIFEST_PARSE: '+str(x))
if m.get('current_stack') not in {'V18.0.0','V19.0.0'}:e.append('CURRENT_STACK_NOT_V18_OR_V19')
if m.get('fact_constitution_version')!='1.1.0':e.append('FACT_CONSTITUTION_NOT_1_1')
if m.get('decision_authority',{}).get('direction')!='FUNDAMENTAL_ONLY':e.append('DIRECTION_AUTHORITY_DRIFT')
d2=m.get('d2_market_sciences') or {}
if d2.get('authority_mode')!='CANONICAL_SHADOW':e.append('D2_NOT_CANONICAL_SHADOW')
if m.get('current_stack')=='V18.0.0' and d2.get('final_permission_effect')!='NONE':e.append('D2_PREMATURE_PERMISSION_EFFECT')
if m.get('current_stack')=='V19.0.0' and d2.get('direct_permission_effect')!='NONE':e.append('D2_DIRECT_PERMISSION_EFFECT')

if m.get('current_stack')=='V18.0.0' and d2.get('d3_promotion_state')!='NOT_PROMOTED':e.append('D3_PREMATURE_PROMOTION')
if m.get('current_stack')=='V19.0.0' and d2.get('d3_promotion_state')!='PROMOTED_VIA_MODULE_101_ONLY':e.append('D3_PROMOTION_PATH_INVALID')
if m.get('current_stack')=='V18.0.0':
    expected={'positioning_ownership':'SHADOW_STATE_ONLY','actual_flow':'SHADOW_STATE_ONLY','funding_plumbing':'SHADOW_STATE_ONLY','institutional_mechanics':'SHADOW_STATE_ONLY','market_capacity':'SHADOW_STATE_ONLY'}
else:
    expected={'positioning_ownership':'MODULE_101_CONSTRAINED_MODIFIER','actual_flow':'MODULE_101_CONSTRAINED_MODIFIER','funding_plumbing':'MODULE_101_CONSTRAINED_MODIFIER','institutional_mechanics':'MODULE_101_CONSTRAINED_MODIFIER','market_capacity':'MODULE_101_EXECUTION_CAPACITY_GATE'}
for k,v in expected.items():
    if m.get('decision_authority',{}).get(k)!=v:e.append('D2_DECISION_AUTHORITY_DRIFT_'+k)
for req in m.get('required_runtime_contracts',[]):
    if not (r/req).exists():e.append('MISSING_RUNTIME_CONTRACT_'+req)
cmds=[
 ('manifest_sync',[r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/tools/alphalab_manifest_sync.py','--vault-root',r,'--check']),
 ('d2_coverage',[r/'100 Six-Market D2 Fact Books and Production Shadow Engine/tools/alphalab_d2_coverage_audit.py','--vault-root',r]),
 ('d2_sources',[r/'100 Six-Market D2 Fact Books and Production Shadow Engine/tools/alphalab_d2_source_audit.py','--vault-root',r]),
 ('d1_regression_preflight',[r/'95 Fact Constitution and Institutional Evidence Fabric/tools/alphalab_d1_preflight.py','--vault-root',r,'--mode',a.mode]),
 ('v16_1_regression_preflight',[r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/tools/alphalab_preflight.py','--vault-root',r,'--mode',a.mode])]
checks=[]
for name,args in cmds:
    q=subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True);checks.append({'name':name,'pass':q.returncode==0})
    if q.returncode:e.append(name+'_FAIL: '+(q.stdout+q.stderr)[-1200:])
print(json.dumps({'status':'PASS' if not e else 'FAIL','mode':a.mode,'checks':checks,'errors':e,'warnings':w},indent=2));sys.exit(0 if not e else 2)
