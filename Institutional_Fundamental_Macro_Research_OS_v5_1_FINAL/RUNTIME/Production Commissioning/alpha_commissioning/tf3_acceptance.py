from pathlib import Path
import os,tempfile,shutil,json
from .continuous_forward import selftest,preflight,status,scheduler
from .util import load_json

def run(vault_root):
    v=Path(vault_root).resolve();checks=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d})
    st=selftest(v);ck('tf3_selftest',st.get('status')=='PASS',st.get('errors'))
    pf=preflight(v);ck('source_integrity',pf.get('status')=='PASS',pf.get('errors'))
    p=load_json(v/'RUNTIME'/'Production Commissioning'/'config'/'continuous_forward_policy.json')
    ck('hourly_authoritative_schedule',p['scheduler']['frequency']=='HOURLY' and p['scheduler']['interval_hours']==1)
    ck('matured_batch_review_trigger',p['review_trigger']['mode']=='MATURED_FULL_UNIVERSE_BATCH')
    ck('mutable_outside_r4',p['mutable_forward_records_in_r4_source_fingerprint'] is False)
    ck('authority_isolation',p['broker_write'] is False and p['direction_authority_added']=='NONE' and p['apl_a_authority']=='SHADOW_ONLY')
    ck('apl_b_not_implemented',p['apl_b']=='NOT_IMPLEMENTED')
    sch=scheduler(v,'status');ck('scheduler_truthful',sch.get('status') in ('PASS','PENDING'))
    cp=load_json(v/'CURRENT_PRODUCTION_MANIFEST.json');tf3=cp.get('continuous_true_forward_operations',{});ck('production_manifest_bound',tf3.get('version')=='TF3.0.0' and tf3.get('broker_write')=='NONE')
    bad=[x for x in checks if not x['pass']];return {'schema_version':'1.0.0','status':'PASS' if not bad else 'FAIL','passed':len(checks)-len(bad),'total':len(checks),'checks':checks,'errors':[x['name'] for x in bad]}
