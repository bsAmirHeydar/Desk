from pathlib import Path
import json
from .util import now
class Reporter:
    FULL=['scope_state','visibility_receipt','r3_retrieval_receipt','evidence_integrity_receipt','temporal_clearance','fundamental_state','surprise_state','policy_reaction_state','regime_state','narrative_state','reflexivity_state','consumption_state','driver_transition','positioning_state','flow_state','funding_plumbing_state','mechanics_capacity_state','market_state_reconciliation','hypothesis_set','causal_graph','scenario_tree','adversarial_review','model_disagreement','premortem','global_reconciliation','d3_adjudication','decision_utility','d4_authority_receipt','research_intent','cognitive_adjudication','final_permission']
    COMPACT=['fundamental_state','regime_state','narrative_state','market_state_reconciliation','hypothesis_set','scenario_tree','d3_adjudication','d4_authority_receipt','research_intent','cognitive_adjudication','final_permission']
    def __init__(self,vault,rt):self.vault=Path(vault);self.rt=rt
    def _get(self,r,n):
        try:return self.rt.store.load_artifact_json(r,n)
        except Exception:return None
    def render(self,run_id,depth='FULL'):
        m=self.rt.store.load_manifest(run_id)
        if not m.get('decision_seal_hash'):raise RuntimeError('report requires decision seal')
        names=self.FULL if depth.upper()=='FULL' else self.COMPACT;sections={n:self._get(run_id,n) for n in names};sections={k:v for k,v in sections.items() if v is not None};refs=[{'logical_name':x['logical_name'],'artifact_hash':x['artifact_hash'],'world':x['world'],'stage':x['stage']} for x in self.rt.catalog.list_artifacts(run_id,'DECISION')]
        fp=sections.get('final_permission') or {};ri=sections.get('research_intent') or {};ret=sections.get('r3_retrieval_receipt') or {}
        machine={'schema_version':'1.0.0','run_id':run_id,'analysis_cutoff_utc':m['analysis_cutoff_utc'],'instrument':m['subject'],'run_mode':m['run_mode'],'vault_commit':m.get('vault_commit'),'prompt_pack_version':m.get('prompt_pack_version'),'decision_seal_hash':m['decision_seal_hash'],'final_permission':fp.get('permission'),'fundamental_direction':ri.get('fundamental_direction'),'edge_state':ri.get('edge_state'),'material_gaps':ret.get('gaps',[]),'decision_artifact_index':refs,'sections':sections,'generated_at_utc':now()}
        lines=['# Alpha Lab Run Report','',f"- Run: `{run_id}`",f"- Instrument: **{m['subject']}**",f"- Mode: `{m['run_mode']}`",f"- Cutoff: `{m['analysis_cutoff_utc']}`",f"- Vault commit: `{m.get('vault_commit')}`",f"- Decision seal: `{m['decision_seal_hash']}`",f"- Permission: **{fp.get('permission')}**",f"- Fundamental direction: **{ri.get('fundamental_direction')}**",f"- Edge state: **{ri.get('edge_state')}**",'',f"## Material evidence gaps ({len(ret.get('gaps',[]))})"]
        for g in ret.get('gaps',[]):lines.append(f"- {g.get('fact_family')} / {g.get('materiality')}: {g.get('status')} — {g.get('reason','')}")
        for n in names:
            if n in sections:lines += ['', '## '+n, '```json', json.dumps(sections[n],ensure_ascii=False,indent=2), '```']
        md='\n'.join(lines)+'\n';r1=self.rt.store.put_artifact(run_id,'r3_machine_report','OUTCOME','OUTCOME',machine,'application/json',producer_process_id='R3_REPORT',producer_version='R3.0.0');r2=self.rt.store.put_artifact(run_id,'r3_human_report','OUTCOME','OUTCOME',md,'text/markdown',producer_process_id='R3_REPORT',producer_version='R3.0.0');idx={'schema_version':'1.0.0','run_id':run_id,'machine_report_hash':r1['artifact_hash'],'human_report_hash':r2['artifact_hash'],'output_depth':depth.upper(),'created_at_utc':now()};self.rt.store.put_artifact(run_id,'r3_report_index','OUTCOME','OUTCOME',idx,'application/json',producer_process_id='R3_REPORT',producer_version='R3.0.0');return idx
