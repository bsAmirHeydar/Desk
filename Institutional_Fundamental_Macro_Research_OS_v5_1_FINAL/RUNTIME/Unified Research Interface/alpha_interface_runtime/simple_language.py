from __future__ import annotations
import re

STATUS_FA={
 'BULLISH':'صعودی','STRONGLY_BULLISH':'صعودی قوی','BEARISH':'نزولی','STRONGLY_BEARISH':'نزولی قوی',
 'BUY':'فقط خرید','BUY_ONLY':'فقط خرید','SELL':'فقط فروش','SELL_ONLY':'فقط فروش','NO_TRADE':'فعلاً معامله نکن',
 'NEUTRAL':'بدون جهت روشن','MIXED':'متناقض','CONTESTED':'مورد اختلاف','UNRESOLVED':'هنوز نتیجه روشن نیست',
 'UNKNOWN':'نامشخص','UNDETERMINED':'نامشخص','UNAVAILABLE':'داده در دسترس نیست','NOT_AVAILABLE':'داده در دسترس نیست',
 'NOT_APPLICABLE':'در اینجا کاربرد ندارد','INSUFFICIENT_EVIDENCE':'شواهد کافی نیست','PRESENT':'موجود','PASS':'سالم',
 'FAIL':'نامعتبر','BLOCKED':'مسدود','HIGH':'بالا','MODERATE':'متوسط','LOW':'کم','VERY_HIGH':'بسیار بالا',
 'VERY_LOW':'بسیار کم','FAVORABLE':'مطلوب','HIGHLY_FAVORABLE':'بسیار مطلوب','DEGRADED':'ضعیف‌شده',
 'BALANCED':'متعادل','SUPPORTIVE':'تأییدکننده','OPPOSING':'مخالف','MIXED_OR_NEUTRAL':'ترکیبی/نامشخص',
 'KEEP':'ادامه‌دار','CONTINUE':'ادامه‌دار','SHORT':'کوتاه‌مدت','PERSISTENT':'پایدار','FRAGILE':'شکننده'
}

SECTION_TITLES={
 'timing':'زمان و موقعیت بازار','fundamental':'وضعیت بنیادی','expectations':'انتظارات، سیاست و شرایط کلی',
 'narrative':'روایت و ذهن بازار','positioning':'موقعیت معامله‌گران','flow':'جریان واقعی خرید و فروش',
 'funding':'نقدینگی و تأمین مالی','mechanics':'ساختار و رفتار بازار'
}

TERM_MAP=[
 ('cross-currency basis','هزینه نسبی تأمین دلار بین بازارها'),('term premium','پاداش نگهداری اوراق بلندمدت'),
 ('real yields','نرخ‌های واقعی'),('real yield','نرخ واقعی'),('dealer gamma','وضعیت آپشن‌ها و پوشش ریسک معامله‌گران بزرگ'),
 ('gamma','حساسیت آپشن‌ها'),('crowding','شلوغی معامله‌گران در یک سمت'),('reflexivity','اثر بازخورد رفتار بازار بر خودش'),
 ('plumbing','زیرساخت تأمین مالی'),('duration','حساسیت به نرخ بهره'),('skew','عدم‌تقارن قیمت‌گذاری ریسک در آپشن‌ها'),
 ('ois','انتظارات بازار از نرخ‌های کوتاه‌مدت'),('convexity','حساسیت غیرخطی'),('liquidity','نقدینگی یا نقدشوندگی')
]

def to_fa(value):
    if value is None:return 'نامشخص'
    s=str(value)
    return STATUS_FA.get(s.upper(),s)

def flatten_text(value,limit=4):
    out=[]
    def add(x):
        if len(out)>=limit or x in (None,'',[],{}): return
        if isinstance(x,str): out.append(x)
        elif isinstance(x,(int,float,bool)): out.append(str(x))
        elif isinstance(x,list):
            for y in x: add(y)
        elif isinstance(x,dict):
            before=len(out)
            for k in ('summary_fa','summary','reason','rationale','interpretation','description','message','text','finding','driver','name','title'):
                if k in x: add(x[k])
            if len(out)==before:
                for y in list(x.values())[:limit]: add(y)
    add(value)
    return out[:limit]

def simplify_text(value,max_chars=520):
    if value is None:return ''
    if not isinstance(value,str):
        value='؛ '.join(flatten_text(value,3))
    s=str(value).strip()
    if not s:return ''
    for a,b in TERM_MAP:
        s=re.sub(re.escape(a),b,s,flags=re.I)
    s=re.sub(r'\s+',' ',s).strip()
    if len(s)>max_chars:s=s[:max_chars].rsplit(' ',1)[0]+'…'
    return s

def relation_fa(stance):
    s=str(stance or '').upper()
    if s=='SUPPORTIVE':return 'تأیید می‌کند'
    if s=='OPPOSING':return 'مخالف است'
    if s=='MIXED_OR_NEUTRAL':return 'متناقض یا کم‌اثر است'
    return 'نامشخص'

def causal_status_text(status):
    s=str(status or '').upper()
    if 'NOT_IDENTIFIED' in s or 'UNIDENTIFIED' in s:
        return 'این توضیح با شواهد سازگار است، اما علت قطعی هنوز شناسایی نشده است.'
    if 'IDENTIFIED' in s and 'NOT_' not in s:
        return 'رابطه علّی در چارچوب فعلی شواهد پشتیبانی شده و شناسایی شده است.'
    if s in ('UNKNOWN','UNDETERMINED',''):
        return 'درباره رابطه علّی هنوز نتیجه قابل اتکایی وجود ندارد.'
    return 'این رابطه یکی از توضیح‌های فعلی است و باید همراه با عدم‌قطعیت آن خوانده شود.'
