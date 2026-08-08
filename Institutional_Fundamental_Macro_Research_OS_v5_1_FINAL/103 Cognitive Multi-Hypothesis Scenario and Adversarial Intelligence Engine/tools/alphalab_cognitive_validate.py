#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,subprocess
try: import jsonschema
except Exception: jsonschema=None
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--schema',default=None);p.add_argument('--vault-root');a=p.parse_args();mod=Path(__file__).resolve().parent.parent;schema=Path(a.schema) if a.schema else mod/'schemas/AlphaLab_Cognitive_Input.schema.json'
try:data=json.loads(Path(a.input).read_text(encoding='utf-8'));sch=json.loads(schema.read_text(encoding='utf-8'))
except Exception as e:print(json.dumps({'status':'FAIL','errors':[str(e)]},indent=2));sys.exit(2)
errors=[]
if jsonschema:
 try:
  jsonschema.validators.validator_for(sch).check_schema(sch);resolver=jsonschema.RefResolver(base_uri=(mod/'schemas').resolve().as_uri()+'/',referrer=sch);jsonschema.validate(data,sch,resolver=resolver)
 except Exception as e:errors.append('SCHEMA: '+str(e))
root=Path(a.vault_root).resolve() if a.vault_root else mod.parent
q=subprocess.run([sys.executable,str(mod/'tools/alphalab_semantic_integrity.py'),'--input',a.input,'--vault-root',str(root)],capture_output=True,text=True)
if q.returncode:
 try:errors.extend(['SEMANTIC: '+x for x in json.loads(q.stdout).get('errors',[])])
 except:errors.append('SEMANTIC: '+(q.stdout+q.stderr)[-2000:])
print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors},indent=2,ensure_ascii=False));sys.exit(0 if not errors else 2)
