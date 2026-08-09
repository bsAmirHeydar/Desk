from pathlib import Path
from .util import load_json,now,sha256_obj,validate_scientific_schema
from .ledger import D4Ledger
class ForwardError(RuntimeError):pass
class ForwardObservationRecorder:
    def __init__(self,vault,rt):self.vault=Path(vault);self.rt=rt
    def _get(self,r,n):
        try:return self.rt.store.load_artifact_json(r,n)
        except Exception:return {}
    def _refhash(self,r,n):
        for x in self.rt.catalog.list_artifacts(r):
            if x['logical_name']==n:return x['artifact_hash']
        return None
    def build(self,run_id,allow_unpinned=False):
        m=self.rt.store.load_manifest(run_id)
        if not m.get('decision_seal_hash'):raise ForwardError('decision seal required before D4 forward observation')
        try:return self.rt.store.load_artifact_json(run_id,'d4_forward_observation')
        except Exception:pass
        if not m.get('vault_commit') and not allow_unpinned:raise ForwardError('vault commit must be pinned before production forward observation')
        fp=self._get(run_id,'final_permission');ri=self._get(run_id,'research_intent');ca=self._get(run_id,'cognitive_adjudication');d3=self._get(run_id,'d3_adjudication');d4=self._get(run_id,'d4_authority_receipt');req=self._get(run_id,'run_request')
        fd=ca.get('fundamental_direction') or d4.get('fundamental_direction') or d3.get('fundamental_direction') or ri.get('fundamental_direction')
        if fd in ('STRONGLY_BULLISH','BULLISH'):fd='BULLISH'
        elif fd in ('STRONGLY_BEARISH','BEARISH'):fd='BEARISH'
        elif fd=='NEUTRAL':fd='NEUTRAL'
        else:fd='UNRESOLVED'
        p63=self.vault/'RUNTIME'/'R2 Prompt Execution OS'/'prompt_registry'/'P63_FINAL_DECISION'/'prompt.md';prompt_hash='sha256:'+__import__('hashlib').sha256(p63.read_bytes()).hexdigest()
        v=fp.get('validity') or {};valid_until=next((v.get(k) for k in ('valid_until_utc','expires_at_utc','until_utc') if v.get(k)),None)
        obs={'record_type':'FORWARD_OBSERVATION','run_id':run_id,'analysis_id':run_id,'instrument':m['subject'],'analysis_cutoff_utc':m['analysis_cutoff_utc'],'vault_commit':m.get('vault_commit') or 'UNPINNED_SELFTEST','prompt_sha256':prompt_hash,'state_sha256':m['decision_seal_hash'],'registry_version':d4.get('registry_version') or 'UNRESOLVED','fundamental_direction':fd,'pre_d3_permission':d3.get('pre_d3_permission') or 'NO_TRADE','v19_d3_permission':d4.get('v19_d3_permission') or d3.get('final_permission') or 'NO_TRADE','final_v20_permission':d4.get('final_v20_permission') or fp.get('permission') or 'NO_TRADE','d3_edge_quality':d3.get('d3_edge_quality'),'modifier_ids':[str(x.get('rule_id') or x.get('id')) for x in d3.get('applied_rules',[]) if isinstance(x,dict) and (x.get('rule_id') or x.get('id'))],'active_promotion_ids':d4.get('applied_promotion_ids') or [],'shadow_candidate_ids':d4.get('shadow_candidate_ids') or [],'execution_profile_version':str(req.get('execution_profile') or 'PERMISSION_ONLY_V1'),'independent_root_ids':d3.get('deduplicated_root_ids') or [],'metadata':{'decision_seal_hash':m['decision_seal_hash'],'run_mode':m['run_mode'],'prompt_pack_version':m.get('prompt_pack_version'),'runtime_version':'R3.0.0'},'cognitive_state_sha256':self._refhash(run_id,'cognitive_adjudication'),'research_intent_sha256':self._refhash(run_id,'research_intent'),'root_exposure_tags':d3.get('deduplicated_root_ids') or [],'abstention_primary_reason':(ca.get('abstention_reason_codes') or [None])[0] if isinstance(ca.get('abstention_reason_codes'),list) else None}
        if valid_until:obs['permission_valid_until_utc']=valid_until
        # Strip None optional fields to satisfy D4 additionalProperties/typing strictly.
        obs={k:v for k,v in obs.items() if v is not None}
        validate_scientific_schema(self.vault,'102 Forward Validation Calibration Promotion and Scientific Governance Engine/schemas/AlphaLab_D4_Forward_Observation.schema.json',obs)
        ref=self.rt.store.put_artifact(run_id,'d4_forward_observation','OUTCOME','LEARNING',obs,'application/json',producer_process_id='R3_D4_FORWARD',producer_version='R3.0.0')
        D4Ledger(self.rt).append('FORWARD_OBSERVATION',obs,run_id);return obs
