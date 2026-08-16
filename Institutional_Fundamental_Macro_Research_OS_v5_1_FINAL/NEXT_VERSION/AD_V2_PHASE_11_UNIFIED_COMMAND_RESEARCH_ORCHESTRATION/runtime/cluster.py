from pathlib import Path
import hashlib,json
from .common import load
class ClusterError(ValueError):pass

def compile_cluster(phase_root):
 root=Path(phase_root);reg=load(root/'config/gold_master_cluster_registry.json');parts=[];seen=set()
 for c in reg['ordered_clusters']:
  cid=c['cluster_id']
  if cid in seen:raise ClusterError('duplicate cluster '+cid)
  seen.add(cid);p=root/c['prompt_path']
  if not p.is_file():raise ClusterError('missing cluster prompt '+str(p))
  parts.append(p.read_text(encoding='utf-8').rstrip())
 required=set(reg['legacy_r2_required_nodes']);anchors=set();
 for x in reg['ordered_clusters']: anchors.update(x.get('legacy_node_anchors') or [x['legacy_node_anchor']])
 if not required.issubset(anchors):raise ClusterError('master cluster does not cover all canonical S3 nodes')
 text='\n\n---\n\n'.join(parts)+'\n';fp=hashlib.sha256(text.encode()).hexdigest()
 return {'schema_version':'1.0.0','cluster_id':reg['cluster_id'],'subject':'XAUUSD','cluster_count':len(parts),'prompt_sha256':fp,'prompt_text':text,'pressure_price_separation':True,'v1_registry_mutated':False}
