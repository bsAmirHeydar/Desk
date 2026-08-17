from __future__ import annotations
from .common import parse_dt

SUCCESS={'OBSERVED_CURRENT','OBSERVED_DELAYED','LATEST_VALID','RELEASE_NOT_DUE','PUBLIC_PROXY','MODEL_DERIVED'}

def economic_marker(obs,policy):
    for k in policy.get('explicit_economic_marker_order') or ['reference_period','event_time','published_at']:
        v=obs.get(k)
        if v not in (None,''): return {'kind':k,'value':str(v),'dt':parse_dt(v)}
    return None

def classify_observation(obs,source,fact_tier,source_action,horizon,as_of_utc,policy):
    state=(obs or {}).get('epistemic_state')
    warnings=(obs or {}).get('warnings') or []
    if state=='PRIVATE_UNOBSERVABLE': return {'state':'PRIVATE_GAP','economic_time_quality':'UNAVAILABLE','reason':'PRIVATE_UNOBSERVABLE'}
    if state=='PAID_ONLY': return {'state':'PAID_GAP','economic_time_quality':'UNAVAILABLE','reason':'PAID_OR_LICENSED'}
    if state=='UNKNOWN_TRUE' and 'PUBLIC_OR_PROVIDER_GAP_NO_CANONICAL_FREE_DIRECT_SOURCE' in warnings:
        return {'state':'PROVIDER_GAP','economic_time_quality':'UNAVAILABLE','reason':'PROVIDER_GAP'}
    if state not in SUCCESS: return {'state':'UNAVAILABLE','economic_time_quality':'UNKNOWN','reason':state or 'MISSING'}
    asof=parse_dt(as_of_utc); marker=economic_marker(obs,policy); live_cad=set(policy.get('fetch_only_live_cadences') or [])
    cadence=(source or {}).get('cadence')
    # Explicit economic clocks dominate the fetch clock.
    if marker and marker.get('dt') and asof:
        if marker['dt']>asof: return {'state':'UNAVAILABLE','economic_time_quality':'FUTURE_FORBIDDEN','reason':'FUTURE_ECONOMIC_MARKER','economic_marker':marker}
        age=(asof-marker['dt']).total_seconds(); maxage=int((policy.get('live_marker_max_age_seconds') or {}).get(horizon,21600))
        if fact_tier=='LIVE_KERNEL' and cadence in live_cad:
            return {'state':'FRESH_LIVE' if age<=maxage else 'STALE_FOR_HORIZON','economic_time_quality':'EXPLICIT','reason':'EXPLICIT_MARKER_AGE','age_seconds':age,'economic_marker':marker}
        return {'state':'CONTEXT_VALID','economic_time_quality':'EXPLICIT','reason':'CONTEXT_ECONOMIC_STATE','age_seconds':age,'economic_marker':marker}
    # No explicit economic marker: never call slow official data live merely because it was fetched now.
    if fact_tier=='LIVE_KERNEL' and cadence in live_cad and source_action in ('LIVE_FETCH','ESCALATION_FETCH','FIXTURE_NETWORK'):
        return {'state':'FRESH_FOR_HORIZON','economic_time_quality':'IMPLICIT_SOURCE_CLOCK','reason':'LIVE_OR_EVENT_SOURCE_REFRESHED_NO_EXPLICIT_MARKER'}
    if fact_tier=='LIVE_KERNEL':
        return {'state':'CONTEXT_VALID','economic_time_quality':'UNKNOWN','reason':'LIVE_FACT_ONLY_SLOW_CONTEXT_SOURCE'}
    return {'state':'CONTEXT_VALID','economic_time_quality':'UNKNOWN','reason':'CONTEXT_SOURCE_NO_EXPLICIT_MARKER'}
