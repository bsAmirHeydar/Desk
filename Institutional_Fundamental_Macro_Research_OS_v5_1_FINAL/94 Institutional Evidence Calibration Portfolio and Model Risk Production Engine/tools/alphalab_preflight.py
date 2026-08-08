#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json,re
p=argparse.ArgumentParser(); p.add_argument('--vault-root',required=True); a=p.parse_args(); r=Path(a.vault_root)
errors=[]; warnings=[]
mf=r/'CURRENT_PRODUCTION_MANIFEST.json'
if not mf.exists(): errors.append('missing CURRENT_PRODUCTION_MANIFEST.json')
else:
    try: m=json.loads(mf.read_text(encoding='utf-8'))
    except Exception as e: m={}; errors.append(f'manifest parse: {e}')
    if m.get('current_stack')!='V16.0.0': errors.append('current_stack is not V16.0.0')
    ep=m.get('production_entrypoint')
    if not ep or not (r/ep).exists(): errors.append('production_entrypoint missing')
    allowed=set(m.get('allowed_live_entrypoints') or []); sub=set(m.get('allowed_live_subengines') or [])
    if ep and ep not in allowed: errors.append('production entrypoint is not allowlisted')
    if ep in set(m.get('forbidden_live_entrypoints') or []): errors.append('production entrypoint is forbidden')
    for name,path in (m.get('canonical_authorities') or {}).items():
        if not (r/path).exists(): errors.append(f'authority missing: {name} -> {path}')
    for req in m.get('required_runtime_contracts') or []:
        if not (r/req).exists(): errors.append(f'required runtime contract missing: {req}')
    if m.get('production_universe') != ['XAUUSD','NASDAQ100','SP500','DJIA','EURUSD','USDJPY']: errors.append('production universe mismatch')
    # scan execution-ready production prompts inside canonical Vault, excluding backups
    for f in r.rglob('*.md'):
        if '.alphalab_patch_backups' in f.parts: continue
        try: t=f.read_text(encoding='utf-8',errors='ignore')[:1800]
        except: continue
        if 'type: production-live-analysis-prompt' in t and 'status: execution-ready' in t:
            rel=f.relative_to(r).as_posix()
            if rel not in allowed and rel not in sub:
                errors.append(f'unallowlisted execution-ready production prompt: {rel}')
    # legacy contamination hard check
    for f in m.get('forbidden_live_entrypoints') or []:
        q=r/f
        if q.exists():
            t=q.read_text(encoding='utf-8',errors='ignore')[:1200]
            if 'status: execution-ready' in t: errors.append(f'forbidden legacy prompt still execution-ready: {f}')
print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors,'warnings':warnings},indent=2))
sys.exit(0 if not errors else 2)
