#!/usr/bin/env python3
import argparse,json,re,sys
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--vault-root',required=True); p.add_argument('--symbol',required=True); p.add_argument('--extra-path',action='append',default=[]); p.add_argument('--material-topic',action='append',default=[]); p.add_argument('--history-mode',action='store_true'); p.add_argument('--output',required=True); a=p.parse_args(); r=Path(a.vault_root)
m=json.loads((r/'CURRENT_PRODUCTION_MANIFEST.json').read_text(encoding='utf-8')); pol=json.loads((r/m['retrieval_policy']).read_text(encoding='utf-8'))
if a.symbol not in m['production_universe']: print('invalid symbol'); sys.exit(2)
sel=[m['production_entrypoint'],*m['canonical_authorities'].values(),*m['allowed_live_subengines']]
sel += m.get('asset_books',{}).get(a.symbol,[])
sel += a.extra_path
# preserve order unique
outsel=[]
for x in sel:
    if x not in outsel: outsel.append(x)
rejected=[]; errors=[]
def status(path):
    t=path.read_text(encoding='utf-8',errors='ignore')[:2500]
    m1=re.search(r'(?m)^status:\s*["\']?([^"\'\n]+)',t)
    return m1.group(1).strip() if m1 else None
for x in list(outsel):
    q=r/x
    if not q.exists(): errors.append('missing '+x); continue
    if q.suffix.lower()=='.md':
        st=status(q)
        if st in pol['forbidden_load_bearing_statuses'] and not a.history_mode:
            rejected.append({'path':x,'status':st}); errors.append('forbidden production retrieval '+x)
dims=list(pol['mandatory_dimensions'])
plan={'symbol':a.symbol,'selected_paths':outsel,'dimensions_covered':dims,'history_mode':bool(a.history_mode),'material_topics':a.material_topic,'rejected_paths':rejected}
Path(a.output).write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors,'selected':len(outsel),'rejected':rejected},indent=2)); sys.exit(0 if not errors else 2)
