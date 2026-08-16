import json,pathlib
P=pathlib.Path(__file__).resolve().parents[1]
fr=json.loads((P/'config/fact_acquisition_registry.json').read_text()); sr=json.loads((P/'config/source_contract_registry.json').read_text()); h=json.loads((P/'PHASE_02_HANDOFF.json').read_text())
print(json.dumps({'phase':'AD-V3-P02','deployment':h['deployment'],'facts':fr['contract_count'],'sources':sr['source_count'],'mandatory_attempt_contracts':h['mandatory_public_fact_attempt_contracts'],'direction_authority':False,'trade_permission_authority':False},indent=2))
