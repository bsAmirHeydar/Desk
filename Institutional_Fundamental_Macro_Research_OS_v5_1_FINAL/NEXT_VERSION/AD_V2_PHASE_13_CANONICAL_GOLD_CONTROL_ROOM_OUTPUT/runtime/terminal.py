from __future__ import annotations

def render(model, html_path=None, json_path=None):
    o=model.get('overview') or {};p=model.get('pressure') or {}
    lines=['='*60,' ALPHA DESK V2 — GOLD CONTROL ROOM','='*60,
      f" Pressure          : {o.get('directional_pressure')} / {o.get('pressure_trend')}",
      f" Consumption       : {o.get('driver_consumption')}",
      f" Remaining         : {o.get('remaining_causal_pressure')}",
      f" Transmission      : {o.get('price_transmission')}",
      f" Unreleased        : {o.get('unreleased_pressure')}",
      f" Opposing Move     : {o.get('opposing_move_maturity')}",
      f" Release Readiness : {o.get('release_readiness')}",
      f" Permission        : {o.get('trade_permission')}",
      f" Data Health       : {o.get('data_health')}",'='*60,' What changed:']
    changes=o.get('changed_since_previous_run') or []
    if changes:
        for x in changes[:8]:lines.append(f" - {x.get('domain')}.{x.get('field')}: {x.get('from')} -> {x.get('to')}")
    else: lines.append(' - No material semantic change recorded.')
    if html_path:lines += ['',f' HTML: {html_path}']
    if json_path:lines += [f' JSON: {json_path}']
    lines += ['='*60]
    return '\n'.join(lines)
