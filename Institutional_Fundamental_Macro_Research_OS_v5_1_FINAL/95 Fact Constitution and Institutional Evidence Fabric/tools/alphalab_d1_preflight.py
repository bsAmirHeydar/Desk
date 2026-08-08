#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess,sys
p=argparse.ArgumentParser(); p.add_argument('--vault-root',required=True); p.add_argument('--mode',choices=['runtime','deployment'],default='runtime'); a=p.parse_args(); r=Path(a.vault_root); errors=[]; warnings=[]
try: m=json.loads((r/'CURRENT_PRODUCTION_MANIFEST.json').read_text(encoding='utf-8'))
except Exception as e: m={}; errors.append('MANIFEST_PARSE: '+str(e))
if m.get('current_stack') not in {'V17.0.0','V18.0.0','V19.0.0'}: errors.append('CURRENT_STACK_NOT_V17_V18_OR_V19')
expected_fc={'V17.0.0':'1.0.0','V18.0.0':'1.1.0','V19.0.0':'1.1.0'}.get(m.get('current_stack'))
if expected_fc and m.get('fact_constitution_version')!=expected_fc: errors.append('FACT_CONSTITUTION_VERSION_MISMATCH')
if m.get('decision_authority',{}).get('direction')!='FUNDAMENTAL_ONLY': errors.append('DIRECTION_AUTHORITY_DRIFT')
if m.get('canonical_authorities',{}).get('fact_constitution')!='95 Fact Constitution and Institutional Evidence Fabric/00 Fact Constitution and Institutional Evidence Fabric MOC.md': errors.append('FACT_AUTHORITY_MISSING')
for req in m.get('required_runtime_contracts',[]):
    if not (r/req).exists(): errors.append('MISSING_RUNTIME_CONTRACT: '+req)
# verify mirror through existing authority
sync=r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/tools/alphalab_manifest_sync.py'
if sync.exists():
    q=subprocess.run([sys.executable,str(sync),'--vault-root',str(r),'--check'],capture_output=True,text=True)
    if q.returncode: errors.append('MANIFEST_MIRROR_DRIFT: '+q.stdout[-500:])
else: errors.append('MISSING_MANIFEST_SYNC_TOOL')
# coverage contract
cov=Path(__file__).resolve().parent/'alphalab_fact_coverage_audit.py'
q=subprocess.run([sys.executable,str(cov),'--vault-root',str(r)],capture_output=True,text=True)
if q.returncode: errors.append('FACT_COVERAGE_AUDIT_FAIL: '+q.stdout[-500:])
# existing V16.1 production preflight must still pass as delegated stack
old=r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/tools/alphalab_preflight.py'
if old.exists():
    q=subprocess.run([sys.executable,str(old),'--vault-root',str(r),'--mode',a.mode],capture_output=True,text=True)
    if q.returncode: errors.append('V16_1_REGRESSION_PREFLIGHT_FAIL: '+q.stdout[-900:])
else: errors.append('MISSING_V16_1_PREFLIGHT')
print(json.dumps({'status':'PASS' if not errors else 'FAIL','mode':a.mode,'errors':errors,'warnings':warnings},indent=2)); sys.exit(0 if not errors else 2)
