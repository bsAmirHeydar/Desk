#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);p.add_argument('--mode',choices=['runtime','deployment'],default='runtime');a=p.parse_args();r=Path(a.vault_root);e=[];checks=[]
try:m=json.loads((r/'CURRENT_PRODUCTION_MANIFEST.json').read_text())
except Exception as x:m={};e.append('MANIFEST_PARSE '+str(x))
if m.get('current_stack') not in {'V20.0.0','V21.0.0','V21.1.0','V21.2.0','V21.3.0'}:e.append('CURRENT_STACK_NOT_V20_OR_V21')
if m.get('fact_constitution_version')!='1.1.0':e.append('FACT_CONSTITUTION_DRIFT')
if m.get('decision_authority',{}).get('direction')!='FUNDAMENTAL_ONLY':e.append('DIRECTION_AUTHORITY_DRIFT')
d4=m.get('d4_forward_validation') or {}
if d4.get('authority_mode')!='GOVERNANCE_ENFORCED':e.append('D4_GOVERNANCE_NOT_ENFORCED')
if d4.get('direction_flip_allowed') is not False:e.append('D4_DIRECTION_FLIP_GUARD_DRIFT')
if d4.get('positive_permission_creation')!='PROMOTED_REGISTRY_ONLY':e.append('D4_POSITIVE_AUTHORITY_DRIFT')
if (m.get('d3_unified_edge') or {}).get('authority_mode')!='ENFORCED_CAUSAL_MODULATION':e.append('D3_AUTHORITY_DRIFT')
for req in m.get('required_runtime_contracts',[]):
    if not (r/req).exists():e.append('MISSING_RUNTIME_CONTRACT '+req)
cmds=[
 ('manifest_sync',[r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/tools/alphalab_manifest_sync.py','--vault-root',r,'--check']),
 ('d4_selftest',[r/'102 Forward Validation Calibration Promotion and Scientific Governance Engine/tools/alphalab_d4_selftest.py']),
 ('d4_coverage',[r/'102 Forward Validation Calibration Promotion and Scientific Governance Engine/tools/alphalab_d4_coverage_audit.py','--vault-root',r]),
 ('d3_regression',[r/'101 Unified Causal Fuzzy Edge Integration and Permission Adjudication Engine/tools/alphalab_d3_preflight.py','--vault-root',r,'--mode',a.mode]),
 ('d2_regression',[r/'100 Six-Market D2 Fact Books and Production Shadow Engine/tools/alphalab_d2_preflight.py','--vault-root',r,'--mode',a.mode]),
 ('d1_regression',[r/'95 Fact Constitution and Institutional Evidence Fabric/tools/alphalab_d1_preflight.py','--vault-root',r,'--mode',a.mode]),
 ('v16_regression',[r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/tools/alphalab_preflight.py','--vault-root',r,'--mode',a.mode])]
for name,args in cmds:
    q=subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True);checks.append({'name':name,'pass':q.returncode==0})
    if q.returncode:e.append(name+'_FAIL '+(q.stdout+q.stderr)[-1800:])
print(json.dumps({'status':'PASS' if not e else 'FAIL','mode':a.mode,'checks':checks,'errors':e},indent=2));sys.exit(0 if not e else 2)
