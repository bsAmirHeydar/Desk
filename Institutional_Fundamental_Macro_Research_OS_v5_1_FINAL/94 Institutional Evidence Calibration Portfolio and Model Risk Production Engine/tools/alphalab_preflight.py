#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json,subprocess
p=argparse.ArgumentParser(); p.add_argument('--vault-root',required=True); p.add_argument('--mode',choices=['runtime','deployment'],default='runtime'); a=p.parse_args(); r=Path(a.vault_root); errors=[]; warnings=[]
mf=r/'CURRENT_PRODUCTION_MANIFEST.json'
try: m=json.loads(mf.read_text(encoding='utf-8'))
except Exception as e: m={}; errors.append(f'manifest parse: {e}')
if m.get('current_stack') not in {'V16.1.0','V17.0.0','V18.0.0'}: errors.append('current_stack is not a supported V16.1/V17.0/V18.0 stack')
if m.get('current_stack') in {'V17.0.0','V18.0.0'} and 'fact_constitution' not in (m.get('canonical_authorities') or {}): errors.append('V17+ fact_constitution authority missing')
if m.get('current_stack')=='V18.0.0':
    ca=m.get('canonical_authorities') or {}
    for k in ['positioning_ownership','actual_flow','funding_plumbing','institutional_mechanics_capacity','d2_six_market_router']:
        if k not in ca: errors.append('V18 D2 authority missing: '+k)
    d2=m.get('d2_market_sciences') or {}
    if d2.get('authority_mode')!='CANONICAL_SHADOW' or d2.get('final_permission_effect')!='NONE': errors.append('V18 D2 shadow-only authority boundary violated')
ep=m.get('production_entrypoint'); allowed=set(m.get('allowed_live_entrypoints') or []); sub=set(m.get('allowed_live_subengines') or [])
if not ep or not (r/ep).exists(): errors.append('production_entrypoint missing')
if ep and ep not in allowed: errors.append('production entrypoint not allowlisted')
if ep in set(m.get('forbidden_live_entrypoints') or []): errors.append('production entrypoint forbidden')
for name,path in (m.get('canonical_authorities') or {}).items():
    if not (r/path).exists(): errors.append(f'authority missing: {name} -> {path}')
for req in m.get('required_runtime_contracts') or []:
    if not (r/req).exists(): errors.append(f'required runtime contract missing: {req}')
if m.get('production_universe') != ['XAUUSD','NASDAQ100','SP500','DJIA','EURUSD','USDJPY']: errors.append('production universe mismatch')
# mirror integrity
sync=r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/tools/alphalab_manifest_sync.py'
if sync.exists():
    c=subprocess.run([sys.executable,str(sync),'--vault-root',str(r),'--check'],capture_output=True,text=True)
    if c.returncode: errors.append('manifest mirror drift: '+c.stdout[-500:])
else: errors.append('manifest sync tool missing')
# retrieval policy
try:
    pol=json.loads((r/m['retrieval_policy']).read_text(encoding='utf-8'))
    if pol.get('mode')!='ENFORCED': errors.append('retrieval firewall not enforced')
except Exception as e: errors.append('retrieval policy error: '+str(e))
if a.mode=='deployment':
    for f in r.rglob('*.md'):
        if '.alphalab_patch_backups' in f.parts: continue
        try: t=f.read_text(encoding='utf-8',errors='ignore')[:2200]
        except: continue
        if 'type: production-live-analysis-prompt' in t and 'status: execution-ready' in t:
            rel=f.relative_to(r).as_posix()
            if rel not in allowed and rel not in sub: errors.append('unallowlisted execution-ready production prompt: '+rel)
    for f in m.get('forbidden_live_entrypoints') or []:
        q=r/f
        if q.exists() and 'status: execution-ready' in q.read_text(encoding='utf-8',errors='ignore')[:1400]: errors.append('forbidden legacy prompt execution-ready: '+f)
print(json.dumps({'status':'PASS' if not errors else 'FAIL','mode':a.mode,'errors':errors,'warnings':warnings},indent=2)); sys.exit(0 if not errors else 2)
