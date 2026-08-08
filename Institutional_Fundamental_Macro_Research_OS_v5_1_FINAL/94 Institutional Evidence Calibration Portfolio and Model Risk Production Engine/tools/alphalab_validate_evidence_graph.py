#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('graph'); a=p.parse_args(); g=json.loads(Path(a.graph).read_text(encoding='utf-8'))
ids=[n.get('evidence_id') for n in g.get('nodes',[])]; S=set(ids); errors=[]
if len(ids)!=len(S): errors.append('duplicate evidence_id')
adj={i:[] for i in S}
for e in g.get('edges',[]):
    if e.get('from') not in S or e.get('to') not in S: errors.append(f'unknown node in edge {e}')
    else: adj[e['from']].append(e['to'])
seen=set(); stack=set()
def dfs(x):
    if x in stack: return True
    if x in seen: return False
    seen.add(x); stack.add(x)
    cyc=any(dfs(y) for y in adj.get(x,[])); stack.remove(x); return cyc
if any(dfs(x) for x in list(S)): errors.append('cycle detected')
roots={n.get('evidence_id'):n.get('root_cause_id') for n in g.get('nodes',[])}
for e in g.get('edges',[]):
    if e.get('relation')=='INDEPENDENT_EVIDENCE' and roots.get(e.get('from'))==roots.get(e.get('to')):
        errors.append(f'same-root edge incorrectly marked independent: {e}')
print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors},indent=2)); sys.exit(0 if not errors else 2)
