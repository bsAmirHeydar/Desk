#!/usr/bin/env python3
from pathlib import Path
import argparse,json,datetime,sys

def dt(s):
    try:return datetime.datetime.fromisoformat((s or '').replace('Z','+00:00')) if s else None
    except:return None
p=argparse.ArgumentParser();p.add_argument('--cognitive-input',required=True);p.add_argument('--evidence-pack',required=True);a=p.parse_args()
x=json.loads(Path(a.cognitive_input).read_text(encoding='utf-8'));pack=json.loads(Path(a.evidence_pack).read_text(encoding='utf-8'));errors=[];resolved=[]
if pack.get('symbol')!=x.get('instrument'):errors.append('SYMBOL_MISMATCH')
if pack.get('analysis_cutoff_utc')!=x.get('analysis_cutoff_utc'):errors.append('CUTOFF_MISMATCH')
facts={f.get('fact_id'):f for f in pack.get('fact_records') or [] if f.get('fact_id')};cut=dt(x.get('analysis_cutoff_utc'))
for h in (x.get('hypothesis_set') or {}).get('hypotheses') or []:
    for fld in ['supporting_evidence','contradicting_evidence','missing_evidence']:
        for ev in h.get(fld) or []:
            if ev.get('evidence_type')!='FACT_REF':continue
            fid=ev.get('fact_id');f=facts.get(fid)
            if not f:
                errors.append('MISSING_FACT:'+str(fid));continue
            if ev.get('root_id') and f.get('root_cause_id') and ev['root_id']!=f['root_cause_id']:errors.append('ROOT_MISMATCH:'+str(fid))
            if ev.get('source_grade') and (f.get('source') or {}).get('tier') and ev['source_grade']!=(f.get('source') or {}).get('tier'):errors.append('SOURCE_GRADE_MISMATCH:'+str(fid))
            seen=dt((f.get('time') or {}).get('first_seen_time') or (f.get('time') or {}).get('publication_time'))
            if seen and cut and seen>cut:errors.append('FUTURE_FACT:'+str(fid))
            resolved.append(fid)
out={'status':'PASS' if not errors else 'FAIL','resolved_fact_refs':sorted(set(resolved)),'resolved_count':len(set(resolved)),'errors':errors};print(json.dumps(out,indent=2,ensure_ascii=False));sys.exit(0 if not errors else 2)
