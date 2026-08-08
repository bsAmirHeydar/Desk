#!/usr/bin/env python3
import argparse,json,re,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);p.add_argument('--symbol',required=True);p.add_argument('--extra-path',action='append',default=[]);p.add_argument('--material-topic',action='append',default=[]);p.add_argument('--history-mode',action='store_true');p.add_argument('--output',required=True);a=p.parse_args();r=Path(a.vault_root)
m=json.loads((r/'CURRENT_PRODUCTION_MANIFEST.json').read_text(encoding='utf-8'));pol=json.loads((r/m['retrieval_policy']).read_text(encoding='utf-8'))
if a.symbol not in m['production_universe']: print('invalid symbol'); sys.exit(2)
sel=[m['production_entrypoint'],*m['canonical_authorities'].values(),*m['allowed_live_subengines']];sel+=m.get('asset_books',{}).get(a.symbol,[]);sel+=a.extra_path
exp=[]
dep=r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/config/retrieval_topic_dependencies.json'
if dep.exists() and a.material_topic:
    dm=json.loads(dep.read_text(encoding='utf-8'))
    blob=' | '.join(a.material_topic).lower()
    for item in dm.get('topics',[]):
        if any(k.lower() in blob for k in item.get('keywords',[])):
            for path in item.get('paths',[]):
                sel.append(path);exp.append({'matched_keywords':[k for k in item.get('keywords',[]) if k.lower() in blob],'path':path})
outsel=[]
for x in sel:
    if x not in outsel:outsel.append(x)
rejected=[];errors=[]
def status(path):
    t=path.read_text(encoding='utf-8',errors='ignore')[:2500];m1=re.search(r'(?m)^status:\s*["\']?([^"\'\n]+)',t);return m1.group(1).strip() if m1 else None
for x in list(outsel):
    q=r/x
    if not q.exists():errors.append('missing '+x);continue
    if q.suffix.lower()=='.md':
        st=status(q)
        if st in pol['forbidden_load_bearing_statuses'] and not a.history_mode:rejected.append({'path':x,'status':st});errors.append('forbidden production retrieval '+x)
# Coverage is now evidenced by selected authority/path families instead of copied blindly.
dim_prefix={
 'fundamental_core':['89 '],'narrative_transmission':['90 '],'instrument_identity':['91 '],'asset_specific':['89 ','90 ','100 ','101 ','102 ','103 '],'timing':['93 '],'evidence_governance':['95 '],'edge_permission':['92 ','101 '],'operational_safety':['94 '],
 'positioning_ownership':['96 '],'actual_flow':['97 '],'funding_plumbing':['98 '],'institutional_mechanics':['99 '],'market_capacity':['99 '],
 'competing_hypotheses':['103 '],'horizon_reasoning':['89 ','103 '],'scenario_intelligence':['103 '],'regime_conditioning':['103 '],'adversarial_review':['103 '],'cognitive_semantic_integrity':['103 ']
}
coverage={}
for d in pol['mandatory_dimensions']:
    prefs=dim_prefix.get(d,[]);paths=[x for x in outsel if any(x.startswith(p) for p in prefs)];coverage[d]={'covered':bool(paths),'evidence_paths':paths[:8]}
    if not paths:errors.append('uncovered mandatory dimension '+d)
plan={'symbol':a.symbol,'selected_paths':outsel,'dimensions_covered':[d for d,v in coverage.items() if v['covered']],'dimension_coverage':coverage,'history_mode':bool(a.history_mode),'material_topics':a.material_topic,'topic_expansions':exp,'rejected_paths':rejected}
Path(a.output).write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8');print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors,'selected':len(outsel),'topic_expansions':len(exp),'rejected':rejected},indent=2));sys.exit(0 if not errors else 2)
