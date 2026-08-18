from __future__ import annotations
from datetime import datetime,timedelta,timezone

def make_state(n=100,mode='good'):
    state={'record_type':'AD_V3_P09_FORWARD_STATE','schema_version':'1.0.0','updated_at_utc':'2026-01-01T00:00:00Z','predictions':[],'outcomes':[],'episodes':[],'cohorts':[{'cohort_id':'COHORT_001','state':'OPEN','fingerprint':'TEST'}],'market_observations':[],'integrity_failures':0,'test_fixture_samples_included':False}
    base=datetime(2026,1,2,tzinfo=timezone.utc)
    for i in range(n):
        t=(base+timedelta(hours=8*i)).isoformat().replace('+00:00','Z');mt=(base+timedelta(hours=8*i+6)).isoformat().replace('+00:00','Z')
        bull=(i%2==0);action=(i%2==0 or i%4==1)  # ~75% action, enough WAIT too
        # For balanced action subgroups, override every fourth to WAIT.
        if i%4==3: action=False
        perm=('BUY_CANDIDATE' if bull else 'SELL_CANDIDATE') if action else 'WAIT'
        edge='ACTIONABLE_EDGE' if action else 'NO_EDGE'
        event='EVENT_EXPOSED' if i%4==0 else 'EVENT_FREE'
        vol=[0.003,0.006,0.012][i%3]
        root=['REAL_RATE_OPPORTUNITY_COST','US_POLICY_EXPECTATIONS','USD_AUTONOMOUS','INVESTMENT_ALLOCATION_DEMAND'][i%4]
        dom=('BULLISH_DOMINANT' if bull else 'BEARISH_DOMINANT') if i%3 else ('BULLISH_FRAGILE' if bull else 'BEARISH_FRAGILE')
        strength=['WEAK','MODERATE','STRONG','DOMINANT'][i%4]
        cons='HIGH' if i%5==0 else 'LOW';frag='HIGH' if i%6==0 else 'LOW'
        if mode=='bad_coverage':
            event='EVENT_FREE';vol=0.006;root='REAL_RATE_OPPORTUNITY_COST'
        pred={'prediction_id':f'P{i}','episode_id':f'E{i}','cohort_id':'COHORT_001','eligibility':'VALIDATION_ELIGIBLE','causal_direction':'BULLISH_GOLD' if bull else 'BEARISH_GOLD','pressure_strength':strength,'dominance_state':dom,'dominant_root':root,'edge_state':edge,'permission_candidate':perm,'consumption':cons,'fragility':frag,'semantic_mode':'AUTO_GOVERNED','data_health':'ALLOW','volatility_reference':vol,'precommit_time':t,'maturity_time':mt}
        dout='ALIGNED';pq='CLEAN' if action else 'NO_MEANINGFUL_EDGE';po='SUPPORTED' if action else 'NEUTRAL';wo=None if action else ('WAIT_PROTECTED' if i%3 else 'WAIT_APPROPRIATE_UNCERTAINTY');mfe=0.012 if action else 0.002;mae=0.001;band=0.002
        if mode=='bad_quality':
            dout='OPPOSED';pq='ADVERSE' if action else 'CLEAN';po='OPPOSED' if action else 'NEUTRAL';wo=None if action else 'WAIT_MISSED_OPPORTUNITY';mfe=0.001;mae=0.010
        if mode=='bad_subgroup' and action and not bull and (i%16 in (1,5,9)):
            # enough bearish permission failures to exceed subgroup threshold, while aggregate action quality remains acceptable.
            pq='ADVERSE';po='OPPOSED';mfe=0.001;mae=0.010
        out={'prediction_id':f'P{i}','outcome_id':f'O{i}','episode_id':f'E{i}','cohort_id':'COHORT_001','direction_outcome':dout,'permission_outcome':po,'wait_outcome':wo,'path_quality':pq,'path_coverage':{'path_metric_authority':'AVAILABLE','actual_points':12,'expected_min_points':8},'mfe_return':mfe,'mae_return':mae,'neutral_band_return':band,'terminal_return':0.01 if dout=='ALIGNED' else -0.01,'event_exposure':event}
        ep={'episode_id':f'E{i}','cohort_id':'COHORT_001','state':'CLOSED','start_time':t,'primary_prediction_id':f'P{i}','prediction_ids':[f'P{i}']}
        state['predictions'].append(pred);state['outcomes'].append(out);state['episodes'].append(ep)
    return state
