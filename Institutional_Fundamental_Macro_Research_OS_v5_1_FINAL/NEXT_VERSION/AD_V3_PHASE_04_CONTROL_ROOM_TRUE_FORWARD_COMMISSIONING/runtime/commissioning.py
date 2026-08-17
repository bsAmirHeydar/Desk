from __future__ import annotations
import json
from pathlib import Path
from .common import load_json, write_json, stable_id, iso

def state_path(phase_root): return Path(phase_root)/'artifacts'/'commissioning'/'commissioning_state.json'
def outcomes_path(phase_root): return Path(phase_root)/'artifacts'/'commissioning'/'outcomes.jsonl'
def _sample_state(n):
    if n<5:return 'UNCALIBRATED'
    if n<20:return 'INSUFFICIENT'
    if n<50:return 'EARLY'
    return 'PROVISIONAL'
def default_state(): return {'record_type':'AD_V3_P04_COMMISSIONING_STATE','updated_at_utc':iso(),'total_capsules':0,'directional_precommits':0,'outcomes_evaluated':0,'aligned_outcomes':0,'opposed_outcomes':0,'flat_outcomes':0,'unevaluable_outcomes':0,'integrity_failures':0,'sample_state':'UNCALIBRATED','promotion_ready':False,'pending':[],'numeric_confidence_forbidden':True}
def load_state(phase_root):
    p=state_path(phase_root); return load_json(p,default_state()) if p.exists() else default_state()
def build_precommit(run_id,p03,permission,price_anchor=None):
    direction=permission.get('direction','UNKNOWN')
    obj={'record_type':'AD_V3_P04_TRUE_FORWARD_PRECOMMIT','run_id':run_id,'created_at_utc':iso(),'subject':'XAUUSD','horizon':p03.get('horizon'),'direction_candidate':direction,'research_action_candidate':permission.get('research_action_candidate'),'expected_signatures':(p03.get('hypotheses') or {}).get('primary',{}).get('expected_signatures',{}),'model_completeness':(p03.get('model_quality') or {}).get('model_completeness'),'missing_driver_risk':(p03.get('model_quality') or {}).get('missing_driver_risk'),'price_anchor':price_anchor,'outcome_status':'PENDING' if direction in ('BULLISH_GOLD','BEARISH_GOLD') else 'NOT_DIRECTIONAL','immutable_precommit':True}
    obj['precommit_id']=stable_id('P04PRE',obj); return obj

def _marker(a):
    if not a:return None
    return a.get('economic_marker') or a.get('reference_period') or a.get('event_time') or a.get('published_at') or a.get('retrieved_at')

def _append_outcome(phase_root,o):
    p=outcomes_path(phase_root); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a',encoding='utf-8') as f: f.write(json.dumps(o,ensure_ascii=False,separators=(',',':'))+'\n')

def update(phase_root,precommit,current_price_anchor=None):
    st=load_state(phase_root); pending=[]
    for old in st.get('pending',[]):
        d=old.get('direction'); pa=old.get('price_anchor')
        if d not in ('BULLISH_GOLD','BEARISH_GOLD'):
            continue
        if not pa or not current_price_anchor or not isinstance(pa.get('value'),(int,float)) or not isinstance(current_price_anchor.get('value'),(int,float)):
            pending.append(old); continue
        om=_marker(pa); cm=_marker(current_price_anchor)
        if not om or not cm or str(om)==str(cm):
            pending.append(old); continue
        delta=float(current_price_anchor['value'])-float(pa['value'])
        sign='UP' if delta>0 else 'DOWN' if delta<0 else 'FLAT'
        aligned=(d=='BULLISH_GOLD' and sign=='UP') or (d=='BEARISH_GOLD' and sign=='DOWN')
        outcome='ALIGNED' if aligned else 'FLAT' if sign=='FLAT' else 'OPPOSED'
        o={'record_type':'AD_V3_P04_TRUE_FORWARD_OUTCOME','evaluated_at_utc':iso(),'precommit_id':old.get('precommit_id'),'run_id':old.get('run_id'),'direction_candidate':d,'anchor':pa,'outcome_anchor':current_price_anchor,'price_delta':delta,'outcome':outcome,'historical_precommit_rewritten':False}
        o['outcome_id']=stable_id('P04OUT',o); _append_outcome(phase_root,o)
        st['outcomes_evaluated']=int(st.get('outcomes_evaluated',0))+1
        key={'ALIGNED':'aligned_outcomes','OPPOSED':'opposed_outcomes','FLAT':'flat_outcomes'}[outcome]; st[key]=int(st.get(key,0))+1
    st['pending']=pending
    st['total_capsules']=int(st.get('total_capsules',0))+1
    if precommit.get('direction_candidate') in ('BULLISH_GOLD','BEARISH_GOLD'):
        st['directional_precommits']=int(st.get('directional_precommits',0))+1
        st['pending'].append({'precommit_id':precommit['precommit_id'],'run_id':precommit['run_id'],'direction':precommit.get('direction_candidate'),'price_anchor':precommit.get('price_anchor')})
    st['sample_state']=_sample_state(int(st.get('outcomes_evaluated',0))); st['promotion_ready']=st['sample_state']=='PROVISIONAL' and int(st.get('integrity_failures',0))==0; st['updated_at_utc']=iso(); write_json(state_path(phase_root),st); return st
