import json
from .timeutil import utc_now
from .canonical import dump_json

class LifecycleError(RuntimeError): pass

class Lifecycle:
    def __init__(self,store,catalog,policy): self.store=store; self.catalog=catalog; self.policy=policy
    def transition(self,run_id,to_state,event_type="STATE_TRANSITION",details=None):
        m=self.store.load_manifest(run_id); cur=m['state']; allowed=self.policy['allowed_transitions'].get(cur,[])
        if to_state not in allowed: raise LifecycleError(f"illegal transition {cur} -> {to_state}")
        now=utc_now(); run=self.catalog.get_run(run_id)
        with self.store._lock(run_id):
            with self.catalog.connect() as c:
                seq=c.execute("SELECT COALESCE(MAX(sequence),0)+1 FROM run_events WHERE run_id=?",(run_id,)).fetchone()[0]
                c.execute("INSERT INTO run_events(run_id,sequence,event_type,from_state,to_state,occurred_at_utc,details_json) VALUES(?,?,?,?,?,?,?)",(run_id,seq,event_type,cur,to_state,now,json.dumps(details or {},ensure_ascii=False,sort_keys=True)))
                c.execute("UPDATE runs SET state=?, manifest_revision=manifest_revision+1, updated_at_utc=? WHERE run_id=?",(to_state,now,run_id))
            m['state']=to_state; m['manifest_revision']=int(m['manifest_revision'])+1; m['updated_at_utc']=now; self.store.write_manifest(m); self._append_event(m,seq,event_type,cur,to_state,now,details or {})
        return m
    def event(self,run_id,event_type,details=None):
        m=self.store.load_manifest(run_id); now=utc_now(); run=self.catalog.get_run(run_id)
        with self.store._lock(run_id):
            with self.catalog.connect() as c:
                seq=c.execute("SELECT COALESCE(MAX(sequence),0)+1 FROM run_events WHERE run_id=?",(run_id,)).fetchone()[0]
                c.execute("INSERT INTO run_events(run_id,sequence,event_type,from_state,to_state,occurred_at_utc,details_json) VALUES(?,?,?,?,?,?,?)",(run_id,seq,event_type,None,None,now,json.dumps(details or {},ensure_ascii=False,sort_keys=True)))
            self._append_event(m,seq,event_type,None,None,now,details or {})
        return seq
    def _append_event(self,m,seq,event_type,frm,to,now,details):
        p=self.store.run_dir(m)/"meta"/"events.jsonl"; e={"schema_version":"1.0.0","run_id":m['run_id'],"sequence":seq,"event_type":event_type,"from_state":frm,"to_state":to,"occurred_at_utc":now,"details":details};
        with open(p,"a",encoding="utf-8",newline="\n") as f: f.write(json.dumps(e,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n")
