from pathlib import Path
from datetime import datetime, timezone
import platform,sys,os,tempfile,subprocess,time
from zoneinfo import ZoneInfo
from .util import now,data_root,dump_json,current_certification_surface

def certify(vault_root):
    v=Path(vault_root).resolve();checks=[];errors=[];iswin=platform.system()=='Windows'
    def ck(n,b,detail=None):checks.append({'name':n,'pass':bool(b),'detail':detail});errors.extend([] if b else [n])
    ck('real_windows_host',iswin,platform.platform())
    ck('python_supported',sys.version_info>=(3,10),platform.python_version())
    try:
        ZoneInfo('UTC');ny=ZoneInfo('America/New_York');ck('timezone_database_available',True,str(ny))
        jan=datetime(2026,1,15,12,0,tzinfo=ny).utcoffset();jul=datetime(2026,7,15,12,0,tzinfo=ny).utcoffset();ck('new_york_dst_rules_available',jan!=jul,{'jan':str(jan),'jul':str(jul)})
    except Exception as e:ck('timezone_database_available',False,str(e))
    u=datetime.now(timezone.utc);ck('aware_utc_clock',u.tzinfo is not None,u.isoformat())
    try:
        local=datetime.now().astimezone();ck('aware_local_clock',local.tzinfo is not None,{'local':local.isoformat(),'zone':str(local.tzinfo)})
    except Exception as e:ck('aware_local_clock',False,str(e))
    try:
        dr=data_root(v);dr.mkdir(parents=True,exist_ok=True);fd,p=tempfile.mkstemp(prefix='.hostcert_',dir=str(dr));os.write(fd,b'ok');os.close(fd);Path(p).unlink();ck('data_root_write_atomic_prerequisite',True,str(dr))
    except Exception as e:ck('data_root_write_atomic_prerequisite',False,str(e))
    try:
        q=subprocess.run([sys.executable,'-c','import subprocess,sys; r=subprocess.run([sys.executable,"-c","print(7)"],capture_output=True,text=True); print(r.stdout.strip())'],capture_output=True,text=True,timeout=30);ck('subprocess_execution',q.returncode==0 and q.stdout.strip()=='7',q.stderr[-1000:])
    except Exception as e:ck('subprocess_execution',False,str(e))
    try:surface=current_certification_surface(v);ck('r4_source_surface_current',True,surface)
    except Exception as e:surface=None;ck('r4_source_surface_current',False,str(e))
    host={'system':platform.system(),'release':platform.release(),'version':platform.version(),'machine':platform.machine(),'python':platform.python_version(),'executable':sys.executable,'local_timezone':str(datetime.now().astimezone().tzinfo),'utc_now':u.isoformat().replace('+00:00','Z')}
    # Non-Windows execution can validate machinery but must never certify the user's Windows host.
    if not iswin:status='PENDING';classification='HOST_CERTIFICATION_PENDING_REAL_WINDOWS_HOST_EXECUTION'
    elif any(not x['pass'] for x in checks):status='FAIL';classification='HOST_PLATFORM_NOT_CERTIFIED'
    else:status='PASS';classification='WINDOWS_HOST_PLATFORM_CERTIFIED'
    out={'schema_version':'1.0.0','true_forward_version':'TF1.0.0','status':status,'classification':classification,'checks':checks,'host':host,'certification_surface_fingerprint':surface,'environment_live_attestation':'SEPARATE_C1_ENVIRONMENT_CERTIFICATION_REQUIRED','created_at_utc':now(),'errors':errors}
    dump_json(data_root(v)/'commissioning'/'host_certificate.json',out);return out
