from __future__ import annotations
import json,pathlib,hashlib,sys
P=pathlib.Path(__file__).resolve().parents[1];N=P.parent;REPO=N.parents[1]
def load(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def main():
 errs=[]
 for x in ['report_contract.json','presentation_policy.json','security_policy.json','label_registry.json','help_registry.json']:
  if not (P/'config'/x).exists():errs.append('missing config '+x)
 for x in ['control_room_view_model.schema.json','report_receipt.schema.json']:
  if not (P/'schemas'/x).exists():errs.append('missing schema '+x)
 p10=(N/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/gold_orchestrator.py').read_text(encoding='utf-8');p04=(N/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING/runtime/renderer.py').read_text(encoding='utf-8')
 if 'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM' not in p10:errs.append('P10 does not invoke P11')
 if 'render_p11_report' not in p10:errs.append('P11 render call missing')
 contract=load(P/'config/report_contract.json')
 if contract.get('legacy_v3_renderer')=='AD-V3-P11':errs.append('legacy renderer invalid')
 if contract.get('canonical_v3_html_authority')!='AD-V3-P11':errs.append('canonical renderer config')
 # Upstream authority hashes captured before P11 must remain unchanged.
 b=load(P/'baseline/PRE_P11_AUTHORITY_HASHES.json'); drift=[]
 for rel,expected in (b.get('hashes') or {}).items():
  if rel.endswith('/AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/config/stage_dag.json'): continue
  q=REPO/rel
  if q.exists() and sha(q)!=expected:drift.append(rel)
 if drift:errs.append('authority drift: '+','.join(drift))
 # P10 stage DAG topology must remain identical; only CONTROL_MODEL/REPORT authority transition to P11 is allowed.
 pre=load(P/'baseline/PRE_P11_P10_STAGE_DAG.json'); cur=load(N/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/config/stage_dag.json')
 pre_top=[(x['stage_id'],tuple(x.get('depends_on') or []),x.get('mandatory')) for x in pre.get('stages',[])]
 cur_top=[(x['stage_id'],tuple(x.get('depends_on') or []),x.get('mandatory')) for x in cur.get('stages',[])]
 if pre_top!=cur_top: errs.append('P10 stage DAG topology drift')
 auth={x['stage_id']:x.get('authority') for x in cur.get('stages',[])}
 if auth.get('CONTROL_MODEL')!='AD-V3-P11' or auth.get('REPORT')!='AD-V3-P11': errs.append('P11 stage authority transition missing')

 out={'phase':'AD-V3-P11','version':'3.11.0-final-control-room','status':'PASS' if not errs else 'FAIL','errors':errs,'authority_drift':drift};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if not errs else 2
if __name__=='__main__':raise SystemExit(main())
