from pathlib import Path
import json
from .util import canon,sha,now

def validate(path):
    p=Path(path); prev='GENESIS'; ids=set(); n=0; errors=[]
    if not p.exists(): return {'status':'PASS','records':0,'tip_hash':'GENESIS','errors':[]}
    for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip():continue
        n+=1; row=json.loads(line); got=row.get('record_hash'); tmp=dict(row); tmp.pop('record_hash',None)
        if got!=sha(tmp): errors.append(f'HASH_MISMATCH_LINE_{i}')
        if row.get('previous_record_hash')!=prev: errors.append(f'CHAIN_MISMATCH_LINE_{i}')
        rid=row.get('record_id')
        if rid in ids: errors.append(f'DUPLICATE_ID_{rid}')
        ids.add(rid); prev=got
    return {'status':'PASS' if not errors else 'FAIL','records':n,'tip_hash':prev,'errors':errors}
def append(path,record):
    p=Path(path); state=validate(p)
    if state['status']!='PASS': raise RuntimeError('ledger invalid: '+','.join(state['errors']))
    rid=record.get('record_id')
    if not rid: raise RuntimeError('record_id required')
    if p.exists():
        for line in p.read_text(encoding='utf-8').splitlines():
            if line.strip() and json.loads(line).get('record_id')==rid: raise RuntimeError('duplicate record id: '+rid)
    row={'record_type':'METHOD_PERSPECTIVE_VALIDATION','record_id':rid,'created_at_utc':record.get('created_at_utc') or now(),'previous_record_hash':state['tip_hash'],'payload':record}
    row['record_hash']=sha(row); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(row,sort_keys=True,ensure_ascii=False)+'\n')
    return {'status':'PASS','record_id':rid,'record_hash':row['record_hash']}
