from __future__ import annotations
from .common import cfg

def _match(p,o,sel):
    mapping={'permission':p.get('permission_candidate'),'event_exposure':o.get('event_exposure'),'semantic_mode':p.get('semantic_mode'),'fragility':p.get('fragility'),'data_health':p.get('data_health')}
    return all(mapping.get(k) in vals for k,vals in sel.items())
def evaluate(rows):
    pol=cfg('critical_subgroup_policy.json');mult=float(pol['severe_adverse_multiple_of_neutral_band']);reports=[];critical=[]
    for g in pol['critical_groups']:
        z=[(p,o) for p,o,e in rows if _match(p,o,g['selector'])];n=len(z);opp=sum(1 for p,o in z if o.get('direction_outcome')=='OPPOSED');sev=0
        for p,o in z:
            band=o.get('neutral_band_return') or 0;mae=o.get('mae_return')
            if isinstance(mae,(int,float)) and band>0 and mae/band>=mult:sev+=1
        orate=opp/n if n else None;srate=sev/n if n else None;evaluable=n>=g['min_n'];fail=bool(evaluable and ((orate or 0)>g['max_opposed_rate'] or (srate or 0)>g['max_severe_adverse_rate']))
        r={'group_id':g['id'],'n':n,'evaluable':evaluable,'opposed_rate':orate,'severe_adverse_rate':srate,'state':'FAIL' if fail else ('PASS' if evaluable else 'INSUFFICIENT')};reports.append(r)
        if fail:critical.append(g['id'])
    return {'state':'FAIL' if critical else 'PASS','critical_failures':critical,'groups':reports,'overall_average_cannot_override':True}
