#!/usr/bin/env python3
from pathlib import Path
import argparse,json,datetime,sys
p=argparse.ArgumentParser(); p.add_argument('--facts',required=True); p.add_argument('--cutoff',required=True); p.add_argument('--output',required=True); a=p.parse_args()
cut=datetime.datetime.fromisoformat(a.cutoff.replace('Z','+00:00'))
facts=[]
for line in Path(a.facts).read_text(encoding='utf-8').splitlines():
    if line.strip(): facts.append(json.loads(line))
elig=[]; excluded=[]
for f in facts:
    pub=(f.get('time') or {}).get('publication_time')
    if not pub:
        excluded.append({'fact_id':f.get('fact_id'),'reason':'UNRESOLVED_PUBLICATION_TIME'}); continue
    try: pt=datetime.datetime.fromisoformat(pub.replace('Z','+00:00'))
    except Exception:
        excluded.append({'fact_id':f.get('fact_id'),'reason':'INVALID_PUBLICATION_TIME'}); continue
    if pt<=cut: elig.append((pt,f))
    else: excluded.append({'fact_id':f.get('fact_id'),'reason':'FUTURE_VINTAGE'})
# latest eligible per release family; ungrouped facts remain individually eligible
selected=[]; fam={}; singles=[]
for pt,f in elig:
    k=f.get('release_family_id')
    if k:
        cur=fam.get(k)
        if cur is None or pt>cur[0] or (pt==cur[0] and (f.get('release_sequence') or 0)>(cur[1].get('release_sequence') or 0)): fam[k]=(pt,f)
    else: singles.append(f)
selected=singles+[x[1] for x in fam.values()]
selected.sort(key=lambda x:x.get('fact_id',''))
out={'cutoff':a.cutoff,'selected':selected,'excluded':excluded,'future_vintages_excluded':True}
Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'status':'PASS','selected':len(selected),'excluded':len(excluded)},indent=2)); sys.exit(0)
