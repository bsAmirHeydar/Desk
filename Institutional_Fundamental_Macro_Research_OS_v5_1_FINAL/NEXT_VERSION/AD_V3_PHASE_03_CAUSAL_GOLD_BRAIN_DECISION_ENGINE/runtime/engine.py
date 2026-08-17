from __future__ import annotations
from pathlib import Path
from .common import load_json, stable_id, iso
from .loader import latest_receipt, observation_history, current_previous_for_receipt, load_bundle
from .interpreter import auto_interpret, apply_bundle
from .planes import causal_plane, structural_plane, transaction_plane, mechanical_plane
from .transmission import price_transmission, model_quality
from .decision import shadow_decision
from .lifecycle import persistence_stack, consumption_vector, remaining_pressure
from .hypotheses import build_hypotheses

def execute(phase_root, p02_data_root, coverage_path=None, adjudication_path=None, horizon='SESSION_1_6H'):
    phase=Path(phase_root); p01=phase.parent/'AD_V3_PHASE_01_TOTAL_GOLD_KNOWLEDGE_SCIENCE_FOUNDATION'; p02=phase.parent/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC'
    reason=load_json(phase/'config/fact_reasoning_registry.json'); roots=load_json(phase/'config/root_family_registry.json'); root_paths=load_json(phase/'config/root_pathway_registry.json')
    coverage=load_json(coverage_path) if coverage_path else latest_receipt(p02_data_root)
    if coverage.get('analysis_admission')=='BLOCKED' or not coverage.get('analysis_may_start'):
        return {'record_type':'AD_V3_P03_CAUSAL_BRAIN_RECEIPT','receipt_id':stable_id('P03BRAIN',{'coverage':coverage.get('receipt_id'),'blocked':True}),'phase':'AD-V3-P03','subject':'XAUUSD','generated_at_utc':iso(),'analysis_admission':'BLOCKED','reason':'P02_COVERAGE_BLOCKED','production_direction_authority_granted':False,'production_trade_permission_authority_granted':False}
    # Load full lineage first, then bind the reasoning ledger to the exact
    # acquisition run certified by the P02 coverage receipt. Never cut current
    # observations using the receipt generation timestamp alone.
    hist=observation_history(p02_data_root,None); hp,handoff_meta=current_previous_for_receipt(hist,coverage)
    expected_fids=[c['fact_id'] for c in reason['contracts']]
    missing_current=[fid for fid in expected_fids if not hp.get(fid,{}).get('current')]
    current_loaded=len(expected_fids)-len(missing_current)
    handoff_integrity={**handoff_meta,'expected_current_observations':len(expected_fids),'current_observations_loaded':current_loaded,'missing_current_fact_ids':missing_current,'complete':not missing_current}
    if missing_current:
        return {'record_type':'AD_V3_P03_CAUSAL_BRAIN_RECEIPT','receipt_id':stable_id('P03BRAIN',{'coverage':coverage.get('receipt_id'),'handoff_incomplete':missing_current}),'phase':'AD-V3-P03','subject':'XAUUSD','generated_at_utc':iso(),'horizon':horizon,'p02_coverage_receipt_id':coverage.get('receipt_id'),'analysis_admission':'BLOCKED','reason':'P02_P03_OBSERVATION_HANDOFF_INCOMPLETE','handoff_integrity':handoff_integrity,'production_direction_authority_granted':False,'production_trade_permission_authority_granted':False}
    bundle=load_bundle(adjudication_path); bmap={x['fact_id']:x for x in bundle.get('items',[])}
    analysis_stage='POST_SEMANTIC' if adjudication_path else 'PRE_SEMANTIC'
    semantic_bundle_id=stable_id('P03SEMBUNDLE',bundle) if adjudication_path else None
    rows=[]
    for c in reason['contracts']:
        pair=hp.get(c['fact_id'],{}); cur=pair.get('current'); prev=pair.get('previous')
        r=auto_interpret(c,cur,prev,horizon=horizon); r=apply_bundle(r,bmap.get(c['fact_id']),c,cur)
        rows.append(r)
    # Exact fact-accounting gate.
    fids=[r['fact_id'] for r in rows]
    if len(rows)!=192 or len(set(fids))!=192:
        raise RuntimeError('P03_REASONING_LEDGER_FACT_PARITY_FAILURE')
    causal=causal_plane(rows,roots); structural=structural_plane(rows,roots); transaction=transaction_plane(rows,reason['contracts']); mechanical=mechanical_plane(rows,reason['contracts'])
    transmission=price_transmission(rows,causal['direction']); quality=model_quality(coverage,causal,transmission); decision=shadow_decision(causal,transaction,mechanical,structural,transmission,quality)
    persistence=persistence_stack(causal,reason['contracts'],horizon=horizon); consumption=consumption_vector(rows,causal,transaction,mechanical); remaining=remaining_pressure(causal,consumption,persistence); hypotheses=build_hypotheses(causal,root_paths)
    unresolved=[r['fact_id'] for r in rows if r.get('resolution') in ('UNRESOLVED','ACCOUNTED_REQUIRES_SEMANTIC')]
    adjudication_request=[{'fact_id':r['fact_id'],'observation_id':r.get('observation_id'),'role':r.get('role'),'causal_root_family':r.get('causal_root_family'),'pressure_plane':r.get('pressure_plane'),'required_semantic_output':['effect_on_gold','effect_kind','strength','is_additive','causal_owner_id','rationale_summary']} for r in rows if r.get('resolution')=='ACCOUNTED_REQUIRES_SEMANTIC' and r.get('observation_id')]
    receipt_seed={'coverage':coverage.get('receipt_id'),'horizon':horizon,'analysis_stage':analysis_stage,'semantic_bundle_id':semantic_bundle_id,'decision':decision}
    receipt={'record_type':'AD_V3_P03_CAUSAL_BRAIN_RECEIPT','receipt_id':stable_id('P03BRAIN',receipt_seed),'phase':'AD-V3-P03','subject':'XAUUSD','generated_at_utc':iso(),'horizon':horizon,'analysis_stage':analysis_stage,'semantic_bundle_id':semantic_bundle_id,'p02_coverage_receipt_id':coverage.get('receipt_id'),'handoff_integrity':handoff_integrity,'analysis_admission':'DEGRADED' if coverage.get('analysis_admission')=='DEGRADED' or unresolved else 'PASS','reasoning_ledger':{'record_type':'AD_V3_P03_REASONING_LEDGER','fact_count':192,'rows':rows,'unresolved_fact_ids':unresolved,'zero_silent_omission':True},'pressure_planes':{'causal_fundamental':causal,'realized_transaction':transaction,'mechanical_forced':mechanical,'structural_carry':structural},'price_transmission':transmission,'model_quality':quality,'lifecycle':{'consumption_vector':consumption,'persistence_stack':persistence,'remaining_pressure':remaining},'hypotheses':hypotheses,'semantic_adjudication_request':adjudication_request,'shadow_decision':decision,'production_direction_authority_granted':False,'production_trade_permission_authority_granted':False,'hard_note':'P03 is SHADOW_ONLY. Direction/action are research candidates, not production permission.'}
    return receipt
