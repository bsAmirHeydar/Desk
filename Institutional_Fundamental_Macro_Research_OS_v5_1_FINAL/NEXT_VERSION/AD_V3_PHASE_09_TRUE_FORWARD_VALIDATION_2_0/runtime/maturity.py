from __future__ import annotations
from datetime import timedelta
from zoneinfo import ZoneInfo
from .common import parse_dt, iso, cfg

def _tradable(dt):
    pol=cfg('horizon_evaluation_policy.json'); tz=ZoneInfo(pol['market_timezone']); x=dt.astimezone(tz); wd=x.weekday(); mins=x.hour*60+x.minute
    # CME-style weekly Gold schedule: Sun 17:00 local through Fri 16:00 local, daily 16:00-17:00 break.
    if wd==5:return False
    if wd==6:return mins>=17*60
    if wd==4:return mins<16*60
    return not (16*60<=mins<17*60)

def add_tradable_minutes(start,minutes):
    x=parse_dt(start)
    if x is None: raise ValueError('INVALID_T0_TIME')
    remaining=int(minutes)
    while remaining>0:
        x=x+timedelta(minutes=1)
        if _tradable(x):remaining-=1
    return x

def maturity_for(precommit_time,horizon):
    h=(cfg('horizon_evaluation_policy.json').get('horizons') or {}).get(horizon)
    if not h:raise ValueError('UNKNOWN_HORIZON:'+str(horizon))
    return iso(add_tradable_minutes(precommit_time,h['terminal_minutes']))

def is_mature(maturity_time,now):
    m=parse_dt(maturity_time);n=parse_dt(now)
    if not m or not n:raise ValueError('INVALID_MATURITY_CLOCK')
    return n>=m
