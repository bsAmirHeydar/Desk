#!/usr/bin/env python3
import argparse,json,pathlib
from _v12_common import link_report,frontmatter_and_fence_errors
ap=argparse.ArgumentParser(description='Validate link delta, frontmatter, fences and V12 precedence.')
ap.add_argument('--vault-root',required=True); ap.add_argument('--baseline-link-report',required=True); ap.add_argument('--patch-manifest',required=True)
a=ap.parse_args(); root=pathlib.Path(a.vault_root); base=json.loads(pathlib.Path(a.baseline_link_report).read_text()); m=json.loads(pathlib.Path(a.patch_manifest).read_text())
cur=link_report(root); bU={(x['source'],x['target']) for x in base['unresolved']}; bA={(x['source'],x['target']) for x in base['ambiguous']}
newU=[x for x in cur['unresolved'] if (x['source'],x['target']) not in bU]; newA=[x for x in cur['ambiguous'] if (x['source'],x['target']) not in bA]
paths=[x['path'] for x in m.get('files_added',[])+m.get('files_modified',[])]
e=frontmatter_and_fence_errors(root,paths)
if newU: e.append(f'new unresolved links: {newU[:10]}')
if newA: e.append(f'new ambiguous links: {newA[:10]}')
auth=root/'V12_CANONICAL_AUTHORITY_MAP.yaml'
if not auth.is_file(): e.append('V12 canonical authority map missing')
else:
 t=auth.read_text(encoding='utf-8',errors='replace')
 for x in ['market_attention','narrative_validity','narrative_dominance','narrative_persistence','daily_intelligence']:
  if x not in t: e.append(f'authority map missing {x}')
print(json.dumps({'status':'PASS' if not e else 'FAIL','errors':e,'current_link_counts':cur['counts'],'new_unresolved':len(newU),'new_ambiguous':len(newA)},indent=2)); raise SystemExit(0 if not e else 1)
