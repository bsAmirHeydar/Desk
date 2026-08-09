#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,subprocess,tempfile
import jsonschema
p=argparse.ArgumentParser();p.add_argument('--pack',required=True);p.add_argument('--vault-root');a=p.parse_args();x=json.loads(Path(a.pack).read_text(encoding='utf-8'));e=[]
mod=Path(__file__).resolve().parent.parent; schema_path=mod/'schemas/AlphaLab_D2_Shadow_Pack.schema.json'
try:
    sch=json.loads(schema_path.read_text(encoding='utf-8')); jsonschema.validators.validator_for(sch).check_schema(sch)
    resolver=jsonschema.RefResolver(base_uri=(mod/'schemas').resolve().as_uri()+'/',referrer=sch)
    jsonschema.validate(x,sch,resolver=resolver)
except Exception as exc:e.append('SCHEMA:'+str(exc))
for k in ['version','authority_mode','instrument','analysis_cutoff_utc','positioning','actual_flow','funding_plumbing','institutional_mechanics','market_capacity','cross_science_independent_roots','d2_permission_effect','d3_promotion_state']:
    if k not in x:e.append('MISSING_'+k)
if x.get('version') not in {'1.0.0','1.1.0'}:e.append('VERSION')
if x.get('authority_mode')!='CANONICAL_SHADOW':e.append('AUTHORITY_NOT_SHADOW')
if x.get('d2_permission_effect')!='NONE':e.append('PREMATURE_D2_PERMISSION')
if x.get('d3_promotion_state') not in {'NOT_PROMOTED','PROMOTED_VIA_MODULE_101_ONLY'}:e.append('BAD_D3_PROMOTION_STATE')
if x.get('version')=='1.1.0' and 'observability_receipt' not in x:e.append('MISSING_OBSERVABILITY_RECEIPT')
if x.get('version')=='1.1.0' and a.vault_root and 'observability_receipt' in x:
    with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False,encoding='utf-8') as f:
        json.dump(x['observability_receipt'],f); fn=f.name
    q=subprocess.run([sys.executable,str(Path(a.vault_root)/'100 Six-Market D2 Fact Books and Production Shadow Engine/tools/alphalab_observability_validate.py'),'--vault-root',a.vault_root,'--receipt',fn],capture_output=True,text=True)
    if q.returncode:e.append('OBSERVABILITY_RECEIPT_INVALID:'+q.stdout+q.stderr)
print(json.dumps({'status':'PASS' if not e else 'FAIL','errors':e},indent=2));sys.exit(0 if not e else 2)
