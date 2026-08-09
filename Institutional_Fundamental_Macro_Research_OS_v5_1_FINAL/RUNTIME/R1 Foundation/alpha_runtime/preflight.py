from pathlib import Path
import json
from .selftest import run as selftest

def _syntax_check(path):
    src=path.read_text(encoding='utf-8-sig')
    compile(src,str(path),'exec',dont_inherit=True,optimize=0)

def run(vault_root):
    v=Path(vault_root); r=v/'RUNTIME'/'R1 Foundation'; errors=[]; checks=[]
    required=['00 R1 Foundation MOC.md','config/runtime_policy.json','config/storage_policy.json','config/temporal_policy.json','config/lifecycle_policy.json','sql/catalog_schema.sql','tools/alpha_runtime.py']
    for x in required:
        ok=(r/x).exists(); checks.append({"name":"exists:"+x,"pass":ok});
        if not ok: errors.append('missing '+x)
    schemas=list((r/'schemas').glob('*.schema.json')); checks.append({"name":"schema_count","pass":len(schemas)>=15,"count":len(schemas)})
    for p in schemas:
        try: json.loads(p.read_text(encoding='utf-8'))
        except Exception as e: errors.append(f'invalid schema json {p.name}: {e}')
    pyfiles=list((r/'alpha_runtime').glob('*.py'))+[r/'tools'/'alpha_runtime.py']
    for p in pyfiles:
        try: _syntax_check(p)
        except Exception as e: errors.append(f'compile fail {p.name}: {e}')
    checks.append({"name":"runtime_python_syntax","pass":not any(x.startswith('compile fail ') for x in errors),"count":len(pyfiles)})
    st=selftest(v); checks.append({"name":"r1_selftest","pass":st['status']=='PASS','detail':st})
    if st['status']!='PASS': errors.append('R1 selftest failed')
    return {"status":"PASS" if not errors else "FAIL","runtime":"R1.0.0","scientific_stack":"V21.3.0","checks":checks,"errors":errors}
