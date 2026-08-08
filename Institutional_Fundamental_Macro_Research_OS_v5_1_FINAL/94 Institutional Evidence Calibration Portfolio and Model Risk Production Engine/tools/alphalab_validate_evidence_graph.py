#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('graph'); p.add_argument('--output'); a=p.parse_args(); g=json.loads(Path(a.graph).read_text(encoding='utf-8'))
ids=[n.get('evidence_id') for n in g.get('nodes',[])]; S=set(ids); hard=[]; issues=[]
if len(ids)!=len(S): hard.append('duplicate evidence_id')
adj={i:[] for i in S}
for e in g.get('edges',[]):
    if e.get('from') not in S or e.get('to') not in S: hard.append(f'unknown node in edge {e}')
    else: adj[e['from']].append(e['to'])
seen=set(); stack=set()
def dfs(x):
    if x in stack: return True
    if x in seen: return False
    seen.add(x); stack.add(x); cyc=any(dfs(y) for y in adj.get(x,[])); stack.remove(x); return cyc
if any(dfs(x) for x in list(S)): hard.append('cycle detected')
node={n.get('evidence_id'):n for n in g.get('nodes',[])}
rank={'CONTEXTUAL':0,'MATERIAL_SECONDARY':1,'DECISION_CRITICAL':2}
clearance='CLEAR'
def raise_clear(level):
    global clearance
    order={'CLEAR':0,'CLEAR_WITH_CONFIDENCE_CAP':1,'HOLD':2,'BLOCK':3}
    if order[level]>order[clearance]: clearance=level
for e in g.get('edges',[]):
    a1=node.get(e.get('from'),{}); b1=node.get(e.get('to'),{}); mat=max([a1.get('decision_materiality','CONTEXTUAL'),b1.get('decision_materiality','CONTEXTUAL')],key=lambda x:rank.get(x,0))
    same=a1.get('root_cause_id')==b1.get('root_cause_id')
    if e.get('relation')=='INDEPENDENT_EVIDENCE' and same:
        issues.append({'type':'SAME_ROOT_FALSE_INDEPENDENCE','materiality':mat,'edge':e})
        raise_clear('HOLD' if mat=='DECISION_CRITICAL' else ('CLEAR_WITH_CONFIDENCE_CAP' if mat=='MATERIAL_SECONDARY' else 'CLEAR'))
    if e.get('relation')=='UNKNOWN_DEPENDENCY':
        issues.append({'type':'UNKNOWN_DEPENDENCY','materiality':mat,'edge':e})
        raise_clear('HOLD' if mat=='DECISION_CRITICAL' else ('CLEAR_WITH_CONFIDENCE_CAP' if mat=='MATERIAL_SECONDARY' else 'CLEAR'))
if hard: clearance='BLOCK'
out={'status':'PASS' if not hard else 'FAIL','hard_errors':hard,'issues':issues,'decision_clearance':clearance}
if a.output: Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2)); sys.exit(0 if not hard else 2)
