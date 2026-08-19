from __future__ import annotations
from .common import cfg

def human(v):
    if v is None:return 'نامشخص'
    return (cfg('human_terminology.json').get('mappings') or {}).get(str(v),str(v))

def scenario_title(v):return human(v)
def data_health_message(dh):
    adm=dh.get('analysis_admission')
    r04=dh.get('r04') or {};dxy=(r04.get('direct_dxy') or {}).get('state');rr=(r04.get('intraday_real_rate_proxy') or {}).get('state');parts=[]
    if adm in ('BLOCK','BLOCKED'):return 'داده‌ی حیاتی کافی نیست و تحلیل جهت‌دار فعلاً مسدود است.'
    if adm in ('DEGRADED','DEGRADED_ALLOW'):parts.append('بخشی از داده‌های مهم ناقص است، اما تحلیل با محدودیت ادامه دارد.')
    if dxy and 'LIVE' not in dxy and 'CONFIGURED' not in dxy:parts.append('شاخص مستقیم دلار زنده تأیید نشده؛ بخش دلار با هویت پروکسی جداگانه نگه داشته شده است.')
    if rr and str(rr).startswith('UNAVAILABLE'):parts.append('بازده واقعی رسمی درون‌روزی نیست و پروکسی درون‌روزی معتبر فعلاً در دسترس نیست.')
    return ' '.join(parts) if parts else 'داده‌های کلیدی برای این Run در وضعیت عملیاتی قابل استفاده‌اند.'

def qualification_message(q):
    if not q:return 'برای قضاوت نهایی کیفیت هنوز وضعیت Qualification کافی در دسترس نیست.'
    sm=q.get('sample_maturity'); fq=q.get('forward_quality_state');cv=q.get('coverage_state');sg=q.get('critical_subgroup_state');pq=q.get('production_qualification_state')
    if pq in ('QUALIFIED','PRODUCTION_ELIGIBLE'):return 'شواهد آینده‌نگر معیارهای کیفیت را پاس کرده‌اند؛ ارتقا همچنان به مجوز صریح نیاز دارد.'
    if sm in (None,'NO_SAMPLES','INSUFFICIENT','EARLY','DEVELOPING'):return 'نمونه‌های آینده‌نگر هنوز برای قضاوت نهایی کیفیت کافی نیستند.'
    if fq=='FAIL':return 'تعداد نمونه کافی است، اما کیفیت تصمیم هنوز معیار تولید را پاس نکرده است.'
    if cv not in ('PASS',True):return 'کیفیت اولیه قابل ارزیابی است، اما پوشش جهت‌ها/رژیم‌ها هنوز کافی نیست.'
    if sg=='FAIL':return 'میانگین کلی کافی نیست؛ یک زیرگروه بحرانی هنوز معیار ایمنی را پاس نکرده است.'
    return 'ارتقای تولید هنوز توسط یکی از گیت‌های آینده‌نگر یا عملیاتی مسدود است.'

def permission_reasons(executive,perspective):
    reasons=[]
    c=executive.get('consumption');f=executive.get('fragility');u=executive.get('unknown_envelope');ms=executive.get('model_sensitivity');rh=executive.get('dominant_root_health_state')
    if c in ('HIGH','CONSUMED','EXHAUSTED'):reasons.append('بخش مهمی از فشار فعلی ممکن است قبلاً در قیمت بیان شده باشد.')
    if f in ('HIGH','CRITICAL'):reasons.append('شکنندگی ساختار فعلی بالا است.')
    if u in ('OPEN','WIDE','CRITICAL'):reasons.append('بخشی از رفتار بازار هنوز خارج از توضیح کامل مدل مانده است.')
    if ms in ('MODEL_SENSITIVE','HIGH','UNSTABLE'):reasons.append('نتیجه به برخی فرض‌های معقول مدل حساس است.')
    if rh in ('DEGRADED','CRITICAL_GAP'):reasons.append('ریشه‌ی غالب از نظر پوشش شواهد شکاف مهم دارد.')
    ov=(perspective.get('overlay') or {}).get('overlay') if perspective else None
    if ov in ('FORCE_WAIT','CAP_TO_CONDITIONAL','CAP_ACTIONABLE_TO_CONDITIONAL'):reasons.append('لایه‌ی سناریویی برای حفظ اختیار تفسیر، مجوز را محدود کرده است.')
    return reasons[:5]

def headline(executive,perspective=None,blocked=False):
    if blocked:return 'داده‌ی حیاتی کافی نیست؛ تحلیل جهت‌دار فعلاً متوقف شده است.'
    d=str(executive.get('direction') or 'UNKNOWN');p=str(executive.get('permission') or 'WAIT');cons=str(executive.get('consumption') or 'UNKNOWN');frag=str(executive.get('fragility') or 'UNKNOWN')
    if 'BULL' in d:base='فشار بنیادی طلا فعلاً صعودی است'
    elif 'BEAR' in d:base='فشار بنیادی طلا فعلاً نزولی است'
    elif d=='MIXED':base='ریشه‌های اصلی طلا فعلاً در تعارض‌اند'
    else:base='شواهد فعلی هنوز جهت علّی روشنی برای طلا نمی‌دهند'
    if p in ('WAIT','WAIT_CANDIDATE'):tail='؛ مجوز فعلی انتظار است'
    elif 'BUY' in p:tail='؛ مجوز پژوهشی فعلی در سمت خرید است'
    elif 'SELL' in p:tail='؛ مجوز پژوهشی فعلی در سمت فروش است'
    else:tail='؛ اختیار تصمیم جهت‌دار صادر نشده است'
    if cons=='HIGH':tail+=' چون بخش مهمی از حرکت ممکن است مصرف شده باشد'
    elif frag in ('HIGH','CRITICAL'):tail+=' چون شکنندگی ساختار فعلی بالاست'
    return base+tail+'.'
