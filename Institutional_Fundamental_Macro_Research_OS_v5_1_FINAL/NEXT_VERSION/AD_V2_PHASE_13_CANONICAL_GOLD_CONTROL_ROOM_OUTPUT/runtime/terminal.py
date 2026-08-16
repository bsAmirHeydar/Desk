from __future__ import annotations
from .model import human_label


def render(model, html_path=None, json_path=None):
    o=model.get('overview') or {}
    b=o.get('human_brief') or {}
    lines=[
      '='*68,
      ' ALPHA DESK V2 - GOLD',
      '='*68,
      '',
      ' جمع‌بندی:',
      f" {b.get('headline') or o.get('current_interpretation') or 'جمع‌بندی انسانی در دسترس نیست.'}",
      '',
      ' چرا؟'
    ]
    why=b.get('why') or []
    if why:
        for x in why[:3]: lines.append(f' - {x}')
    else:
        lines.append(' - دلیل همسوی مشخصی برای نمایش ثبت نشده است.')
    lines += [
      '',
      ' رفتار قیمت:',
      f" {b.get('price_story') or human_label(o.get('price_transmission'))}",
      '',
      ' وضعیت حرکت و ورود:',
      f" {b.get('maturity_story') or ''}",
      f" {b.get('action_context') or human_label(o.get('trade_permission'))}",
      '',
      ' چیزهایی که باید زیر نظر بماند:'
    ]
    watch=b.get('watch_next') or []
    if watch:
        for x in watch[:4]: lines.append(f' - {x}')
    else:
        lines.append(' - مورد برجسته‌ای ثبت نشده است.')
    changes=o.get('changed_since_previous_run') or []
    lines += ['', ' تغییر نسبت به ران قبلی:']
    if changes:
        for x in changes[:6]:
            lines.append(f" - {x.get('domain')}.{x.get('field')}: {x.get('from')} -> {x.get('to')}")
    else:
        lines.append(' - تغییر معنایی مهمی ثبت نشده است.')
    lines += [
      '',
      ' جزئیات فنی کوتاه:',
      f" Pressure    : {o.get('directional_pressure')} ({human_label(o.get('directional_pressure'))})",
      f" Transmission: {o.get('price_transmission')} ({human_label(o.get('price_transmission'))})",
      f" Maturity    : {o.get('opposing_move_maturity')} ({human_label(o.get('opposing_move_maturity'))})",
      f" Readiness   : {o.get('release_readiness')} ({human_label(o.get('release_readiness'))})",
      f" Permission  : {o.get('trade_permission')} ({human_label(o.get('trade_permission'))})",
      f" Data        : {o.get('data_health')} ({human_label(o.get('data_health'))})",
    ]
    if html_path: lines += ['',f' HTML: {html_path}']
    if json_path: lines += [f' JSON: {json_path}']
    lines += ['='*68]
    return '\n'.join(lines)
