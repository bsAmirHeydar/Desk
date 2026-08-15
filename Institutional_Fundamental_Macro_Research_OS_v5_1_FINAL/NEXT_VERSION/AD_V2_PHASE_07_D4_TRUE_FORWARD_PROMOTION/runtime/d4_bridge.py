#!/usr/bin/env python3
from __future__ import annotations
PHASE='AD-V2-P07'
def forward_observation(commitment):
    f=commitment.get('features') or {}
    d='BULLISH' if f.get('pressure_sign')=='BUY' else 'BEARISH' if f.get('pressure_sign')=='SELL' else 'UNRESOLVED'
    return {'record_type':'FORWARD_OBSERVATION','run_id':commitment['run_id'],'analysis_id':commitment['commitment_id'],'instrument':'XAUUSD','analysis_cutoff_utc':commitment['analysis_cutoff_utc'],'vault_commit':'V2_SIDE_CAR','prompt_sha256':'V2_SIDE_CAR','state_sha256':commitment['p06_state_hash'],'registry_version':'AD-V2-P07','fundamental_direction':d,'v19_d3_permission':f.get('v1_permission') or 'NO_TRADE','final_v20_permission':f.get('v1_permission') or 'NO_TRADE','execution_profile_version':'V1_INHERITED','independent_root_ids':commitment.get('dominant_root_ids',[]),'metadata':{'p07_commitment_id':commitment['commitment_id'],'sample_provenance':commitment['sample_provenance'],'write_to_v1_d4_ledger':False}}
def d4_outcome(outcome_link):
    m=outcome_link.get('metrics') or {};return {'record_type':'OUTCOME','outcome_id':outcome_link['outcome_link_id'],'run_id':outcome_link['run_id'],'maturity_state':outcome_link['maturity_state'],**{k:v for k,v in m.items() if k in {'realized_r','mfe_r','mae_r','time_to_trigger_seconds','time_to_mfe_seconds','cost_r','exit_reason'}},'metadata':{'p07_commitment_id':outcome_link['commitment_id'],'write_to_v1_d4_ledger':False}}
