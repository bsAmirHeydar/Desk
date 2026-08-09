from pathlib import Path
from .util import load_json,now,uid,validate_scientific_schema
from .ledger import D4Ledger
class CounterfactualError(RuntimeError):pass
class CounterfactualEngine:
    def __init__(self,vault,rt):self.vault=Path(vault);self.rt=rt;self.cfg=load_json(self.vault/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'counterfactual_runtime_policy.json')
    def plan(self,run_id):
        m=self.rt.store.load_manifest(run_id)
        if not m.get('decision_seal_hash'):raise CounterfactualError('decision seal required')
        try:return self.rt.store.load_artifact_json(run_id,'counterfactual_plan')
        except Exception:pass
        d3=self.rt.store.load_artifact_json(run_id,'d3_adjudication');d4=self.rt.store.load_artifact_json(run_id,'d4_authority_receipt');fp=self.rt.store.load_artifact_json(run_id,'final_permission');branches=[{'branch':'PRE_D3_BASELINE','hypothetical_permission':d3.get('pre_d3_permission'),'basis':'frozen_d3_artifact'},{'branch':'V19_D3_BASELINE','hypothetical_permission':d3.get('final_permission'),'basis':'frozen_d3_artifact'}]
        for x in d4.get('applied_promotion_ids',[]):branches.append({'branch':'REMOVE_MODIFIER','modifier_id':x,'hypothetical_permission':d3.get('final_permission'),'basis':'remove_applied_promotion_without_ex_post_entry_choice'})
        for x in d4.get('shadow_candidate_ids',[]):branches.append({'branch':'POSITIVE_PROMOTION_SHADOW','modifier_id':x,'hypothetical_permission':fp.get('permission'),'basis':'shadow_only'})
        plan={'schema_version':'1.0.0','run_id':run_id,'decision_seal_hash':m['decision_seal_hash'],'policy_version':'1.0.0','branches':branches,'same_frozen_information_set':True,'same_execution_profile':True,'ex_post_entry_selection':False,'created_at_utc':now()};self.rt.store.put_artifact(run_id,'counterfactual_plan','OUTCOME','OUTCOME',plan,'application/json',producer_process_id='R3_COUNTERFACTUAL',producer_version='R3.0.0');return plan
    def attach_unscorable(self,run_id,plan=None):
        plan=plan or self.plan(run_id);records=[]
        for b in plan['branches']:
            r={'record_type':'COUNTERFACTUAL_OUTCOME','counterfactual_id':uid('CF'),'run_id':run_id,'branch':b['branch'],'policy_version':plan['policy_version'],'score_state':'UNSCORABLE','metadata':{'reason':'No deterministic same-profile hypothetical execution path supplied.','decision_seal_hash':plan['decision_seal_hash']}}
            if b.get('modifier_id'):r['modifier_id']=b['modifier_id']
            if b.get('hypothetical_permission') in ('BUY','SELL','NO_TRADE'):r['hypothetical_permission']=b['hypothetical_permission']
            self._store(r);records.append(r)
        self._advance(run_id,len(records));return records
    def ingest_scored(self,run_id,result):
        plan=self.plan(run_id);branch=result.get('branch');allowed={(x['branch'],x.get('modifier_id')) for x in plan['branches']}
        if (branch,result.get('modifier_id')) not in allowed:raise CounterfactualError('result branch was not predeclared in frozen plan')
        if result.get('score_state') not in ('MATURE','EXPIRY_WITHOUT_TRIGGER','UNSCORABLE'):raise CounterfactualError('invalid score_state')
        md=result.get('metadata') or {}
        if result.get('score_state')=='MATURE' and not md.get('deterministic_same_profile_replay'):raise CounterfactualError('mature counterfactual requires deterministic_same_profile_replay receipt')
        if md.get('ex_post_entry_selection'):raise CounterfactualError('ex-post entry selection forbidden')
        r={'record_type':'COUNTERFACTUAL_OUTCOME','counterfactual_id':uid('CF'),'run_id':run_id,'branch':branch,'policy_version':plan['policy_version'],'score_state':result['score_state'],'metadata':{**md,'decision_seal_hash':plan['decision_seal_hash']}}
        for k in ('modifier_id','hypothetical_permission','realized_r','mfe_r','mae_r'):
            if result.get(k) is not None:r[k]=result[k]
        self._store(r);return r
    def _store(self,r):
        validate_scientific_schema(self.vault,'102 Forward Validation Calibration Promotion and Scientific Governance Engine/schemas/AlphaLab_D4_Counterfactual.schema.json',r)
        ref=self.rt.store.put_artifact(r['run_id'],'counterfactual_'+r['counterfactual_id'].lower(),'OUTCOME','OUTCOME',r,'application/json',producer_process_id='R3_COUNTERFACTUAL',producer_version='R3.0.0')
        with self.rt.catalog.connect() as c:c.execute('INSERT INTO r3_counterfactuals(counterfactual_id,run_id,branch,score_state,hypothetical_permission,realized_r,mfe_r,mae_r,artifact_hash,created_at_utc) VALUES(?,?,?,?,?,?,?,?,?,?)',(r['counterfactual_id'],r['run_id'],r['branch'],r['score_state'],r.get('hypothetical_permission'),r.get('realized_r'),r.get('mfe_r'),r.get('mae_r'),ref['artifact_hash'],now()))
        D4Ledger(self.rt).append('COUNTERFACTUAL_OUTCOME',r,r['run_id']);return ref
    def _advance(self,run_id,count):
        if self.rt.store.load_manifest(run_id)['state']=='OUTCOME_MATURED':self.rt.lifecycle.transition(run_id,'COUNTERFACTUALS_ATTACHED','R3_COUNTERFACTUALS_ATTACHED',{'count':count})
