from .util import sha256_obj
from datetime import datetime, timezone

def now(): return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')

class GateEngine:
    def __init__(self,rt,registry): self.rt=rt; self.registry=registry; self.policy=registry.completion
    def evaluate(self,run_id,gate_id,process_status):
        cfg=self.policy['gates'][gate_id]; rows=self.rt.catalog.list_artifacts(run_id); names={r['logical_name'] for r in rows}; checks=[]
        for p in cfg['required_processes']:
            ok=process_status.get(p) in ('COMPLETED','NOT_APPLICABLE','UNAVAILABLE','UNDETERMINED')
            checks.append({'check':'process:'+p,'pass':ok})
        missing=[x for x in cfg['required_artifacts'] if x not in names]
        checks.append({'check':'required_artifacts','pass':not missing})
        # R1 world firewall check
        m=self.rt.store.load_manifest(run_id)
        future_preseal=[]
        if not m.get('decision_seal_hash'):
            future_preseal=[r['logical_name'] for r in rows if r['world'] in ('OUTCOME','LEARNING')]
        checks.append({'check':'outcome_firewall','pass':not future_preseal})
        status='PASS' if all(x['pass'] for x in checks) else 'FAIL'
        return {'schema_version':'1.0.0','run_id':run_id,'gate_id':gate_id,'status':status,'checks':checks,'missing_artifacts':missing+future_preseal,'created_at_utc':now()}
