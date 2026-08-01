#!/usr/bin/env python3
"""Validate Alpha Lab hybrid reconstruction CSV outputs."""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from pathlib import Path

REQUIRED_TYPES = {
    "DAILY_BASELINE", "END_OF_DAY_STATE"
}
EVENT_TYPES = {
    "SCHEDULED_EVENT_T0", "UNSCHEDULED_EVENT_T0"
}
MICRO = ["EVENT_T_PLUS_5","EVENT_T_PLUS_15","EVENT_T_PLUS_30","EVENT_T_PLUS_60"]
MARKET_MIN = {"Nasdaq 100":6,"S&P 500":6,"Gold":6,"EURUSD":6}
MAX_GAP_MIN = {"Nasdaq 100":120,"S&P 500":120,"Gold":180,"EURUSD":180}

def parse_time(s):
    return datetime.fromisoformat(s.replace('Z','+00:00'))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('csv_path')
    ap.add_argument('--report', default='DENSITY_VALIDATION_REPORT.json')
    args=ap.parse_args()
    rows=list(csv.DictReader(open(args.csv_path,encoding='utf-8-sig',newline='')))
    by=defaultdict(list)
    failures=[]
    for r in rows:
        by[(r.get('market',''),r.get('trading_date',''))].append(r)
    stats={}
    for (market,day), rs in sorted(by.items()):
        types=Counter(r.get('record_type','') for r in rs)
        for req in REQUIRED_TYPES:
            if types[req] < 1: failures.append(f'{market} {day}: missing {req}')
        min_n=MARKET_MIN.get(market,1)
        if len(rs)<min_n: failures.append(f'{market} {day}: only {len(rs)} records, minimum {min_n}')
        times=[]
        for r in rs:
            try: times.append(parse_time(r['event_time_utc']))
            except Exception: failures.append(f'{market} {day}: invalid event_time_utc')
        times=sorted(times)
        maxgap=max(((b-a).total_seconds()/60 for a,b in zip(times,times[1:])), default=0)
        if maxgap>MAX_GAP_MIN.get(market,240): failures.append(f'{market} {day}: max gap {maxgap:.0f}m')
        stats[f'{market}|{day}']={'records':len(rs),'types':dict(types),'max_gap_minutes':maxgap}
    # event micro-window test by parent/event id
    groups=defaultdict(set)
    for r in rows:
        eid=r.get('parent_record_id') or r.get('event_id')
        if eid: groups[eid].add(r.get('record_type',''))
    for eid, types in groups.items():
        if types & EVENT_TYPES:
            for m in MICRO:
                if m not in types:
                    # explicit missing reason can satisfy
                    has_reason=any((r.get('parent_record_id') or r.get('event_id'))==eid and r.get('missing_window_reason') for r in rows)
                    if not has_reason: failures.append(f'event {eid}: missing {m}')
    report={'status':'PASS' if not failures else 'FAIL','rows':len(rows),'market_days':len(by),'failures':failures,'stats':stats}
    Path(args.report).write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'status':report['status'],'failures':len(failures),'rows':len(rows)}))
    raise SystemExit(0 if not failures else 1)
if __name__=='__main__': main()
