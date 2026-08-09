from pathlib import Path
import json
from datetime import datetime,timezone
from .util import load_json,now,uid,dump_json
from .forward import ForwardObservationRecorder

class ExecutionError(RuntimeError): pass
def _parse_valid_until(finalp):
    v=finalp.get('validity') or {}
    for k in ('valid_until_utc','expires_at_utc','until_utc'):
        if v.get(k): return v[k]
    return None
def _expired(ts):
    if not ts:return False
    try:return datetime.fromisoformat(ts.replace('Z','+00:00')) <= datetime.now(timezone.utc)
    except Exception:return True
class ExecutionManager:
    def __init__(self,vault,rt):
        self.vault=Path(vault);self.rt=rt;self.cfg=load_json(self.vault/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'execution_profiles.json')
    def handoff(self,run_id):
        m=self.rt.store.load_manifest(run_id)
        if not m.get('decision_seal_hash'): raise ExecutionError('decision seal required')
        if m['state']!='DECISION_FROZEN': raise ExecutionError('handoff requires DECISION_FROZEN')
        ForwardObservationRecorder(self.vault,self.rt).build(run_id)
        fp=self.rt.store.load_artifact_json(run_id,'final_permission'); req=self.rt.store.load_artifact_json(run_id,'run_request'); profile=req.get('execution_profile') or 'PERMISSION_ONLY_V1'
        if profile not in self.cfg['profiles']: status='BLOCKED_EXECUTION_PROFILE'
        elif m['run_mode']=='SHADOW_LIVE' or self.cfg['profiles'][profile]['mode']=='SHADOW_ONLY': status='SHADOW_ONLY'
        elif fp['permission']=='NO_TRADE': status='BLOCKED_NO_TRADE'
        elif _expired(_parse_valid_until(fp)): status='BLOCKED_EXPIRED'
        else: status='AUTHORIZED_TO_HANDOFF'
        h={'schema_version':'1.0.0','handoff_id':uid('HANDOFF'),'run_id':run_id,'instrument':fp['instrument'],'scientific_permission':fp['permission'],'operational_status':status,'execution_profile':profile,'valid_until_utc':_parse_valid_until(fp),'review_trigger':fp.get('review_trigger') or {},'invalidation_triggers':fp.get('invalidation_triggers') or [],'decision_seal_hash':m['decision_seal_hash'],'direction_authority':'FUNDAMENTAL_ONLY','runtime_permission_mutation':False,'created_at_utc':now(),'outbox_path':None}
        if status=='AUTHORIZED_TO_HANDOFF':
            self.rt.lifecycle.transition(run_id,'PERMISSION_ISSUED','R3_PERMISSION_HANDOFF_READY',{})
            outdir=self.rt.data_root/'outbox'/'execution';outdir.mkdir(parents=True,exist_ok=True);p=outdir/(run_id+'.json');h['outbox_path']=str(p);dump_json(p,h)
            self.rt.lifecycle.transition(run_id,'EXECUTION_PENDING','R3_EXECUTION_PENDING',{})
        elif status=='BLOCKED_NO_TRADE': self.rt.lifecycle.transition(run_id,'NO_TRADE','R3_NO_TRADE',{})
        elif status=='SHADOW_ONLY': self.rt.lifecycle.transition(run_id,'NO_TRADE','R3_SHADOW_NO_EXECUTION',{})
        else: self.rt.lifecycle.transition(run_id,'NO_TRADE','R3_OPERATIONAL_BLOCK',{'status':status})
        ref=self.rt.store.put_artifact(run_id,'execution_handoff','OUTCOME','EXECUTION',h,'application/json',producer_process_id='R3_EXECUTION_GATE',producer_version='R3.0.0')
        with self.rt.catalog.connect() as c:c.execute("INSERT OR REPLACE INTO r3_execution_handoffs(handoff_id,run_id,scientific_permission,operational_status,execution_profile,artifact_hash,created_at_utc) VALUES(?,?,?,?,?,?,?)",(h['handoff_id'],run_id,h['scientific_permission'],status,profile,ref['artifact_hash'],h['created_at_utc']))
        return h
    def ingest_receipt(self,receipt):
        run_id=receipt['run_id']; m=self.rt.store.load_manifest(run_id)
        if not m.get('decision_seal_hash'): raise ExecutionError('outcome firewall: decision seal required')
        ref=self.rt.store.put_artifact(run_id,'execution_receipt_'+receipt['execution_id'].lower(),'OUTCOME','EXECUTION',receipt,'application/json',producer_process_id='R3_EXECUTION_ADAPTER',producer_version='R3.0.0')
        with self.rt.catalog.connect() as c:c.execute("INSERT OR REPLACE INTO r3_execution_receipts(execution_id,run_id,status,artifact_hash,received_at_utc) VALUES(?,?,?,?,?)",(receipt['execution_id'],run_id,receipt['status'],ref['artifact_hash'],receipt['received_at_utc']))
        st=m['state']
        if receipt['status']=='NOT_TRIGGERED' and st=='EXECUTION_PENDING': self.rt.lifecycle.transition(run_id,'NO_TRIGGER','R3_EXECUTION_NOT_TRIGGERED',{})
        elif receipt['status'] in ('EXECUTED','CLOSED') and st=='EXECUTION_PENDING': self.rt.lifecycle.transition(run_id,'EXECUTED','R3_EXECUTED',{'execution_id':receipt['execution_id']})
        return ref
