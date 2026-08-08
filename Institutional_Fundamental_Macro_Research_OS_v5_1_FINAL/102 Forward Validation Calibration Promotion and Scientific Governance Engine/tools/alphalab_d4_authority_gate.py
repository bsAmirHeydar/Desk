#!/usr/bin/env python3
import argparse,json,hashlib,datetime
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--registry',required=True);a=p.parse_args();inp=json.loads(Path(a.input).read_text());regp=Path(a.registry);reg=json.loads(regp.read_text());fund=inp.get('fundamental_direction');base=inp.get('v19_d3_permission',inp.get('pre_d4_permission'));final=base;applied=[];shadow=[];reasons=[];effects=[];conflicts=[];caps=list(inp.get('confidence_caps') or []);validity=inp.get('validity_action','KEEP_BASE')
def parse_dt(s):
    if not s:return None
    try:return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
    except:return None
asof=parse_dt(inp.get('analysis_cutoff_utc'))
def scope_match(rec):
    s=rec.get('scope') or {};tests=[('instruments',inp.get('instrument')),('horizons',inp.get('active_strategy_horizon')),('sessions',inp.get('session')),('regimes',inp.get('regime')),('fundamental_directions',fund),('evidence_grades',inp.get('evidence_grade')),('execution_profiles',inp.get('execution_profile'))]
    for key,val in tests:
        allowed=s.get(key)
        if allowed and val not in allowed:return False
    ex=parse_dt(rec.get('expires_at_utc'));act=parse_dt(rec.get('activated_at_utc'))
    if asof and act and asof<act:return False
    if asof and ex and asof>=ex:return False
    return True
def specificity(rec):
    s=rec.get('scope') or {};return sum(1 for k in ['instruments','horizons','sessions','regimes','fundamental_directions','evidence_grades','execution_profiles'] if s.get(k))
prec={'CAPACITY_BLOCK':100,'SUPPRESS_PERMISSION':90,'DELAY_PERMISSION':80,'VALIDITY_SHORTEN':70,'CONFIDENCE_CAP':60,'RESTORE_EXISTING_DIRECTION_PERMISSION':50,'CREATE_PERMISSION_WITH_EXISTING_FUNDAMENTAL_DIRECTION':40,'REPORT_ONLY':10}
matched=[]
for c in inp.get('promotion_candidates',[]):
    mid=c.get('modifier_id');ms=[x for x in reg.get('records',[]) if x.get('modifier_id')==mid and x.get('status')=='ACTIVE' and scope_match(x)]
    if not ms:shadow.append(mid);continue
    ms=sorted(ms,key=lambda z:(specificity(z),prec.get(z.get('authority_class'),0),str(z.get('activated_at_utc') or '')),reverse=True)
    if len(ms)>1 and specificity(ms[0])==specificity(ms[1]) and prec.get(ms[0].get('authority_class'),0)==prec.get(ms[1].get('authority_class'),0):conflicts.append({'modifier_id':mid,'promotion_ids':[m.get('promotion_id') for m in ms[:2]],'resolution':'LATEST_ACTIVATION_AFTER_EQUAL_SPECIFICITY_AND_PRECEDENCE'})
    matched.append((c,ms[0]))
# Apply risk-reducing/constraint authorities first. Positive authorities never override a matched hard constraint.
matched=sorted(matched,key=lambda z:(prec.get(z[1].get('authority_class'),0),specificity(z[1])),reverse=True)
hard_block=False
for c,x in matched:
    cls=x.get('authority_class');pid=x.get('promotion_id');proposed=c.get('proposed_permission');ep=x.get('effect_parameters') or {}
    if cls in {'CAPACITY_BLOCK','SUPPRESS_PERMISSION','DELAY_PERMISSION'}:
        if proposed=='NO_TRADE' or cls in {'CAPACITY_BLOCK','SUPPRESS_PERMISSION'}:
            final='NO_TRADE';hard_block=True;applied.append(pid);effects.append({'promotion_id':pid,'authority_class':cls,'effect':'NO_TRADE'})
    elif cls=='CONFIDENCE_CAP':
        label=ep.get('cap_label') or c.get('cap_label') or ('PROMOTION_'+str(pid))
        if label not in caps:caps.append(label)
        applied.append(pid);effects.append({'promotion_id':pid,'authority_class':cls,'effect':'CONFIDENCE_CAP','label':label})
    elif cls=='VALIDITY_SHORTEN':
        proposed_validity=ep.get('validity_action') or c.get('proposed_validity_action') or 'SHORTEN_MODERATE'
        validity=proposed_validity;applied.append(pid);effects.append({'promotion_id':pid,'authority_class':cls,'effect':'VALIDITY_SHORTEN','validity_action':validity})
    elif cls in {'RESTORE_EXISTING_DIRECTION_PERMISSION','CREATE_PERMISSION_WITH_EXISTING_FUNDAMENTAL_DIRECTION'}:
        if hard_block:reasons.append(str(c.get('modifier_id'))+': positive authority suppressed by higher-precedence risk constraint');continue
        if fund not in {'BULLISH','BEARISH'}:reasons.append(str(c.get('modifier_id'))+': fundamental direction guard');continue
        expected='BUY' if fund=='BULLISH' else 'SELL'
        if proposed!=expected:reasons.append(str(c.get('modifier_id'))+': proposed permission conflicts with fundamental');continue
        final=proposed;applied.append(pid);effects.append({'promotion_id':pid,'authority_class':cls,'effect':'PERMISSION','permission':final})
    else:
        applied.append(pid);effects.append({'promotion_id':pid,'authority_class':cls,'effect':'REPORT_ONLY'})
# Final guard: never flip fundamental direction via permission.
if fund=='BULLISH' and final=='SELL':final='NO_TRADE';reasons.append('final permission flip guard')
if fund=='BEARISH' and final=='BUY':final='NO_TRADE';reasons.append('final permission flip guard')
receipt={'registry_version':reg.get('version'),'registry_sha256':hashlib.sha256(regp.read_bytes()).hexdigest(),'fundamental_direction':fund,'v19_d3_permission':base,'final_v20_permission':final,'final_permission':final,'applied_promotion_ids':applied,'applied_rule_effects':effects,'shadow_candidate_ids':shadow,'fail_closed_reasons':reasons,'conflicts_resolved':conflicts,'confidence_caps':sorted(caps),'validity_action':validity}
print(json.dumps(receipt,indent=2))
