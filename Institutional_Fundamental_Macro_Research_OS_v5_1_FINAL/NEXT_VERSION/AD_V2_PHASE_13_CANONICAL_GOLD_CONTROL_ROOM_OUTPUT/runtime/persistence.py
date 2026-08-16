from __future__ import annotations
from pathlib import Path
from copy import deepcopy
import json, os
from .common import dump_json, load_json, hobj, safe_id
from .render_html import render

class OutputConflict(RuntimeError): pass

def root(data_root): return Path(data_root)/'alpha_desk_v2'/'control_room'

def _append(path,row):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')

def persist(data_root, model):
    r=root(data_root);run_id=safe_id((model.get('run') or {}).get('run_id'));archive=r/'runs'/run_id;archive.mkdir(parents=True,exist_ok=True)
    jp=archive/'control_room.json';hp=archive/'control_room.html'
    if jp.exists():
        old=load_json(jp)
        if old.get('canonical_content_hash')!=model.get('canonical_content_hash'):
            raise OutputConflict('immutable archived control-room conflict for run '+run_id)
        if not hp.exists(): render(old,hp)
        chosen=old
    else:
        dump_json(jp,model);render(model,hp);chosen=model
        _append(r/'index.jsonl',{'run_id':run_id,'as_of':(model.get('run') or {}).get('as_of'),'schema_id':model.get('schema_id'),'canonical_content_hash':model.get('canonical_content_hash'),'json':str(jp),'html':str(hp)})
    latest=r/'latest';latest.mkdir(parents=True,exist_ok=True);dump_json(latest/'control_room.json',chosen);render(chosen,latest/'control_room.html')
    return {'status':'PASS','run_id':run_id,'archive_json':str(jp),'archive_html':str(hp),'latest_json':str(latest/'control_room.json'),'latest_html':str(latest/'control_room.html'),'index':str(r/'index.jsonl'),'canonical_content_hash':chosen.get('canonical_content_hash')}

def latest(data_root):
    p=root(data_root)/'latest'/'control_room.json'
    return load_json(p) if p.exists() else None
