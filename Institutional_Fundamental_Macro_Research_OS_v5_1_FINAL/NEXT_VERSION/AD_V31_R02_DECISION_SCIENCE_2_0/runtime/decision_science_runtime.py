from __future__ import annotations
import time
from .magnitude_engine import root_magnitude
from .root_health_engine import assess as assess_health
from .causal_importance_engine import infer_regime,importance
from .sensitivity_engine import evaluate as sensitivity

def enrich_roots(p03,roots,rows_by_root,expected_by_root,freshness_by_fact,contract_map,history=None,kernel=None,explicit_regime=None):
    t0=time.perf_counter();reg=infer_regime(p03,kernel,explicit_regime);out=[];mag_ms=health_ms=imp_ms=0.0
    for root0 in roots:
        root=dict(root0);rid=root['root_id'];rr=rows_by_root.get(rid,[])
        tm=time.perf_counter();mag=root_magnitude(root,[r for r in rr if r.get('fact_id') in set(root.get('evidence_fact_ids') or [])],history,p03.get('generated_at_utc') or p03.get('decision_time'));mag_ms+=(time.perf_counter()-tm)*1000
        fmap={x['fact_id']:x for x in mag.get('fact_magnitudes',[])}
        th=time.perf_counter();health=assess_health(rid,expected_by_root.get(rid,[]),rr,freshness_by_fact,contract_map,fmap,root.get('direction','UNKNOWN'));health_ms+=(time.perf_counter()-th)*1000
        ti=time.perf_counter();imp=importance(rid,p03.get('horizon','SESSION_1_6H'),reg);imp_ms+=(time.perf_counter()-ti)*1000
        root.update({'magnitude':mag['state'],'magnitude_source':mag['source'],'magnitude_temporal_role':mag.get('temporal_role'),'magnitude_fact_states':mag.get('fact_magnitudes',[]),'normalized_magnitude_fact_count':mag.get('normalized_fact_count',0),'root_health':health,'freshness':health['freshness_summary'],'evidence_quality':health['evidence_quality_summary'],'causal_importance':imp['state'],'importance_basis':imp,'regime_context':reg})
        out.append(root)
    return out,{'magnitude_ms':round(mag_ms,3),'root_health_ms':round(health_ms,3),'importance_ms':round(imp_ms,3),'enrichment_total_ms':round((time.perf_counter()-t0)*1000,3),'regime_context':reg}
def reconcile(roots):
    t=time.perf_counter();r=sensitivity(roots);r['timing_ms']=round((time.perf_counter()-t)*1000,3);return r
