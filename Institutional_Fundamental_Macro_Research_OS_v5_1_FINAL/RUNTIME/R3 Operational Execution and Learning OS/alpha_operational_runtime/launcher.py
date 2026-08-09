from pathlib import Path
import subprocess
from .util import load_json,now,uid

class LaunchError(RuntimeError): pass
SUPPORTED_MODES={'LIVE','SHADOW_LIVE','HISTORICAL_REPLAY','RESEARCH_REPLAY','REPRODUCTION_REPLAY'}
class Launcher:
    def __init__(self,vault,rt):
        self.vault=Path(vault).resolve(); self.rt=rt; self.r3=self.vault/'RUNTIME'/'R3 Operational Execution and Learning OS'
        self.cfg=load_json(self.r3/'config'/'launcher_profiles.json')
    def resolve_instrument(self,s):
        x=str(s).strip().upper(); aliases={k.upper():v for k,v in self.cfg['aliases'].items()}
        if x not in aliases: raise LaunchError('unresolved production instrument alias: '+str(s))
        return aliases[x]
    def vault_commit(self):
        q=subprocess.run(['git','-C',str(self.vault),'rev-parse','HEAD'],capture_output=True,text=True,timeout=10)
        if q.returncode or not q.stdout.strip(): raise LaunchError('production launch requires a resolvable Git commit')
        return q.stdout.strip()
    def compile_request(self,instrument,run_mode='LIVE',analysis_cutoff=None,active_horizon='DAILY_OPEN_TO_CLOSE',coverage_mode=None,research_depth=None,output_depth=None,execution_profile=None,episode_id=None,tags=None,research_program_id=None,strategy_id=None,allow_private_sources=False,idempotency_policy=None):
        inst=self.resolve_instrument(instrument); d=self.cfg['defaults']; mode=run_mode.upper()
        if mode not in SUPPORTED_MODES: raise LaunchError('unsupported run_mode: '+mode)
        if mode in ('LIVE','SHADOW_LIVE'):
            cutoff=analysis_cutoff or 'NOW'
        else:
            if not analysis_cutoff: raise LaunchError(mode+' requires explicit analysis_cutoff')
            cutoff=analysis_cutoff
        return {
          'schema_version':'1.0.0','research_program_id':research_program_id or d['research_program_id'],
          'episode_id':episode_id,'run_scope':'INSTRUMENT','subject':inst,'instrument':inst,'run_mode':mode,
          'analysis_cutoff':cutoff,'strategy_id':strategy_id or d['strategy_id'],'active_horizon':active_horizon,
          'coverage_mode':coverage_mode or d['coverage_mode'],'research_depth':research_depth or d['research_depth'],
          'output_depth':output_depth or d['output_depth'],'lookahead_policy':'STRICT_POINT_IN_TIME',
          'execution_profile':execution_profile or d['execution_profile'],'allow_private_sources':bool(allow_private_sources),
          'idempotency_policy':idempotency_policy or d['idempotency_policy'],'tags':list(tags or [])
        }
    def create(self,**kw):
        req=self.compile_request(**kw); m,reused=self.rt.create_run(req,vault_commit=self.vault_commit())
        return {'launch_id':uid('LAUNCH'),'run_id':m['run_id'],'reused':reused,'request':req,'vault_commit':m.get('vault_commit')}
    def create_request(self,req):
        m,reused=self.rt.create_run(req,vault_commit=self.vault_commit())
        return {'launch_id':uid('LAUNCH'),'run_id':m['run_id'],'reused':reused,'request':req,'vault_commit':m.get('vault_commit')}
    def daily_six_requests(self,run_mode='LIVE',analysis_cutoff=None,active_horizon='DAILY_OPEN_TO_CLOSE',coverage_mode='STRICT_FULL',research_depth='AUTO',execution_profile='PERMISSION_ONLY_V1'):
        # Historical baskets share an exact cutoff. Live baskets intentionally keep NOW per component;
        # exact component cutoffs are frozen after each strict pre-run intake and recorded for meta reconciliation.
        if run_mode.upper() not in ('LIVE','SHADOW_LIVE') and not analysis_cutoff: raise LaunchError('historical daily-six requires analysis_cutoff')
        ep=uid('EP_DAILY6')
        return ep,[self.compile_request(x,run_mode,analysis_cutoff,active_horizon,coverage_mode,research_depth,'FULL',execution_profile,episode_id=ep,tags=['daily-six']) for x in self.cfg['production_instruments']]
    def bulk_requests(self,instrument,cutoffs,run_mode='HISTORICAL_REPLAY',active_horizon='DAILY_OPEN_TO_CLOSE',coverage_mode='STRICT_FULL',research_depth='AUTO'):
        mode=run_mode.upper()
        if mode in ('LIVE','SHADOW_LIVE'): raise LaunchError('bulk historical planner does not accept live mode')
        out=[]
        for i,cut in enumerate(cutoffs):
            out.append(self.compile_request(instrument,mode,cut,active_horizon,coverage_mode,research_depth,'MACHINE','PERMISSION_ONLY_V1',tags=['bulk-replay','bulk-index:'+str(i)]))
        return {'schema_version':'1.0.0','plan_id':uid('BULK'),'instrument':self.resolve_instrument(instrument),'run_mode':mode,'count':len(out),'requests':out,'created_at_utc':now()}
    def reproduction_request(self,source_run_id):
        sm=self.rt.store.load_manifest(source_run_id); src=self.rt.store.load_artifact_json(source_run_id,'run_request')
        if not sm.get('decision_seal_hash'): raise LaunchError('source run must be decision-sealed for reproduction')
        req=dict(src); req['run_mode']='REPRODUCTION_REPLAY'; req['analysis_cutoff']=sm['analysis_cutoff_utc']; req['idempotency_policy']='NEW_RUN'; req['episode_id']=src.get('episode_id'); req['tags']=list(req.get('tags') or [])+['reproduction-source:'+source_run_id]
        return {'schema_version':'1.0.0','source_run_id':source_run_id,'source_decision_seal_hash':sm['decision_seal_hash'],'source_vault_commit':sm.get('vault_commit'),'request':req,'reproduction_scope':'FROZEN_EVIDENCE_TO_DECISION','created_at_utc':now()}
    def event_requests(self,event_name,event_time_utc,instruments,active_horizon='SHORT_15_60M',run_mode='HISTORICAL_REPLAY'):
        from datetime import datetime,timedelta,timezone
        p=load_json(self.r3/'config'/'event_episode_policy.json'); t=datetime.fromisoformat(event_time_utc.replace('Z','+00:00'))
        if t.tzinfo is None: raise LaunchError('event time must be timezone-aware')
        episode=uid('EP_'+''.join(c for c in event_name.upper() if c.isalnum())[:16]); out=[]
        for off in p['strict_micro_offsets_minutes']:
            cut=(t+timedelta(minutes=off)).astimezone(timezone.utc).isoformat().replace('+00:00','Z')
            for inst in instruments:
                out.append(self.compile_request(instrument=inst,run_mode=run_mode,analysis_cutoff=cut,active_horizon=active_horizon,coverage_mode='EVENT_FAST_STRICT',episode_id=episode,tags=['event:'+event_name,'offset_min:'+str(off)]))
        return episode,out
