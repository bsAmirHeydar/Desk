from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, tempfile

SCHEMA_ID = 'alpha_desk_v2.gold_control_room.v1'
SCHEMA_VERSION = '1.0.0'
PHASE = 'AD-V2-P13'
CONTRACT = 'ALPHA_DESK_V2_GOLD_CONTROL_ROOM_V1'


def now_utc():
    return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',',':'), ensure_ascii=False, default=str)


def hobj(obj):
    return hashlib.sha256(canon(obj).encode('utf-8')).hexdigest()


def sha256_bytes(data: bytes):
    return hashlib.sha256(data).hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def dump_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, ensure_ascii=False, indent=2) + '\n'
    tmp = path.with_name(path.name + '.tmp.' + next(tempfile._get_candidate_names()))
    tmp.write_text(text, encoding='utf-8', newline='\n')
    os.replace(tmp, path)
    return path


def data_root(repo):
    env = os.getenv('ALPHALAB_DATA_ROOT','').strip()
    if env:
        return Path(env).expanduser().resolve()
    repo = Path(repo).resolve()
    return repo.parent / 'AlphaLab_Data'


def p13_root(repo):
    return Path(repo).resolve() / 'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL' / 'NEXT_VERSION' / 'AD_V2_PHASE_13_CANONICAL_GOLD_CONTROL_ROOM_OUTPUT'


def safe_id(value):
    s = ''.join(c if c.isalnum() or c in '._-' else '_' for c in str(value or 'UNKNOWN'))
    return s[:160] or 'UNKNOWN'


def unknown(value=None):
    return value if value not in (None, '', [], {}) else 'UNKNOWN'
