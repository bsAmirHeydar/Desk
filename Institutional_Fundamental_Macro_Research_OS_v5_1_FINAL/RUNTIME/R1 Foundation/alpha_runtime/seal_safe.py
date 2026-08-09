from .canonical import sha256_obj
import json
from .timeutil import utc_now

class SealError(RuntimeError): pass

def _decision_rows(catalog,store,run_id):
    rows=[]
    for r in catalog.list_artifacts(run_id,'DECISION'):
        if r['logical_name']=='decision_seal_payload': continue
        b=store.objects.get_bytes(r['artifact_hash']); rows.append({"logical_name":r['logical_name'],"stage":r['stage'],"artifact_hash":r['artifact_hash'],"byte_length":len(b)})
    return sorted(rows,key=lambda x:(x['stage'],x['logical_name']))

def create_decision_seal(run_id,rt):
    store,catalog,lifecycle=rt.store,rt.catalog,rt.lifecycle; m=store.load_manifest(run_id)
    if m['state']!='COGNITION_FROZEN': raise SealError('decision seal requires COGNITION_FROZEN')
    rows=_decision_rows(catalog,store,run_id)
    with catalog.connect() as c: next_seq=c.execute("SELECT COALESCE(MAX(sequence),0)+1 FROM run_events WHERE run_id=?",(run_id,)).fetchone()[0]
    payload={"schema_version":"1.0.0","run_id":run_id,"analysis_cutoff_utc":m['analysis_cutoff_utc'],"request_fingerprint":m['request_fingerprint'],"run_fingerprint":m.get('run_fingerprint'),"runtime_version":m['runtime_version'],"vault_stack":m['vault_stack'],"vault_commit":m.get('vault_commit'),"snapshot_manifest_hash":m.get('snapshot_manifest_hash'),"decision_artifacts":rows,"event_sequence_at_freeze":next_seq,"sealed_at_utc":utc_now()}
    basis=dict(payload); basis.pop('sealed_at_utc'); payload['decision_root_hash']=sha256_obj(basis)
    # transition before setting seal hash so the event is the freeze event described by payload
    m=lifecycle.transition(run_id,'DECISION_FROZEN','DECISION_SEALED',{"decision_root_hash":payload['decision_root_hash']})
    # store seal as META to avoid self-referential decision-world set
    ref=store.put_artifact(run_id,'decision_seal_payload','META','META',payload,'application/json',producer_process_id='R1_SEALER',producer_version='R1.0.0')
    m=store.load_manifest(run_id); m['decision_seal_hash']=payload['decision_root_hash']; m['manifest_revision']+=1; m['updated_at_utc']=utc_now(); store.write_manifest(m)
    with catalog.connect() as c:
        c.execute("UPDATE runs SET decision_seal_hash=?,manifest_revision=?,updated_at_utc=? WHERE run_id=?",(payload['decision_root_hash'],m['manifest_revision'],m['updated_at_utc'],run_id)); c.execute("INSERT OR REPLACE INTO seals(run_id,seal_type,seal_hash,artifact_hash,created_at_utc) VALUES(?,?,?,?,?)",(run_id,'DECISION',payload['decision_root_hash'],ref['artifact_hash'],payload['sealed_at_utc'])); c.execute("UPDATE run_artifacts SET immutable=1 WHERE run_id=? AND world='DECISION'",(run_id,))
    return payload

def verify_decision_seal(run_id,rt):
    store,catalog=rt.store,rt.catalog; m=store.load_manifest(run_id); expected=m.get('decision_seal_hash')
    if not expected: raise SealError('decision seal missing')
    p=store.load_artifact_json(run_id,'decision_seal_payload'); rows=_decision_rows(catalog,store,run_id)
    if rows!=p['decision_artifacts']: raise SealError('decision artifact set drift')
    for r in catalog.list_artifacts(run_id,'DECISION'):
        refp=store.root/r['ref_relpath']
        if not refp.is_file(): raise SealError('decision artifact ref missing')
        ref=json.loads(refp.read_text(encoding='utf-8'))
        if ref.get('artifact_hash')!=r['artifact_hash'] or ref.get('logical_name')!=r['logical_name'] or ref.get('world')!='DECISION' or ref.get('stage')!=r['stage']:
            raise SealError('decision artifact ref/catalog mismatch')
    basis=dict(p); basis.pop('decision_root_hash',None); basis.pop('sealed_at_utc',None)
    if sha256_obj(basis)!=expected: raise SealError('decision seal hash mismatch')
    return True


def create_close_seal(run_id,rt):
    store,catalog,lifecycle=rt.store,rt.catalog,rt.lifecycle
    m=store.load_manifest(run_id)
    if not m.get('decision_seal_hash'): raise SealError('decision seal required')
    if m.get('run_close_seal_hash'): raise SealError('run already close-sealed')
    if m['state']!='CLOSED':
        allowed=rt.lifecycle_policy['allowed_transitions'].get(m['state'],[])
        if 'CLOSED' not in allowed: raise SealError('run not close-eligible')
        m=lifecycle.transition(run_id,'CLOSED','RUN_CLOSING',{})
    out=[]
    for world in ('OUTCOME','LEARNING'):
        rows=[]
        for r in catalog.list_artifacts(run_id,world):
            b=store.objects.get_bytes(r['artifact_hash']); rows.append({"logical_name":r['logical_name'],"stage":r['stage'],"artifact_hash":r['artifact_hash'],"byte_length":len(b)})
        rows=sorted(rows,key=lambda x:(x['stage'],x['logical_name']))
        if world=='OUTCOME': out_rows=rows
        else: learn_rows=rows
    payload={"schema_version":"1.0.0","run_id":run_id,"decision_root_hash":m['decision_seal_hash'],"terminal_state":"CLOSED","outcome_artifacts":out_rows,"learning_artifacts":learn_rows,"closed_at_utc":utc_now()}
    basis=dict(payload); basis.pop('closed_at_utc'); payload['run_close_hash']=sha256_obj(basis)
    ref=store.put_artifact(run_id,'run_close_seal_payload','META','META',payload,'application/json',producer_process_id='R1_SEALER',producer_version='R1.0.0')
    m=store.load_manifest(run_id); m['run_close_seal_hash']=payload['run_close_hash']; m['manifest_revision']+=1; m['updated_at_utc']=utc_now(); store.write_manifest(m)
    with catalog.connect() as c:
        c.execute("UPDATE runs SET run_close_seal_hash=?,manifest_revision=?,updated_at_utc=? WHERE run_id=?",(payload['run_close_hash'],m['manifest_revision'],m['updated_at_utc'],run_id)); c.execute("INSERT OR REPLACE INTO seals(run_id,seal_type,seal_hash,artifact_hash,created_at_utc) VALUES(?,?,?,?,?)",(run_id,'CLOSE',payload['run_close_hash'],ref['artifact_hash'],payload['closed_at_utc'])); c.execute("UPDATE run_artifacts SET immutable=1 WHERE run_id=? AND world IN ('OUTCOME','LEARNING')",(run_id,))
    return payload

def verify_close_seal(run_id,rt):
    store,catalog=rt.store,rt.catalog; m=store.load_manifest(run_id); expected=m.get('run_close_seal_hash')
    if not expected: raise SealError('run close seal missing')
    p=store.load_artifact_json(run_id,'run_close_seal_payload')
    def rows(world):
        z=[]
        for r in catalog.list_artifacts(run_id,world):
            b=store.objects.get_bytes(r['artifact_hash']); z.append({"logical_name":r['logical_name'],"stage":r['stage'],"artifact_hash":r['artifact_hash'],"byte_length":len(b)})
        return sorted(z,key=lambda x:(x['stage'],x['logical_name']))
    if rows('OUTCOME')!=p['outcome_artifacts'] or rows('LEARNING')!=p['learning_artifacts']: raise SealError('close-sealed artifact set drift')
    basis=dict(p); basis.pop('run_close_hash',None); basis.pop('closed_at_utc',None)
    if sha256_obj(basis)!=expected: raise SealError('run close hash mismatch')
    return True
