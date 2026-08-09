from .util import now,uid
class MetaReconciler:
    def __init__(self,rt):self.rt=rt
    def reconcile(self,run_ids):
        if not run_ids:raise RuntimeError('at least one component run is required')
        comps=[]
        for rid in run_ids:
            m=self.rt.store.load_manifest(rid)
            if not m.get('decision_seal_hash'):raise RuntimeError('all component runs must be decision-sealed')
            fp=self.rt.store.load_artifact_json(rid,'final_permission'); gr=self.rt.store.load_artifact_json(rid,'global_reconciliation')
            comps.append({'run_id':rid,'instrument':m['subject'],'permission':fp.get('permission'),'analysis_cutoff_utc':m['analysis_cutoff_utc'],'vault_commit':m.get('vault_commit'),'decision_seal_hash':m['decision_seal_hash'],'global_reconciliation':gr})
        bad=[x for x in comps if str(x['global_reconciliation'].get('state','')).upper() in ('CONTESTED','RECHECK_REQUIRED','INSUFFICIENT_EVIDENCE')]
        state='RECHECK_REQUIRED' if bad else ('MIXED' if len(set(x['permission'] for x in comps))>1 else 'CONSISTENT')
        cuts=sorted(set(x['analysis_cutoff_utc'] for x in comps)); commits=sorted(set(x.get('vault_commit') for x in comps))
        return {'schema_version':'1.0.0','meta_run_id':uid('META'),'component_run_ids':list(run_ids),'components':comps,'state':state,'temporal_alignment':('EXACT' if len(cuts)==1 else 'NON_ATOMIC_RECORDED'),'component_cutoffs_utc':cuts,'atomic_snapshot_claim':len(cuts)==1,'vault_commit_alignment':('EXACT' if len(commits)==1 else 'MIXED'),'inconsistencies':[{'run_id':x['run_id'],'instrument':x['instrument'],'component_state':x['global_reconciliation'].get('state')} for x in bad],'recheck_run_ids':[x['run_id'] for x in bad],'permission_effect':'NONE_DIRECT','created_at_utc':now()}
