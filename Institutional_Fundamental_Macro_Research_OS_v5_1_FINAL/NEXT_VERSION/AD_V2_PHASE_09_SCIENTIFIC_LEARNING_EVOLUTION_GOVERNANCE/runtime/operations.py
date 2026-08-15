from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
from .store import root,read_jsonl,create,append,hsh
from .taxonomy import build_case
from .patterns import aggregate
from .hypotheses import build as build_hyp
from .queue import item as queue_item

def _load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def _now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def _phase_parent(phase_root):return Path(phase_root).resolve().parent

def load_p07_links(data_root,phase_root):
 pp=_phase_parent(phase_root)
 if str(pp) not in sys.path:sys.path.insert(0,str(pp))
 from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.true_forward import load_links
 return load_links(data_root)

def _load_cases(data_root):
 rt=root(data_root);out=[]
 for x in read_jsonl(rt/'cases/index.jsonl'):
  p=Path(x.get('path',''))
  if p.is_file():
   try:out.append(_load(p))
   except:pass
 return out

def learn_from_links(data_root,phase_root,links,now_utc=None):
 phase_root=Path(phase_root).resolve();pol=_load(phase_root/'config/learning_policy.json');tax=_load(phase_root/'config/failure_taxonomy.json');qpol=_load(phase_root/'config/research_queue_policy.json');rt=root(data_root);now=now_utc or _now();existing={x.get('outcome_link_id') for x in read_jsonl(rt/'cases/index.jsonl')};new=[]
 for link in links:
  if link.get('maturity_state')!='MATURE' or link.get('outcome_link_id') in existing:continue
  c=build_case(link,pol,now);p=rt/'cases'/c['learning_case_id']/'learning_case.json';create(p,c);append(rt/'cases/index.jsonl',{'learning_case_id':c['learning_case_id'],'outcome_link_id':c['outcome_link_id'],'sample_provenance':c['sample_provenance'],'independent_episode_key':c.get('independent_episode_key'),'path':str(p),'learning_case_hash':c['learning_case_hash']});new.append(c)
 cases=_load_cases(data_root);patterns=aggregate(cases,pol);new_patterns=[]
 seenp={x.get('pattern_id') for x in read_jsonl(rt/'patterns/index.jsonl')}
 for ptn in patterns:
  if ptn['pattern_id'] in seenp:continue
  pp=rt/'patterns'/ptn['pattern_id']/'pattern.json';create(pp,ptn);append(rt/'patterns/index.jsonl',{'pattern_id':ptn['pattern_id'],'failure_family':ptn['failure_family'],'proposal_eligible':ptn['proposal_eligible'],'path':str(pp)});new_patterns.append(ptn)
 seenh={x.get('source_pattern_id') for x in read_jsonl(rt/'hypotheses/index.jsonl')};new_h=[]
 for ptn in patterns:
  if ptn['pattern_id'] in seenh:continue
  h=build_hyp(ptn,tax,now)
  if not h:continue
  hp=rt/'hypotheses'/h['hypothesis_id']/'hypothesis.json';create(hp,h);append(rt/'hypotheses/index.jsonl',{'hypothesis_id':h['hypothesis_id'],'source_pattern_id':h['source_pattern_id'],'failure_family':h['failure_family'],'candidate_family':h['candidate_family'],'path':str(hp),'hypothesis_hash':h['hypothesis_hash']});new_h.append(h)
 # research queue snapshot from current recurring patterns
 q=[queue_item(x,qpol) for x in patterns if x['counts']['all_cases']>0];q=sorted(q,key=lambda x:(-x['priority_score'],x['failure_family']))[:qpol['max_open_items']]
 snapshot={'schema_version':'1.0.0','phase':'AD-V2-P09','record_type':'P09_RESEARCH_QUEUE_SNAPSHOT','as_of_utc':now,'items':q,'authority':{'auto_mutation':False,'trade_permission':'V1_INHERITED','broker':'NONE'}};snapshot['snapshot_hash']=hsh(snapshot);sp=rt/'queue'/snapshot['snapshot_hash'].replace(':','_')/'queue.json'
 if not sp.exists():create(sp,snapshot);append(rt/'queue/index.jsonl',{'snapshot_hash':snapshot['snapshot_hash'],'path':str(sp),'items':len(q),'as_of_utc':now})
 return {'new_cases':new,'patterns':patterns,'new_patterns':new_patterns,'new_hypotheses':new_h,'queue':snapshot,'total_cases':len(cases)}

def run_cycle(data_root,phase_root,now_utc=None):
 now=now_utc or _now();links=load_p07_links(data_root,phase_root);res=learn_from_links(data_root,phase_root,links,now);seed=now+'|'+str(len(links))+'|'+str(res['total_cases']);cid='P09CYCLE_'+hashlib.sha256(seed.encode()).hexdigest()[:24].upper();rec={'schema_version':'1.0.0','phase':'AD-V2-P09','record_type':'P09_LEARNING_CYCLE_RECEIPT','cycle_id':cid,'status':'PASS','as_of_utc':now,'learning':{'mature_links_seen':len([x for x in links if x.get('maturity_state')=='MATURE']),'new_cases':len(res['new_cases']),'total_cases':res['total_cases']},'patterns':{'current':len(res['patterns']),'new':len(res['new_patterns']),'proposal_eligible':len([x for x in res['patterns'] if x.get('proposal_eligible')])},'hypotheses':{'new':len(res['new_hypotheses']),'total':len(read_jsonl(root(data_root)/'hypotheses/index.jsonl'))},'research_queue':{'items':len(res['queue']['items']),'snapshot_hash':res['queue']['snapshot_hash']},'integrity':{'status':'PASS','upstream_rewritten':False,'single_case_model_change':False,'historical_used_for_tf_gate':False,'auto_mutation':False},'authority':{'deployment':'SHADOW_LEARNING_ONLY','trade_permission':'V1_INHERITED','broker':'NONE'}};rec['cycle_hash']=hsh(rec);rp=root(data_root)/'cycles'/cid/'cycle.json';create(rp,rec);append(root(data_root)/'cycles/index.jsonl',{'cycle_id':cid,'path':str(rp),'cycle_hash':rec['cycle_hash'],'as_of_utc':now});return rec

def status(data_root):
 rt=root(data_root);c=read_jsonl(rt/'cases/index.jsonl');p=read_jsonl(rt/'patterns/index.jsonl');h=read_jsonl(rt/'hypotheses/index.jsonl');q=read_jsonl(rt/'queue/index.jsonl');cy=read_jsonl(rt/'cycles/index.jsonl');return {'schema_version':'1.0.0','phase':'AD-V2-P09','status':'PASS','learning_cases':len(c),'patterns':len(p),'hypotheses':len(h),'queue_snapshots':len(q),'cycles':len(cy),'latest_cycle':cy[-1] if cy else None,'deployment':'SHADOW_LEARNING_ONLY','authority':{'auto_mutation':False,'trade_permission':'V1_INHERITED','broker':'NONE'}}
