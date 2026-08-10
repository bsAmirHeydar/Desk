from pathlib import Path
import tempfile,json
from .preflight import run as preflight
from .engine import run_suite
from .ledger import append,validate
from .util import sha

def run(vault_root):
    checks=[]
    def ck(n,x,d=None):checks.append({'name':n,'pass':bool(x),'detail':d})
    p=preflight(vault_root);ck('preflight',p['status']=='PASS',p.get('errors'))
    s=run_suite(vault_root);ck('synthetic_suite',s['status']=='PASS');ck('truth_label',s['truth_states_observed']==['SYNTHETIC_VALIDATION']);ck('true_forward_not_fabricated',s['true_forward_status']=='TRUE_FORWARD_EVIDENCE_INSUFFICIENT')
    ck('authority_unchanged',s['authority_unchanged'] is True)
    with tempfile.TemporaryDirectory(prefix='fv1_ledger_') as td:
        lp=Path(td)/'ledger.jsonl'; rec=s['records'][0]
        a=append(lp,rec);v=validate(lp);ck('append_only_hash_chain',a['status']=='PASS' and v['status']=='PASS' and v['records']==1,v)
        duplicate_rejected=False
        try: append(lp,rec)
        except RuntimeError: duplicate_rejected=True
        ck('duplicate_record_rejected',duplicate_rejected)
        payload={'run_id':'R','finding':'shadow'};h=sha(payload);ck('preoutcome_payload_hash','sha256:' in h and len(h)==71,h)
    bad=[x for x in checks if not x['pass']]
    return {'status':'PASS' if not bad else 'FAIL','validation_version':'FV1.0.0','passed':len(checks)-len(bad),'total':len(checks),'checks':checks,'errors':[x['name'] for x in bad]}
