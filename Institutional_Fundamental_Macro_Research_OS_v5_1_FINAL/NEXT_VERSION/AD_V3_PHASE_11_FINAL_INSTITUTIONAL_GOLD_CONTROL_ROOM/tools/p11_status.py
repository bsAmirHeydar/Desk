from __future__ import annotations
import json,pathlib
P=pathlib.Path(__file__).resolve().parents[1];N=P.parent;REPO=N.parents[1]
def load(p,default=None):
 try:return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
 except Exception:return default

def main():
 man=load(P/'DEVELOPMENT_MANIFEST.json',{});handoff=load(P/'PHASE_11_HANDOFF.json',{});p10=N/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN';latest=p10/'artifacts/latest';ls=load(latest/'last_success.json');p09=load(N/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/artifacts/state/forward_state.json',{})
 out={'record_type':'AD_V3_P11_STATUS','phase':'AD-V3-P11','version':man.get('version','3.11.0-final-control-room'),'acceptance_status':handoff.get('p11_status') or man.get('status','IMPLEMENTED_PENDING_ACCEPTANCE'),'canonical_renderer':'AD-V3-P11','p04_renderer_authority':'LEGACY_COMPATIBILITY','view_model_schema':'1.0.0','html_contract':'1.0.0','visual_acceptance':handoff.get('visual_acceptance','NOT_RECORDED'),'last_v3_success':ls,'p09_forward_state':(p09.get('statistics') or {}).get('forward_evidence_state','NO_SAMPLES'),'v3_state':'SHADOW_COMMISSIONING','promotion_performed':False,'trade_execution_authority':'NONE'}
 print(json.dumps(out,ensure_ascii=False,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
