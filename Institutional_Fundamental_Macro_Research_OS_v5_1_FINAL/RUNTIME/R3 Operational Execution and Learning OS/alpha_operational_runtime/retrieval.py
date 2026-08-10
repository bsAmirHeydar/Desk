from pathlib import Path
import os,shlex,subprocess,base64,json
from datetime import datetime,timezone
from .util import load_json,now,uid,decode_content,sha256_obj,dump_json

class RetrievalError(RuntimeError): pass
def _dt(x):
    if not x:return None
    return datetime.fromisoformat(str(x).replace('Z','+00:00')).astimezone(timezone.utc)
class RetrievalRuntime:
    def __init__(self,vault,rt):
        self.vault=Path(vault);self.rt=rt;self.r3=self.vault/'RUNTIME'/'R3 Operational Execution and Learning OS';self.policy=load_json(self.r3/'config'/'retrieval_runtime_policy.json');self.bind=load_json(self.r3/'config'/'source_bindings.json')
        self.families=load_json(self.vault/'100 Six-Market D2 Fact Books and Production Shadow Engine'/'config'/'fact_observability_registry.json');self.sources=load_json(self.vault/'100 Six-Market D2 Fact Books and Production Shadow Engine'/'config'/'d2_source_registry.json');self.market_map=load_json(self.vault/'100 Six-Market D2 Fact Books and Production Shadow Engine'/'config'/'six_market_observability_map.json')
        self.fmap={x['family_id']:x for x in self.families['families']};self.smap={x['source_id']:x for x in self.sources['sources']}
    def _requirements(self,run_id):
        cov=self.rt.store.load_artifact_json(run_id,'coverage_requirements');req=[]
        m=self.rt.store.load_manifest(run_id);instrument=m.get('subject')
        for f in cov['fact_families']:
            fam=self.fmap.get(f['family_id'],{});req.append({'requirement_id':'REQ_'+f['family_id'],'instrument':instrument,'fact_family':f['family_id'],'applicability':f['applicability'],'materiality':f['materiality'],'reason':f['reason'],'source_ids':list(fam.get('direct_or_primary_source_ids',[])),'proxy_source_ids':list(fam.get('proxy_or_context_source_ids',[])),'licensed_source_ids':list(fam.get('licensed_or_private_source_ids',[]))})
        return req
    def _provisional(self,instrument,active_horizon):
        mm=self.market_map['markets'].get(instrument,{})
        out=[]
        for fid,fam in self.fmap.items():
            x=mm.get(fid,{});mat=x.get('materiality','CONTEXTUAL')
            out.append({'requirement_id':'PREFETCH_'+fid,'instrument':instrument,'fact_family':fid,'applicability':'APPLICABLE','materiality':mat,'reason':'R3 strict live pre-run intake covers the full 16-family surface before the decision cutoff is frozen.','source_ids':list(fam.get('direct_or_primary_source_ids',[])),'proxy_source_ids':list(fam.get('proxy_or_context_source_ids',[])),'licensed_source_ids':list(fam.get('licensed_or_private_source_ids',[]))})
        return out
    def _binding(self,source_id):return self.bind.get('bindings',{}).get(source_id,self.bind['default'])
    def _external(self,b,request):
        cmd=os.environ.get(b.get('command_env',''))
        if not cmd:return []
        d=self.rt.data_root/'tmp'/'r3_retrieval';d.mkdir(parents=True,exist_ok=True);rid=uid('RET');req=d/(rid+'.request.json');rsp=d/(rid+'.response.json');dump_json(req,request);
        try:
            parts=json.loads(cmd) if cmd.lstrip().startswith('[') else shlex.split(cmd,posix=True)
            if not isinstance(parts,list) or not all(isinstance(x,str) and x for x in parts):return []
        except Exception:return []
        parts=parts+[str(req),str(rsp)]
        q=subprocess.run(parts,capture_output=True,text=True,timeout=int(b.get('timeout_seconds',1200)),env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        if q.returncode or not rsp.exists():return []
        try:return load_json(rsp).get('snapshots',[]) or []
        except Exception:return []
    def _local(self,b,source_id,reqid):
        p=os.environ.get(b.get('path_env','')) if b.get('path_env') else b.get('path')
        if not p or not Path(p).is_file():return []
        t=now();data=Path(p).read_bytes();enc='BASE64' if b.get('binary') else 'UTF8_TEXT';content=base64.b64encode(data).decode() if enc=='BASE64' else data.decode('utf-8','replace')
        return [{'schema_version':'1.0.0','snapshot_id':uid('SNP'),'requirement_id':reqid,'source_id':source_id,'source_uri':str(Path(p).resolve()),'media_type':b.get('media_type','text/plain'),'content':content,'content_encoding':enc,'publication_time':b.get('publication_time'),'first_available_time':b.get('first_available_time') or t,'retrieved_at':t,'ingested_at':t,'event_time':None,'reference_time':None,'effective_time':None,'vintage_id':b.get('vintage_id') or ('LOCAL_'+t),'vintage_integrity':b.get('vintage_integrity','ORIGINAL_CAPTURE'),'superseded_at':None,'metadata':{'adapter':'LOCAL_FILE'}}]
    def _rows_for_source(self,sid,r,run_mode,cutoff,host_retriever=None):
        b=self._binding(sid);a=b.get('adapter','UNBOUND');request={'schema_version':'1.0.0','operation':'EVIDENCE_RETRIEVAL','analysis_cutoff_utc':cutoff,'capture_mode':('LIVE_PRE_RUN' if run_mode in ('LIVE','SHADOW_LIVE') and cutoff is None else 'FROZEN_CUTOFF'),'run_mode':run_mode,'instrument':r.get('instrument'),'requirements':[r],'source_contracts':[self.smap.get(sid,{'source_id':sid})],'strict_point_in_time':True}
        try:
            if a=='LOCAL_FILE':return self._local(b,sid,r['requirement_id'])
            if a=='EXTERNAL_COMMAND':return self._external(b,request)
            if a=='HOST_CAPABILITY' and host_retriever:return host_retriever(request) or []
        except Exception:return []
        return []
    def _validate_snapshot(self,s,mode,cutoff):
        required=('snapshot_id','source_id','first_available_time','retrieved_at','ingested_at','vintage_integrity')
        if any(not s.get(x) for x in required):return False,'MISSING_REQUIRED_SNAPSHOT_CLOCK_OR_ID'
        try:fa=_dt(s['first_available_time']);ret=_dt(s['retrieved_at']);ing=_dt(s['ingested_at']);co=_dt(cutoff)
        except Exception:return False,'INVALID_TIMESTAMP'
        if ret<fa or ing<ret:return False,'TEMPORAL_ORDER_INVALID'
        vi=s.get('vintage_integrity')
        if mode in ('LIVE','SHADOW_LIVE') and (ret>co or ing>co):return False,'LIVE_LATE_RETRIEVAL'
        if mode not in ('LIVE','SHADOW_LIVE'):
            if vi=='CURRENT_ONLY':return False,'HISTORICAL_CURRENT_ONLY_FORBIDDEN'
            if vi=='ORIGINAL_CAPTURE' and ret>co:return False,'POST_CUTOFF_ORIGINAL_CAPTURE_INVALID'
            if vi not in ('ORIGINAL_CAPTURE','OFFICIAL_VINTAGE_ARCHIVE'):return False,'HISTORICAL_STRICT_VINTAGE_REQUIRED'
            if vi=='OFFICIAL_VINTAGE_ARCHIVE' and not s.get('vintage_id'):return False,'ARCHIVE_VINTAGE_ID_REQUIRED'
        return True,'VALID'
    def _discovery_requests(self,instrument,active_horizon):
        return [
            {'requirement_id':'DISCOVERY_MACRO_OFFICIAL','instrument':instrument,'fact_family':'CROSS_DOMAIN_MACRO_POLICY_DISCOVERY','applicability':'APPLICABLE','materiality':'SUPPORTING','reason':'Pre-cutoff broad official macro/policy/event discovery for fundamental and expectations state.','source_ids':['ALPHALAB_OFFICIAL_MACRO_WEB'],'proxy_source_ids':[],'licensed_source_ids':[],'evidence_role':'DISCOVERY_OFFICIAL'},
            {'requirement_id':'DISCOVERY_MACRO_INSTITUTIONAL','instrument':instrument,'fact_family':'INSTITUTIONAL_MACRO_SURVEY_DISCOVERY','applicability':'APPLICABLE','materiality':'SUPPORTING','reason':'Pre-cutoff institutional survey/PMI/leading-indicator discovery. This lane is supporting context and cannot become direct observed fact without D1 admission.','source_ids':['ALPHALAB_INSTITUTIONAL_MACRO_WEB'],'proxy_source_ids':[],'licensed_source_ids':[],'evidence_role':'DISCOVERY_INSTITUTIONAL'},
            {'requirement_id':'DISCOVERY_NARRATIVE','instrument':instrument,'fact_family':'MARKET_NARRATIVE_ATTENTION_DISCOVERY','applicability':'APPLICABLE','materiality':'SUPPORTING','reason':'Pre-cutoff high-quality market narrative/attention discovery; secondary reporting never becomes observed fact without D1 admission.','source_ids':['ALPHALAB_NARRATIVE_WEB'],'proxy_source_ids':[],'licensed_source_ids':[],'evidence_role':'DISCOVERY_NEWS'},
            {'requirement_id':'DISCOVERY_EVENT_CALENDAR','instrument':instrument,'fact_family':'SCHEDULED_EVENT_CALENDAR_DISCOVERY','applicability':'APPLICABLE','materiality':'SUPPORTING','reason':'Pre-cutoff official scheduled-event/calendar discovery for temporal state.','source_ids':['ALPHALAB_EVENT_WEB'],'proxy_source_ids':[],'licensed_source_ids':[],'evidence_role':'DISCOVERY_OFFICIAL'}
        ]
    def prefetch_live(self,instrument,active_horizon,host_retriever=None,allow_private_sources=False):
        started=now();reqs=self._provisional(instrument,active_horizon);captured=[];gaps=[]
        discovery=self._discovery_requests(instrument,active_horizon)
        for r in discovery:
            for sid in r['source_ids']:
                rows=self._rows_for_source(sid,r,'LIVE',None,host_retriever)
                for x in rows or []:
                    x=dict(x);x['source_id']=sid;x['fact_family']=r['fact_family'];x['evidence_role']=r['evidence_role'];x['requirement_id']=r['requirement_id']
                    try:
                        raw=decode_content(x);h,_,_=self.rt.store.objects.put_bytes(raw,x.get('media_type','application/octet-stream'));x['preintake_artifact_hash']=h;x.pop('content',None)
                    except Exception:continue
                    captured.append(x)
        for r in reqs:
            roles=[('DIRECT',r['source_ids']),('PROXY',r['proxy_source_ids'])]
            if allow_private_sources:roles.append(('LICENSED',r['licensed_source_ids']))
            for role,sids in roles:
                for sid in sids:
                    rows=self._rows_for_source(sid,r,'LIVE',None,host_retriever)
                    if not rows:continue
                    for x in rows:
                        x=dict(x);x['source_id']=sid;x['fact_family']=r['fact_family'];x['evidence_role']=role
                        try:raw=decode_content(x);h,_,_=self.rt.store.objects.put_bytes(raw,x.get('media_type','application/octet-stream'));x['preintake_artifact_hash']=h;x.pop('content',None)
                        except Exception:continue
                        captured.append(x)
        cutoff=now()
        valid=[]
        for s in captured:
            ok,why=self._validate_snapshot(s,'LIVE',cutoff)
            if ok:valid.append(s)
            else:gaps.append({'fact_family':s.get('fact_family'),'source_id':s.get('source_id'),'status':'INVALID_LIVE_INTAKE_SNAPSHOT','reason':why})
        times=[_dt(s['retrieved_at']) for s in valid if s.get('retrieved_at')]
        skew=(max(times)-min(times)).total_seconds() if len(times)>1 else 0.0
        warn=float(self.policy.get('live_retrieval_skew',{}).get('standard_warn_seconds',120)); intake={'schema_version':'1.0.0','intake_id':uid('INTAKE'),'instrument':instrument,'active_horizon':active_horizon,'started_at_utc':started,'cutoff_utc':cutoff,'cutoff_semantics':'INTAKE_COMPLETION_UTC','atomic_snapshot_claim':False,'retrieval_skew_seconds':skew,'retrieval_skew_state':('RECHECK_REQUIRED' if skew>warn else 'RECORDED'),'snapshots':valid,'gaps':gaps,'full_family_surface_count':len(reqs),'discovery_requirement_count':len(discovery),'created_at_utc':now()}
        p=self.rt.data_root/'intake'/'live';p.mkdir(parents=True,exist_ok=True);dump_json(p/(intake['intake_id']+'.json'),intake);return intake
    def capture(self,run_id,host_retriever=None,live_intake=None):
        m=self.rt.store.load_manifest(run_id);reqobj=self.rt.store.load_artifact_json(run_id,'run_request');requirements=self._requirements(run_id);snapshots=[];gaps=[];proxy=[]
        if m['run_mode'] in ('LIVE','SHADOW_LIVE') and not live_intake:
            gaps=[{'requirement_id':r['requirement_id'],'fact_family':r['fact_family'],'materiality':r['materiality'],'status':'LIVE_INTAKE_REQUIRED','source_ids':r['source_ids'],'reason':'On-demand retrieval after a live cutoff is forbidden. Use strict pre-run intake.'} for r in requirements if r['applicability']!='NOT_APPLICABLE']
        else:
            intake_rows=(live_intake or {}).get('snapshots',[])
            for r in requirements:
                if r['applicability']=='NOT_APPLICABLE':continue
                direct=[];prox=[]
                roles=[('DIRECT',r['source_ids']),('PROXY',r['proxy_source_ids'])]
                if reqobj.get('allow_private_sources'):roles.append(('LICENSED',r['licensed_source_ids']))
                for role,sids in roles:
                    for sid in sids:
                        if live_intake:
                            rows=[dict(x) for x in intake_rows if x.get('source_id')==sid and x.get('fact_family')==r['fact_family']]
                            for x in rows:
                                raw=self.rt.store.objects.get_bytes(x['preintake_artifact_hash']);x['content']=base64.b64encode(raw).decode();x['content_encoding']='BASE64';x['requirement_id']=r['requirement_id'] if role!='PROXY' else r['requirement_id']+'__PROXY';x['evidence_role']=role
                        else:
                            rows=self._rows_for_source(sid,r,m['run_mode'],m['analysis_cutoff_utc'],host_retriever)
                            for x in rows:x=dict(x);x['requirement_id']=r['requirement_id'] if role!='PROXY' else r['requirement_id']+'__PROXY';x['source_id']=sid;x['fact_family']=r['fact_family'];x['evidence_role']=role
                        for x in rows:
                            ok,why=self._validate_snapshot(x,m['run_mode'],m['analysis_cutoff_utc'])
                            if not ok:
                                gaps.append({'requirement_id':r['requirement_id'],'fact_family':r['fact_family'],'materiality':r['materiality'],'status':'INVALID_SNAPSHOT_CONTRACT','source_ids':[sid],'reason':why});continue
                            (prox if role=='PROXY' else direct).append(x)
                if not direct:
                    gaps.append({'requirement_id':r['requirement_id'],'fact_family':r['fact_family'],'materiality':r['materiality'],'status':'DIRECT_UNAVAILABLE_PROXY_CONTEXT_PRESENT' if prox else 'UNBOUND_OR_UNAVAILABLE','source_ids':r['source_ids']+r.get('licensed_source_ids',[]),'reason':'No strict direct/primary snapshot satisfied the source contract. Proxy context never substitutes for direct evidence.'})
                snapshots.extend(direct);proxy.extend(prox)
            # Preserve pre-cutoff broad discovery as explicit supplemental evidence. It is never
            # admitted as a direct D1 candidate merely because retrieval succeeded.
            if live_intake:
                for x in intake_rows:
                    role=x.get('evidence_role','')
                    if role not in ('DISCOVERY_OFFICIAL','DISCOVERY_INSTITUTIONAL','DISCOVERY_NEWS'):continue
                    y=dict(x)
                    try:raw=self.rt.store.objects.get_bytes(y['preintake_artifact_hash'])
                    except Exception:continue
                    y['content']=base64.b64encode(raw).decode();y['content_encoding']='BASE64'
                    proxy.append(y)
        allrows=snapshots+proxy;candidates=[];items=[]
        for s in allrows:
            raw=decode_content(s);logical='raw_'+s['source_id'].lower()+'_'+s['snapshot_id'].lower();ref=self.rt.store.put_artifact(run_id,logical,'DECISION','EVIDENCE',raw,s.get('media_type','application/octet-stream'),producer_process_id='R3_RETRIEVAL',producer_version='R3.0.0')
            cand={k:s.get(k) for k in ['snapshot_id','requirement_id','source_id','source_uri','publication_time','first_available_time','retrieved_at','ingested_at','event_time','reference_time','effective_time','vintage_id','vintage_integrity','superseded_at']};cand['artifact_hash']=ref['artifact_hash']
            role=s.get('evidence_role','DIRECT')
            if role in ('DIRECT','LICENSED'):candidates.append(cand)
            items.append({'snapshot_id':s['snapshot_id'],'requirement_id':s['requirement_id'],'source_id':s['source_id'],'evidence_role':role,'artifact_hash':ref['artifact_hash'],'vintage_integrity':s.get('vintage_integrity'),'first_available_time':s.get('first_available_time'),'retrieved_at':s.get('retrieved_at'),'status':'CAPTURED'})
            with self.rt.catalog.connect() as c:c.execute("INSERT OR REPLACE INTO r3_retrieval_items(run_id,snapshot_id,requirement_id,source_id,evidence_role,artifact_hash,vintage_integrity,first_available_time,retrieved_at,status,created_at_utc) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(run_id,s['snapshot_id'],s['requirement_id'],s['source_id'],role,ref['artifact_hash'],s.get('vintage_integrity'),s.get('first_available_time'),s.get('retrieved_at'),'CAPTURED',now()))
        from alpha_runtime.visibility import build_receipt
        base_req=[{'requirement_id':r['requirement_id'],'fact_family':r['fact_family'],'materiality':r['materiality'],'applicability':r['applicability']} for r in requirements]
        vis=build_receipt(run_id,m['analysis_cutoff_utc'],m['run_mode'],base_req,candidates)
        self.rt.store.put_artifact(run_id,'visibility_receipt','DECISION','EVIDENCE',vis,'application/json',producer_process_id='R3_RETRIEVAL',producer_version='R3.0.0')
        receipt={'schema_version':'1.0.0','run_id':run_id,'analysis_cutoff_utc':m['analysis_cutoff_utc'],'live_intake_id':(live_intake or {}).get('intake_id'),'retrieval_skew_seconds':(live_intake or {}).get('retrieval_skew_seconds'),'items':items,'gaps':gaps,'proxy_context_count':sum(1 for x in items if x['evidence_role'] not in ('DIRECT','LICENSED')),'decision_critical_gap_count':sum(1 for g in gaps if g.get('materiality')=='DECISION_CRITICAL'),'material_gap_count':sum(1 for g in gaps if g.get('materiality')=='MATERIAL'),'created_at_utc':now()};receipt['receipt_hash']=sha256_obj({k:v for k,v in receipt.items() if k not in ('created_at_utc','receipt_hash')})
        self.rt.store.put_artifact(run_id,'r3_retrieval_receipt','DECISION','EVIDENCE',receipt,'application/json',producer_process_id='R3_RETRIEVAL',producer_version='R3.0.0')
        return receipt,vis,candidates
