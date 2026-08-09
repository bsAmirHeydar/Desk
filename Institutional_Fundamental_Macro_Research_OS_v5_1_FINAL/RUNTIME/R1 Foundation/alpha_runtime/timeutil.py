from datetime import datetime, timezone
from pathlib import Path
import os
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

class TimeError(ValueError): pass

def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")

def parse_aware(value: str) -> datetime:
    if not isinstance(value,str) or not value.strip(): raise TimeError("timestamp required")
    v=value.strip()
    if v.endswith("Z"): v=v[:-1]+"+00:00"
    try: dt=datetime.fromisoformat(v)
    except Exception as e: raise TimeError(f"invalid timestamp: {value}") from e
    if dt.tzinfo is None: raise TimeError("timezone-aware timestamp required")
    return dt.astimezone(timezone.utc)

def to_utc_z(value: str) -> str:
    return parse_aware(value).isoformat(timespec="seconds").replace("+00:00","Z")

def _bundled_zone_path(zone: str) -> Path:
    parts=[p for p in zone.split('/') if p and p not in ('.','..')]
    return Path(__file__).resolve().parent/'_zoneinfo'/Path(*parts)

def load_zone(zone: str):
    if zone in ('UTC','Etc/UTC','GMT','Etc/GMT'):
        return timezone.utc
    force=os.environ.get('ALPHALAB_FORCE_BUNDLED_TZ','').strip()=='1'
    if not force:
        try:
            return ZoneInfo(zone)
        except ZoneInfoNotFoundError:
            pass
    p=_bundled_zone_path(zone)
    if p.is_file():
        with p.open('rb') as fh:
            return ZoneInfo.from_file(fh,key=zone)
    raise TimeError(f"time zone data unavailable for {zone}; use an explicit UTC/offset timestamp or a bundled market zone")

def local_to_utc(local_value: str, zone: str, fold=None) -> str:
    try: naive=datetime.fromisoformat(local_value)
    except Exception as e: raise TimeError("invalid local timestamp") from e
    if naive.tzinfo is not None: return to_utc_z(local_value)
    z=load_zone(zone); valid=[]
    for f in (0,1):
        aware=naive.replace(tzinfo=z,fold=f)
        back=aware.astimezone(timezone.utc).astimezone(z).replace(tzinfo=None)
        if back==naive: valid.append((f,aware))
    uniq={}
    for f,a in valid: uniq[(a.utcoffset(),a.dst())]=(f,a)
    valid=list(uniq.values())
    if not valid: raise TimeError("nonexistent local time; explicit valid offset/time required")
    if len(valid)>1:
        if fold is None: raise TimeError("ambiguous local time; explicit fold or offset required")
        matches=[a for f,a in valid if f==int(fold)]
        if not matches: raise TimeError("requested fold is not valid for local time")
        aware=matches[0]
    else:
        aware=valid[0][1]
    return aware.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")

def leq(a,b): return parse_aware(a) <= parse_aware(b)
def lt(a,b): return parse_aware(a) < parse_aware(b)
