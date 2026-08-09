from pathlib import Path
import json,importlib.util
from .util import now,dump_json
class Warehouse:
    def __init__(self,vault,rt):self.vault=Path(vault);self.rt=rt
    def upsert_run(self,run_id):
        m=self.rt.store.load_manifest(run_id);get=lambda n: self._get(run_id,n)
        fp=get('final_permission') or {};ri=get('research_intent') or {};fs=get('fundamental_state') or {};reg=get('regime_state') or {};ca=get('cognitive_adjudication') or {};out=get('d4_outcome') or {}
        roots=[]
        d3=get('d3_adjudication') or {};roots=d3.get('deduplicated_root_ids') or []
        row={'schema_version':'1.0.0','run_id':run_id,'instrument':m['subject'],'run_mode':m['run_mode'],'analysis_cutoff_utc':m['analysis_cutoff_utc'],'decision_seal_hash':m.get('decision_seal_hash') or '', 'permission':fp.get('permission'),'fundamental_direction':ri.get('fundamental_direction') or fs.get('direction'),'edge_state':ri.get('edge_state'),'active_horizon':ri.get('active_horizon'),'execution_profile':(get('run_request') or {}).get('execution_profile'),'outcome_state':out.get('maturity_state'),'realized_r':out.get('realized_r'),'mfe_r':out.get('mfe_r'),'mae_r':out.get('mae_r'),'cost_r':out.get('cost_r'),'independent_root_ids':roots,'regime_state':reg.get('overall_state') or reg.get('state'),'complexity_class':ca.get('complexity_class'),'unmodeled_driver_risk':ca.get('unmodeled_driver_risk'),'abstention_reason_codes':ca.get('abstention_reason_codes') or [],'updated_at_utc':now()}
        with self.rt.catalog.connect() as c:c.execute("INSERT OR REPLACE INTO r3_analytics_rows(run_id,instrument,run_mode,analysis_cutoff_utc,analysis_date,decision_seal_hash,permission,fundamental_direction,edge_state,active_horizon,execution_profile,outcome_state,realized_r,mfe_r,mae_r,cost_r,regime_state,complexity_class,unmodeled_driver_risk,independent_root_ids_json,abstention_reason_codes_json,updated_at_utc) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(run_id,row['instrument'],row['run_mode'],row['analysis_cutoff_utc'],row['analysis_cutoff_utc'][:10],row['decision_seal_hash'],row['permission'],row['fundamental_direction'],row['edge_state'],row['active_horizon'],row['execution_profile'],row['outcome_state'],row['realized_r'],row['mfe_r'],row['mae_r'],row['cost_r'],row['regime_state'],row['complexity_class'],row['unmodeled_driver_risk'],json.dumps(roots),json.dumps(row['abstention_reason_codes']),row['updated_at_utc']))
        return row
    def _get(self,run_id,n):
        try:return self.rt.store.load_artifact_json(run_id,n)
        except Exception:return None
    def query(self,where='1=1',params=()):
        with self.rt.catalog.connect() as c:
            c.row_factory=__import__('sqlite3').Row;return [dict(x) for x in c.execute('SELECT * FROM r3_analytics_rows WHERE '+where,params).fetchall()]
    def export_jsonl(self):
        rows=self.query(); root=self.rt.data_root/'warehouse'/'jsonl';root.mkdir(parents=True,exist_ok=True);p=root/'runs.jsonl'
        with open(p,'w',encoding='utf-8',newline='\n') as f:
            for r in rows:f.write(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
        return str(p),len(rows)

    def counterfactual_summary(self,instrument=None,branch=None):
        sql='SELECT c.branch,c.score_state,c.realized_r,a.instrument,a.realized_r AS actual_r FROM r3_counterfactuals c JOIN r3_analytics_rows a ON a.run_id=c.run_id WHERE 1=1';params=[]
        if instrument:sql+=' AND a.instrument=?';params.append(instrument)
        if branch:sql+=' AND c.branch=?';params.append(branch)
        with self.rt.catalog.connect() as c:
            c.row_factory=__import__('sqlite3').Row;rows=[dict(x) for x in c.execute(sql,params).fetchall()]
        scored=[x for x in rows if x.get('realized_r') is not None and x.get('actual_r') is not None]
        return {'rows':len(rows),'scored_pairs':len(scored),'mean_counterfactual_r':(sum(x['realized_r'] for x in scored)/len(scored) if scored else None),'mean_actual_r':(sum(x['actual_r'] for x in scored)/len(scored) if scored else None),'mean_delta_r':(sum(x['realized_r']-x['actual_r'] for x in scored)/len(scored) if scored else None)}

    def accelerator_status(self):return {'duckdb':bool(importlib.util.find_spec('duckdb')),'pyarrow':bool(importlib.util.find_spec('pyarrow')),'canonical_backend':'SQLITE','precision_loss_if_unavailable':False}
