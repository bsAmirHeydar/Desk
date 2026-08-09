from pathlib import Path
from .util import load_json,now,uid,validate_scientific_schema
from .ledger import D4Ledger
class OutcomeError(RuntimeError):pass
def _mid(p):
    if p.get('mid') is not None:return p['mid']
    if p.get('bid') is not None and p.get('ask') is not None:return (p['bid']+p['ask'])/2
    if p.get('close') is not None:return p['close']
    return None
class OutcomeEngine:
    def __init__(self,vault,rt):self.vault=Path(vault);self.rt=rt;self.cfg=load_json(self.vault/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'outcome_runtime_policy.json')
    def build(self,run_id,execution_receipt=None,price_path=None):
        m=self.rt.store.load_manifest(run_id)
        if not m.get('decision_seal_hash'):raise OutcomeError('decision seal required')
        try:return self.rt.store.load_artifact_json(run_id,'d4_outcome'),self.rt.store.load_artifact_json(run_id,'r3_outcome_receipt')
        except Exception:pass
        ex=execution_receipt or {};status=ex.get('status');meta=(price_path or {}).get('metadata') or {};horizon_matured=bool(ex.get('metadata',{}).get('horizon_matured') or meta.get('horizon_matured'))
        maturity='IMMATURE';rr=mfe=mae=cost=None;basis='WAITING_FOR_DECLARED_HORIZON';exit_reason=status or 'PENDING';ttt=ttm=None
        if status=='NOT_TRIGGERED':maturity='EXPIRY_WITHOUT_TRIGGER';basis='NO_TRIGGER_EXPLICIT';exit_reason='NO_TRIGGER'
        elif status=='CLOSED':
            entry=ex.get('entry_price');stop=ex.get('initial_stop_price');exitp=ex.get('exit_price');side=ex.get('side');cost=ex.get('cost_r')
            if ex.get('realized_pnl') is not None and ex.get('initial_risk_value') not in (None,0):rr=ex['realized_pnl']/abs(ex['initial_risk_value'])-(cost or 0);basis='EXECUTION_VALUES';maturity='MATURE'
            elif None not in (entry,stop,exitp) and side in ('BUY','SELL'):
                risk=abs(entry-stop)
                if risk>0:rr=(1 if side=='BUY' else -1)*(exitp-entry)/risk-(cost or 0);basis='SINGLE_LEG_PRICE_PATH';maturity='MATURE'
            if maturity=='MATURE' and price_path and None not in (entry,stop) and side in ('BUY','SELL'):
                risk=abs(entry-stop);vals=[]
                for p in price_path.get('points',[]):
                    hi=p.get('high');lo=p.get('low');mid=_mid(p)
                    if side=='BUY':fav=hi if hi is not None else mid;adv=lo if lo is not None else mid;fr=(fav-entry)/risk if fav is not None and risk else None;ar=(adv-entry)/risk if adv is not None and risk else None
                    else:fav=lo if lo is not None else mid;adv=hi if hi is not None else mid;fr=(entry-fav)/risk if fav is not None and risk else None;ar=(entry-adv)/risk if adv is not None and risk else None
                    if fr is not None and ar is not None:vals.append((fr,ar,p.get('time_utc')))
                if vals:mfe=max(x[0] for x in vals);mae=min(x[1] for x in vals)
        elif m['state']=='NO_TRADE' and horizon_matured:maturity='UNSCORABLE';basis='NO_TRADE_AT_DECLARED_HORIZON';exit_reason='NO_TRADE'
        if maturity=='IMMATURE':
            provisional={'record_type':'OUTCOME','outcome_id':uid('OUT'),'run_id':run_id,'maturity_state':'IMMATURE','metadata':{'calculation_basis':basis,'decision_seal_hash':m['decision_seal_hash']}}
            validate_scientific_schema(self.vault,'102 Forward Validation Calibration Promotion and Scientific Governance Engine/schemas/AlphaLab_D4_Outcome.schema.json',provisional)
            check={'schema_version':'1.0.0','run_id':run_id,'maturity_state':'IMMATURE','calculation_basis':basis,'created_at_utc':now()};self.rt.store.put_artifact(run_id,'r3_outcome_check_'+uid('CHK').lower(),'OUTCOME','OUTCOME',check,'application/json',producer_process_id='R3_OUTCOME',producer_version='R3.0.0');return provisional,check
        outcome={'record_type':'OUTCOME','outcome_id':uid('OUT'),'run_id':run_id,'maturity_state':maturity,'matured_at_utc':now(),'metadata':{'calculation_basis':basis,'decision_seal_hash':m['decision_seal_hash']},'exit_reason':exit_reason}
        for k,v in [('realized_r',rr),('mfe_r',mfe),('mae_r',mae),('cost_r',cost),('time_to_trigger_seconds',ttt),('time_to_mfe_seconds',ttm)]:
            if v is not None:outcome[k]=v
        validate_scientific_schema(self.vault,'102 Forward Validation Calibration Promotion and Scientific Governance Engine/schemas/AlphaLab_D4_Outcome.schema.json',outcome)
        ref=self.rt.store.put_artifact(run_id,'d4_outcome','OUTCOME','OUTCOME',outcome,'application/json',producer_process_id='R3_OUTCOME',producer_version='R3.0.0');receipt={'schema_version':'1.0.0','run_id':run_id,'outcome_artifact_hash':ref['artifact_hash'],'calculation_basis':basis,'verification':{'decision_seal_present':True,'maturity_state':maturity},'created_at_utc':now()};self.rt.store.put_artifact(run_id,'r3_outcome_receipt','OUTCOME','OUTCOME',receipt,'application/json',producer_process_id='R3_OUTCOME',producer_version='R3.0.0');D4Ledger(self.rt).append('OUTCOME',outcome,run_id)
        cur=self.rt.store.load_manifest(run_id)['state']
        if cur in ('EXECUTED','NO_TRIGGER','NO_TRADE'):self.rt.lifecycle.transition(run_id,'OUTCOME_MATURED','R3_OUTCOME_MATURED',{'maturity_state':maturity})
        return outcome,receipt
