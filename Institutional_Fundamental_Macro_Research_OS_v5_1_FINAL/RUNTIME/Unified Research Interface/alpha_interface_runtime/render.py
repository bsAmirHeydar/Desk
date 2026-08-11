from pathlib import Path
import json,subprocess,shutil,html

UX_VERSION='UX3.0.0'

LENS_ORDER=['timing','fundamental','expectations','narrative','positioning','flow','funding','mechanics']
LENS_TITLES={
 'timing':'زمان و موقعیت بازار','fundamental':'وضعیت بنیادی','expectations':'انتظارات، سیاست و شرایط کلی',
 'narrative':'روایت، ذهن بازار و میزان مصرف خبر','positioning':'موقعیت معامله‌گران و شلوغی بازار',
 'flow':'جریان واقعی خرید و فروش','funding':'نقدینگی و تأمین مالی','mechanics':'ساختار، ظرفیت و نوسان بازار'
}
SCENARIO_ROLES=[
 ('BASE','مسیر اصلی'),('UPSIDE','صعودی'),('DOWNSIDE','نزولی'),('REVERSAL','برگشت'),
 ('RANGE','رنج'),('EVENT','رویداد'),('NO_TRADE','عدم معامله'),('RARE_SHOCK','شوک نادر')
]
THINKING_GUIDE=[
 ('واقعیت را جدا می‌کنیم','آنچه مشاهده شده با برداشت و تصمیم قاطی نمی‌شود.'),
 ('علت‌های محتمل را می‌سنجیم','حرکت قیمت به‌تنهایی علت را اثبات نمی‌کند و همبستگی به معنی علیت نیست.'),
 ('علیه تحلیل خودمان استدلال می‌کنیم','قوی‌ترین شاهد مخالف و حداقل یک توضیح رقیب وقتی مهم است بررسی می‌شود.'),
 ('چند سناریو را باز نگه می‌داریم','نتیجه مجبور نیست فقط صعودی یا نزولی باشد؛ رنج، نامشخص، رویدادی و عدم معامله هم معتبرند.'),
 ('فقط با شواهد کافی تصمیم می‌گیریم','جهت بازار با کیفیت فرصت یکی نیست و UNKNOWN یک جواب معتبر است.'),
 ('نتیجه تاریخ انقضا دارد','با تغییر محرک، شواهد یا رویداد مهم، تحلیل باید دوباره بررسی شود.')
]
PHILOSOPHY=[
 ('واقعیت قبل از داستان','اگر داستان بازار را حذف کنیم، داده و روابطی که هنوز می‌مانند وزن بیشتری دارند.'),
 ('شک و فرضیه رقیب','اگر نتیجه فقط با یک توضیح کار کند و توضیح رقیب معتبر داشته باشد، شکننده‌تر است.'),
 ('شکنندگی و چیزهایی که نمی‌دانیم','حذف منبع یا مدل، وابستگی مشترک، داده‌های ناموجود و ریسک‌های غیرخطی بررسی می‌شوند.'),
 ('تصمیم بدون اجبار به پیش‌بینی','عدم معامله یا نامشخص می‌تواند نتیجه علمی خوب باشد. این بخش جهت بازار را تعیین نمی‌کند.')
]

CSS=r''':root{--bg:#eee8dc;--paper:#fffdf8;--ink:#181612;--muted:#746d62;--line:#d7cdbd;--gold:#987438;--dark:#11110f;--focus:#b58b43;--soft:#f5efe4;--radius:12px;--motion:150ms}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 18% 0,#fbf7ee 0,transparent 38rem),linear-gradient(145deg,#e9e2d6,#f7f3ea 48%,#ece5da);color:var(--ink);font-family:Tahoma,"Segoe UI",sans-serif;line-height:1.9}.skip{position:absolute;inset-inline-start:-9999px}.skip:focus{inset-inline-start:12px;top:12px;background:#fff;padding:8px 12px;z-index:100}.app{display:grid;grid-template-columns:232px minmax(0,1fr);direction:ltr;min-height:100vh}.rail{direction:rtl;position:sticky;top:0;height:100vh;overflow:auto;background:var(--dark);color:#eee8dc;padding:20px 13px;border-left:1px solid #2d2d28}.brand{padding:3px 7px 17px;border-bottom:1px solid #30312b}.brand b{direction:ltr;font-family:Georgia,serif;color:#d4b981;letter-spacing:.12em}.brand h1{font-size:21px;margin:6px 0 0}.brand small{color:#8f887c}.nav-title{font-size:9px;color:#817a6f;margin:18px 9px 5px}.rail button{width:100%;border:0;background:transparent;color:#d8d1c5;text-align:right;padding:8px 10px;border-radius:7px;cursor:pointer}.rail button[aria-current="true"],.rail button:hover{background:#22231e;color:#fff}.rail button span{display:block;color:#8d867a;font-size:9px}.main{direction:rtl;min-width:0}.topbar{position:sticky;top:0;z-index:20;height:58px;background:rgba(248,244,236,.92);backdrop-filter:blur(16px);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px;padding:0 18px}.menu-btn{display:none}.search{flex:1;max-width:660px;border:1px solid var(--line);background:var(--paper);border-radius:8px;padding:8px 11px}.top-meta{margin-inline-start:auto;color:var(--muted);font-size:10px}.content{width:min(1280px,94%);margin:auto;padding-bottom:80px}.command{padding:34px 0 24px;border-bottom:1px solid var(--line)}.eyebrow{color:var(--gold);font-size:9px;font-weight:900;letter-spacing:.11em}.command-head{display:flex;justify-content:space-between;gap:28px;align-items:end}.command h2{font-size:clamp(28px,4vw,50px);line-height:1.15;margin:4px 0 8px}.command .brief{max-width:900px;color:#514c44;margin:0}.brief-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:17px}.brief-grid article{border-top:1px solid var(--line);padding-top:9px}.brief-grid span{display:block;color:var(--gold);font-size:9px}.brief-grid p{margin:3px 0;font-size:12px}.market-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0;margin-top:22px;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.market-tile{appearance:none;border:0;border-left:1px solid var(--line);background:transparent;text-align:right;padding:13px 10px;cursor:pointer;min-width:0}.market-tile:last-child{border-left:0}.market-tile[aria-current="true"]{background:rgba(255,253,248,.66)}.market-tile b{display:block;font-family:Georgia,serif;direction:ltr;text-align:right}.market-tile span{display:block;font-size:10px;color:#4f4b44}.market-tile small{display:block;color:var(--muted);font-size:8px}.workspace{padding:34px 0}.workspace-head{display:grid;grid-template-columns:1.4fr .6fr;gap:30px;align-items:start}.workspace-title h2{font-family:Georgia,serif;direction:ltr;text-align:right;font-size:42px;margin:1px 0}.workspace-title p{max-width:780px;color:#514c44}.decision{border-right:3px solid var(--gold);padding-right:14px}.decision span{display:block;color:var(--muted);font-size:9px}.decision b{display:block;font-size:18px;margin-bottom:7px}.state-strip{display:flex;flex-wrap:wrap;gap:18px;padding:14px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-top:18px}.state-strip div{min-width:110px}.state-strip span{display:block;color:var(--muted);font-size:9px}.state-strip b{font-size:11px}.what-matters{font-size:18px;max-width:900px;margin:25px 0}.drivers{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-bottom:20px}.drivers article{border-top:1px solid var(--line);padding-top:9px}.drivers span{font-size:9px;color:var(--gold)}.drivers p{font-size:12px;margin:3px 0}.kiu{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:22px 0}.kiu article{padding:16px 15px;border-left:1px solid var(--line)}.kiu article:last-child{border-left:0}.kiu h3{font-size:13px;margin:0 0 6px}.kiu p{font-size:11px;margin:0;color:#555047}.kiu .unknown h3{color:#6f6962}.delta{background:var(--soft);border-right:3px solid var(--gold);padding:12px 14px;margin:20px 0}.delta h3{font-size:12px;margin:0}.delta ul{font-size:11px;margin:5px 0;padding-right:17px}.section-heading{margin:30px 0 10px}.section-heading h3{font-size:23px;margin:2px 0}.section-heading p{color:var(--muted);font-size:11px;margin:0}.lens-index{border-top:1px solid var(--line)}.lens-row{width:100%;appearance:none;border:0;background:transparent;display:grid;grid-template-columns:230px 110px 1fr 90px;gap:14px;align-items:center;text-align:right;padding:13px 4px;border-bottom:1px solid var(--line);cursor:pointer}.lens-row:hover{background:rgba(255,253,248,.5)}.lens-title{font-weight:800;font-size:12px}.lens-state{font-size:10px;color:var(--gold)}.lens-summary{font-size:11px;color:#504c45}.lens-more{font-size:9px;color:var(--muted)}.scenario-tabs{display:flex;gap:5px;overflow:auto;padding-bottom:6px}.scenario-tab{border:1px solid var(--line);background:transparent;border-radius:999px;padding:6px 10px;white-space:nowrap;cursor:pointer;font-size:10px}.scenario-tab[aria-selected="true"]{background:var(--dark);color:#fff;border-color:var(--dark)}.scenario-canvas{margin-top:10px;border-top:1px solid var(--line);padding:18px 0}.scenario-canvas h4{font-size:20px;margin:0}.scenario-canvas .material{color:var(--gold);font-size:9px}.scenario-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:13px}.scenario-grid div{border-top:1px solid var(--line);padding-top:7px}.scenario-grid span{display:block;color:var(--muted);font-size:9px}.scenario-grid p{font-size:11px;margin:3px 0}.editorial{padding:38px 0;border-top:1px solid var(--line)}.editorial h2{font-size:28px;margin:2px 0 16px}.steps{max-width:800px;border-right:1px solid var(--line);padding-right:22px}.step{position:relative;margin:0 0 22px}.step:before{content:"";position:absolute;right:-27px;top:10px;width:9px;height:9px;border-radius:50%;background:var(--gold)}.step b{display:block}.step p{font-size:11px;color:#565149;margin:4px 0}.philosophy{display:grid;grid-template-columns:1fr 1fr;gap:24px}.philosophy article{border-top:1px solid var(--line);padding-top:10px}.philosophy b{color:var(--gold)}.philosophy p{font-size:11px;color:#565149}.quality{display:grid;grid-template-columns:repeat(4,1fr);gap:15px}.quality article{border-top:1px solid var(--line);padding-top:8px}.quality span{display:block;color:var(--gold);font-size:9px}.quality p{font-size:11px;margin:3px 0}.drawer-backdrop{position:fixed;inset:0;background:#0008;backdrop-filter:blur(4px);z-index:39;display:none}.drawer-backdrop[data-open="true"]{display:block}.drawer{position:fixed;z-index:40;inset:0 0 0 auto;width:min(720px,94vw);background:var(--paper);box-shadow:-30px 0 80px #0004;transform:translateX(105%);transition:transform var(--motion);overflow:auto}.drawer[data-open="true"]{transform:none}.drawer-head{position:sticky;top:0;background:#fffdf8f2;backdrop-filter:blur(10px);border-bottom:1px solid var(--line);padding:16px 20px;display:flex;justify-content:space-between;align-items:start}.drawer-head h2{font-size:24px;margin:2px 0}.close{border:0;background:#eee5d7;width:34px;height:34px;border-radius:50%;cursor:pointer;font-size:20px}.drawer-body{padding:18px 20px 50px}.deep-lead{background:var(--soft);border-right:3px solid var(--gold);padding:13px;margin-bottom:12px}.deep-section{padding:13px 0;border-top:1px solid var(--line)}.deep-section h3{font-size:13px;margin:0 0 5px}.deep-section p,.deep-section li{font-size:11px;color:#504c45}.deep-section ul{margin:0;padding-right:18px}.search-results{position:absolute;top:49px;right:18px;width:min(650px,calc(100vw - 36px));background:var(--paper);border:1px solid var(--line);box-shadow:0 15px 45px #0002;display:none;max-height:60vh;overflow:auto}.search-results[data-open="true"]{display:block}.search-hit{width:100%;border:0;background:transparent;text-align:right;padding:10px 12px;border-bottom:1px solid var(--line);cursor:pointer}.search-hit b{display:block;font-size:11px}.search-hit span{font-size:9px;color:var(--muted)}:focus-visible{outline:3px solid var(--focus);outline-offset:3px}@media(max-width:900px){.app{display:block}.rail{position:fixed;z-index:50;inset:0 auto 0 0;width:min(280px,82vw);transform:translateX(-105%);transition:transform var(--motion)}.rail[data-open="true"]{transform:none}.menu-btn{display:inline-block;border:1px solid var(--line);background:var(--paper);padding:6px 9px;border-radius:7px}.top-meta{display:none}.market-strip{display:flex;overflow:auto}.market-tile{min-width:210px;border-left:1px solid var(--line)}.workspace-head{grid-template-columns:1fr}.drivers,.kiu,.philosophy,.quality{grid-template-columns:1fr}.kiu article{border-left:0;border-bottom:1px solid var(--line)}.lens-row{grid-template-columns:1fr 100px;gap:4px}.lens-summary{grid-column:1/-1}.lens-more{display:none}.drawer{inset:auto 0 0 0;width:100%;height:92vh;transform:translateY(105%);border-radius:14px 14px 0 0}.drawer[data-open="true"]{transform:none}.brief-grid,.scenario-grid{grid-template-columns:1fr}.content{width:94%}}@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}@media print{.rail,.topbar,.drawer,.drawer-backdrop,.scenario-tabs{display:none!important}.app{display:block}.content{width:100%;max-width:none}.command,.workspace,.editorial{break-inside:auto}.lens-row{break-inside:avoid}.scenario-canvas{display:block}.search-results{display:none!important}}'''

JS=r'''(()=>{const D=JSON.parse(document.getElementById('public-data').textContent),$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)],esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));let mi=0,si=0;const market=()=>D.markets[mi];function list(a,empty='مورد مهمی ثبت نشده است.'){a=(a||[]).filter(Boolean);return '<ul>'+((a.length?a:[empty]).map(x=>'<li>'+esc(x)+'</li>').join(''))+'</ul>'}function renderStrip(){const h=D.markets.map((m,i)=>`<button class="market-tile" data-mi="${i}" aria-current="${i===mi}"><b><bdi>${esc(m.symbol)}</bdi></b><span>${esc(m.direction)}</span><small>${esc(m.action)} · ${esc(m.delta_label||'بدون مقایسه')}</small></button>`).join('');$('#market-strip').innerHTML=h;$$('.market-tile').forEach(b=>b.onclick=()=>{mi=+b.dataset.mi;si=0;render()})}function renderWorkspace(){const m=market();$('#ws-symbol').textContent=m.symbol;$('#ws-name').textContent=m.name||'';$('#ws-summary').textContent=m.summary||'';$('#ws-direction').textContent=m.direction;$('#ws-action').textContent=m.action;$('#ws-metrics').innerHTML=[['قدرت نیرو',m.force],['مصرف',m.consumption],['فشار باقی‌مانده',m.remaining],['دوام',m.persistence],['ریسک برگشت',m.reversal]].map(x=>`<div><span>${x[0]}</span><b>${esc(x[1])}</b></div>`).join('');$('#what-matters').textContent=m.what_matters;$('#drivers').innerHTML=[['نیروی اصلی',m.primary],['نیروی دوم',m.secondary],['قوی‌ترین نیروی مخالف',m.opposing]].map(x=>`<article><span>${x[0]}</span><p>${esc(x[1])}</p></article>`).join('');$('#kiu').innerHTML=`<article><h3>می‌دانیم</h3><p>${esc((m.known||[]).join(' '))}</p></article><article><h3>برداشت فعلی</h3><p>${esc((m.interpretation||[]).join(' '))}</p></article><article class="unknown"><h3>هنوز نمی‌دانیم</h3><p>${esc((m.unknowns||[]).join(' '))}</p></article>`;$('#delta').innerHTML='<h3>از بررسی قبلی چه تغییر کرده؟</h3>'+list(m.changes,m.delta_empty);$('#lens-index').innerHTML=m.lenses.map((x,i)=>`<button class="lens-row" data-li="${i}" aria-haspopup="dialog"><span class="lens-title">${esc(x.title)}</span><span class="lens-state">${esc(x.effect)}</span><span class="lens-summary">${esc(x.summary)}</span><span class="lens-more">جزئیات ←</span></button>`).join('');$$('.lens-row').forEach(b=>b.onclick=()=>openDrawer(+b.dataset.li));renderScenarioTabs();renderScenario()}function renderScenarioTabs(){const m=market();$('#scenario-tabs').innerHTML=m.scenarios.map((s,i)=>`<button class="scenario-tab" role="tab" data-si="${i}" aria-selected="${i===si}">${esc(s.label)}</button>`).join('');$$('.scenario-tab').forEach(b=>b.onclick=()=>{si=+b.dataset.si;renderScenarioTabs();renderScenario()})}function renderScenario(){const s=market().scenarios[si]||{};$('#scenario-canvas').innerHTML=`<span class="eyebrow">${s.material?'سناریوی قابل بررسی':'در حال حاضر سناریوی مهمی نیست'}</span><h4>${esc(s.label||'سناریو')}</h4><div class="scenario-grid"><div><span>چه شرایطی آن را فعال می‌کند؟</span>${list(s.conditions)}</div><div><span>الان چه شواهدی به نفع آن وجود دارد؟</span>${list(s.support)}</div><div><span>چه چیزی هنوز کم است؟</span>${list(s.missing)}</div><div><span>مسیر مورد انتظار</span><p>${esc(s.path)}</p></div><div><span>چه چیزی آن را باطل می‌کند؟</span>${list(s.invalidation)}</div><div><span>افق</span><p>${esc(s.horizon)}</p></div></div>`}function sec(h,a){return `<section class="deep-section"><h3>${h}</h3>${Array.isArray(a)?list(a):`<p>${esc(a)}</p>`}</section>`}function openDrawer(i){const x=market().lenses[i].deep||{};$('#drawer-title').textContent=market().lenses[i].title;$('#drawer-body').innerHTML=`<div class="deep-lead"><b>نتیجه ساده</b><p>${esc(x.result)}</p></div>${sec('چه چیزی مشاهده شده؟',x.observations)}${sec('چرا مهم است؟',x.why)}${sec('شواهد موافق',x.support)}${sec('شواهد مخالف',x.opposition)}${sec('چه چیزی هنوز نمی‌دانیم؟',x.unknowns)}${sec('این عامل چگونه روی بازار اثر می‌گذارد؟',x.mechanism)}${sec('این رابطه چقدر قطعی است؟',x.causal_strength)}${sec('توضیح رقیب',x.rival)}${sec('چه چیزی تحلیل را تغییر می‌دهد؟',x.invalidation)}${sec('اگر اشتباه باشیم، محتمل‌ترین دلیل چیست؟',x.failure_mode)}`;$('#drawer').dataset.open='true';$('#drawer').setAttribute('aria-hidden','false');$('#drawer-backdrop').dataset.open='true';$('#drawer-close').focus()}function closeDrawer(){delete $('#drawer').dataset.open;$('#drawer').setAttribute('aria-hidden','true');delete $('#drawer-backdrop').dataset.open}function render(){renderStrip();renderWorkspace();$$('.rail [data-mi]').forEach(b=>b.setAttribute('aria-current',String(+b.dataset.mi===mi)))}function renderRail(){const nav=D.markets.map((m,i)=>`<button data-mi="${i}" aria-current="${i===0}"><bdi>${esc(m.symbol)}</bdi><span>${esc(m.direction)}</span></button>`).join('');$('#rail-markets').innerHTML=nav;$$('#rail-markets [data-mi]').forEach(b=>b.onclick=()=>{mi=+b.dataset.mi;si=0;render();window.scrollTo({top:$('#workspace').offsetTop-60,behavior:'smooth'});closeMenu()})}function closeMenu(){delete $('#rail').dataset.open}function search(q){q=q.trim().toLowerCase();if(!q){delete $('#search-results').dataset.open;return}const hits=[];D.markets.forEach((m,i)=>{if((m.symbol+' '+m.name+' '+m.summary).toLowerCase().includes(q))hits.push({i,label:m.symbol,sub:m.direction});m.lenses.forEach((x,j)=>{if((x.title+' '+x.summary).toLowerCase().includes(q))hits.push({i,j,label:m.symbol+' · '+x.title,sub:x.summary})})});$('#search-results').innerHTML=hits.slice(0,20).map((h,k)=>`<button class="search-hit" data-k="${k}"><b>${esc(h.label)}</b><span>${esc(h.sub)}</span></button>`).join('');$('#search-results').dataset.open='true';$$('.search-hit').forEach((b,k)=>b.onclick=()=>{const h=hits[k];mi=h.i;si=0;render();if(h.j!=null)openDrawer(h.j);delete $('#search-results').dataset.open;$('#search').value=''})}$('#drawer-close').onclick=closeDrawer;$('#drawer-backdrop').onclick=closeDrawer;$('#menu-btn').onclick=()=>{$('#rail').dataset.open='true'};$('#search').oninput=e=>search(e.target.value);document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeDrawer();closeMenu();delete $('#search-results').dataset.open}if(e.key==='/'&&document.activeElement!==$('#search')){e.preventDefault();$('#search').focus()}});renderRail();render();})();'''

def _clean_list(xs,limit=5):
    out=[]
    for x in xs or []:
        if x is None: continue
        s=str(x).strip()
        if s and s not in out: out.append(s)
        if len(out)>=limit: break
    return out

def _role_key(role):
    s=str(role or '').upper()
    if any(x in s for x in ('BASE','CENTRAL','PRIMARY','MAIN')): return 'BASE'
    if any(x in s for x in ('BULL','UPSIDE','UP')): return 'UPSIDE'
    if any(x in s for x in ('BEAR','DOWNSIDE','DOWN')): return 'DOWNSIDE'
    if any(x in s for x in ('REVERS','FAIL','BREAK')): return 'REVERSAL'
    if any(x in s for x in ('RANGE','NEUTRAL','NO_EDGE','UNRESOLVED')): return 'RANGE'
    if any(x in s for x in ('EVENT','BINARY','SHOCK')): return 'EVENT'
    if any(x in s for x in ('NO_TRADE','NO TRADE','WAIT')): return 'NO_TRADE'
    if any(x in s for x in ('TAIL','RARE')): return 'RARE_SHOCK'
    return None

def _scenario_slots(model):
    src=model.get('layer2',{}).get('scenarios') or model.get('scenarios') or []
    by={}
    for s in src:
        k=_role_key(s.get('role') or s.get('role_fa') or s.get('direction'))
        if k and k not in by: by[k]=s
    out=[]
    for key,label in SCENARIO_ROLES:
        s=by.get(key)
        if not s:
            out.append({'key':key,'label':label,'material':False,'conditions':[],'support':[],'missing':['برای فعال شدن این سناریو شواهد کافی ثبت نشده است.'],'path':'در حال حاضر مسیر مهمی نیست.','invalidation':[],'horizon':'نامشخص'})
        else:
            out.append({'key':key,'label':label,'material':True,'conditions':_clean_list(s.get('conditions') or s.get('required_conditions')),'support':_clean_list(s.get('confirmation') or s.get('confirmation_triggers')),'missing':[],'path':str(s.get('direction_fa') or s.get('direction') or 'مسیر کیفی هنوز نامشخص است.'),'invalidation':_clean_list(s.get('invalidation') or s.get('invalidation_triggers')),'horizon':str(s.get('horizon') or 'نامشخص')})
    return out

def _lens_records(model):
    cards={x.get('section_id'):x for x in model.get('layer2',{}).get('cards',[]) if isinstance(x,dict)}
    deep=model.get('layer3',{}).get('sections',{}) or {}
    out=[]
    for sid in LENS_ORDER:
        c=cards.get(sid,{})
        d=deep.get(sid,{}) if isinstance(deep,dict) else {}
        observations=_clean_list(d.get('observations_fa'),6)
        why=_clean_list(d.get('why_it_matters_fa'),5)
        support=_clean_list(d.get('support_fa'),6)
        opposition=_clean_list(d.get('opposition_fa'),6)
        unknowns=_clean_list(d.get('unknowns_fa'),6)
        mechanism=_clean_list(d.get('mechanism_fa'),6)
        invalid=_clean_list(d.get('invalidation_fa'),6)
        out.append({
          'id':sid,'title':LENS_TITLES[sid],
          'effect':c.get('relation_fa') or c.get('state_fa') or 'نامشخص',
          'summary':c.get('summary_fa') or d.get('simple_result_fa') or 'داده کافی نداریم.',
          'deep':{
            'result':d.get('simple_result_fa') or c.get('summary_fa') or 'داده کافی نداریم.',
            'observations':observations,'why':why,'support':support,'opposition':opposition,'unknowns':unknowns,
            'mechanism':mechanism or ['مکانیزم این بخش با شواهد فعلی به اندازه کافی مشخص نشده است.'],
            'causal_strength':d.get('relation_to_direction_fa') or 'رابطه با جهت فعلی هنوز قطعی نیست.',
            'rival':opposition[:2] or ['توضیح رقیب مهمی به‌طور صریح ثبت نشده است.'],
            'invalidation':invalid,'failure_mode':(unknowns[:2]+opposition[:2]) or ['تغییر شواهد اصلی یا یک عامل مشاهده‌نشده می‌تواند نتیجه را عوض کند.']
          }
        })
    return out

def _single_market(model):
    l1=model.get('layer1',{});l2=model.get('layer2',{});drv=l2.get('drivers',{});prs=l2.get('pressure',{});deep=model.get('layer3',{}).get('sections',{}) or {}
    observations=[];unknowns=[]
    for sid in LENS_ORDER:
        d=deep.get(sid,{}) if isinstance(deep,dict) else {}
        observations += _clean_list(d.get('observations_fa'),1)
        unknowns += _clean_list(d.get('unknowns_fa'),1)
    changes=l2.get('changes',{}) or {}
    return {
      'symbol':str(model.get('header',{}).get('subject') or 'MARKET'),'name':'',
      'summary':str(l1.get('focus',{}).get('answer_fa') or l1.get('what_matters_now_fa') or ''),
      'direction':str(l1.get('direction_fa') or 'نامشخص'),'action':str(l1.get('permission_fa') or 'نامشخص'),
      'force':str(l1.get('force_fa') or 'نامشخص'),'consumption':str(l1.get('consumption_fa') or 'نامشخص'),
      'remaining':str(l1.get('remaining_pressure_fa') or 'نامشخص'),'persistence':str(l1.get('persistence_fa') or 'نامشخص'),
      'reversal':str(l1.get('reversal_risk_fa') or 'نامشخص'),'what_matters':str(l1.get('what_matters_now_fa') or ''),
      'primary':str(drv.get('primary_fa') or 'نامشخص'),'secondary':str(drv.get('secondary_fa') or 'نامشخص'),'opposing':str(drv.get('opposing_fa') or 'نامشخص'),
      'known':_clean_list(observations,3),'interpretation':_clean_list([l1.get('what_matters_now_fa'),drv.get('primary_fa')],3),'unknowns':_clean_list(unknowns,3) or ['UNKNOWN مهمی به‌طور صریح ثبت نشده است.'],
      'changes':_clean_list(changes.get('items'),8) if changes.get('has_comparison') else [],
      'delta_label':'تغییرات موجود' if changes.get('has_comparison') else 'بدون مقایسه معتبر','delta_empty':changes.get('empty_message_fa') or 'مقایسه معتبر با اجرای قبلی در دسترس نیست.',
      'lenses':_lens_records(model),'scenarios':_scenario_slots(model)
    }

def public_payload(model):
    # Support a future multi-market public model while keeping the canonical single-run path backwards compatible.
    markets=model.get('ux3_markets') if isinstance(model.get('ux3_markets'),list) else None
    if not markets:
        markets=[_single_market(model)]
    else:
        # The multi-market producer is responsible for already-sanitized records; never carry audit/internal metadata into HTML.
        safe=[]
        for m in markets:
            safe.append({k:m.get(k) for k in ('symbol','name','summary','direction','action','force','consumption','remaining','persistence','reversal','what_matters','primary','secondary','opposing','known','interpretation','unknowns','changes','delta_label','delta_empty','lenses','scenarios')})
        markets=safe
    mh=model.get('method_health') or {};pers=model.get('perspective') or {};header=model.get('header') or {}
    return {
      'product':'Alpha Desk','as_of':str(header.get('as_of') or ''),'horizon':str(header.get('horizon') or ''),
      'cross_market':model.get('ux3_cross_market') or {'brief':'یک بازار در این گزارش قرار دارد. برای نمای شش‌بازاری از اجرای multi-market استفاده کنید.','driver':markets[0].get('primary'),'opposition':markets[0].get('opposing'),'next_review':model.get('layer1',{}).get('next_review_fa')},
      'markets':markets,
      'thinking_guide':[{'title':a,'text':b} for a,b in THINKING_GUIDE],
      'philosophy':[{'title':a,'text':b} for a,b in PHILOSOPHY],
      'fragility':_clean_list(pers.get('material_findings_fa'),8),
      'quality':{'summary':str(mh.get('simple_summary_fa') or 'وضعیت کیفیت تحلیل به‌صورت ساده در این گزارش نمایش داده می‌شود.'),'limitations':_clean_list(mh.get('material_gaps'),8)}
    }

def explorer_html(model,view='EXPLORER'):
    data=public_payload(model); blob=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    subject=html.escape(str((data.get('markets') or [{}])[0].get('symbol') or 'Alpha Desk'))
    cg=data.get('cross_market') or {}
    steps=''.join(f'<div class="step"><b>{html.escape(x["title"])}</b><p>{html.escape(x["text"])}</p></div>' for x in data['thinking_guide'])
    phil=''.join(f'<article><b>{html.escape(x["title"])}</b><p>{html.escape(x["text"])}</p></article>' for x in data['philosophy'])
    limitations=data['quality'].get('limitations') or []
    lim=' '.join(html.escape(str(x)) for x in limitations) if limitations else 'محدودیت مهمی در سطح کاربر ثبت نشده است؛ UNKNOWNهای هر بخش داخل همان بازار نمایش داده می‌شوند.'
    return f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="color-scheme" content="light"><title>Alpha Desk — {subject}</title><style>{CSS}</style></head><body><a class="skip" href="#workspace">رفتن به محتوای اصلی</a><div class="app"><aside class="rail" id="rail" aria-label="ناوبری"><div class="brand"><b>ALPHA DESK</b><h1>پژوهش بازار</h1><small>خروجی زنده و چندسناریویی</small></div><div class="nav-title">بازارها</div><div id="rail-markets"></div><div class="nav-title">بخش‌ها</div><button onclick="document.getElementById('workspace').scrollIntoView()">تحلیل بازار</button><button onclick="document.getElementById('thinking').scrollIntoView()">منطق تحلیل</button><button onclick="document.getElementById('philosophy').scrollIntoView()">فلسفه و شکنندگی</button><button onclick="document.getElementById('quality').scrollIntoView()">کیفیت و محدودیت‌ها</button></aside><main class="main"><header class="topbar"><button class="menu-btn" id="menu-btn" aria-label="باز کردن منو">منو</button><input class="search" id="search" placeholder="جست‌وجوی بازار یا بُعد تحلیلی…" aria-label="جست‌وجو"><div class="top-meta"><bdi>{html.escape(data.get('as_of',''))}</bdi></div><div class="search-results" id="search-results"></div></header><div class="content"><section class="command"><div class="command-head"><div><span class="eyebrow">ALPHA DESK · نتیجه فوری</span><h2>تصویر فعلی بازار</h2><p class="brief">{html.escape(str(cg.get('brief') or ''))}</p></div></div><div class="brief-grid"><article><span>عامل اصلی</span><p>{html.escape(str(cg.get('driver') or 'نامشخص'))}</p></article><article><span>قوی‌ترین نیروی مخالف</span><p>{html.escape(str(cg.get('opposition') or 'نامشخص'))}</p></article><article><span>بررسی بعدی</span><p>{html.escape(str(cg.get('next_review') or 'نامشخص'))}</p></article></div><div class="market-strip" id="market-strip" aria-label="انتخاب بازار"></div></section><section class="workspace" id="workspace"><div class="workspace-head"><div class="workspace-title"><span class="eyebrow" id="ws-name"></span><h2 id="ws-symbol"></h2><p id="ws-summary"></p></div><div class="decision"><span>جهت فعلی</span><b id="ws-direction"></b><span>اقدام</span><b id="ws-action"></b></div></div><div class="state-strip" id="ws-metrics"></div><p class="what-matters" id="what-matters"></p><div class="drivers" id="drivers"></div><div class="kiu" id="kiu"></div><div class="delta" id="delta"></div><div class="section-heading"><span class="eyebrow">تصویر کامل تحلیل</span><h3>هشت بُعد مستقل</h3><p>هر ردیف فقط نتیجه اصلی همان بُعد را نشان می‌دهد؛ جزئیات با یک Drawer مشترک باز می‌شود.</p></div><div class="lens-index" id="lens-index"></div><div class="section-heading"><span class="eyebrow">چند سناریو باز می‌ماند</span><h3>مسیرهای ممکن</h3><p>سناریوها احتمال عددی ساختگی ندارند و فقط با شواهد قابل مشاهده تغییر می‌کنند.</p></div><div class="scenario-tabs" id="scenario-tabs" role="tablist"></div><div class="scenario-canvas" id="scenario-canvas"></div></section><section class="editorial" id="thinking"><span class="eyebrow">راهنمای منطق تحلیل</span><h2>چطور این تحلیل را بخوانیم؟</h2><div class="steps">{steps}</div></section><section class="editorial" id="philosophy"><span class="eyebrow">دیدگاه فلسفی</span><h2>چطور با عدم قطعیت و شکنندگی برخورد می‌کنیم؟</h2><p class="brief">این بخش جهت بازار را تعیین نمی‌کند؛ فقط بررسی می‌کند نتیجه فعلی به منبع، داستان، مدل یا شوک‌های پنهان چقدر وابسته است.</p><div class="philosophy">{phil}</div></section><section class="editorial" id="quality"><span class="eyebrow">کیفیت و محدودیت‌ها</span><h2>چه چیزهایی را باید درباره کیفیت نتیجه بدانیم؟</h2><div class="quality"><article><span>وضعیت کلی</span><p>{html.escape(data['quality']['summary'])}</p></article><article><span>کجا داده ناقص است؟</span><p>{lim}</p></article><article><span>اثر نقص داده</span><p>داده ناقص به خنثی تبدیل نمی‌شود و در صورت اهمیت، کیفیت فرصت یا اقدام را محدود می‌کند.</p></article><article><span>اصل استفاده</span><p>کیفیت فرایند تحلیل با قطعیت بازار یکی نیست؛ نامشخص و عدم معامله نتیجه‌های معتبرند.</p></article></div></section></div></main></div><div class="drawer-backdrop" id="drawer-backdrop"></div><aside class="drawer" id="drawer" role="dialog" aria-modal="true" aria-hidden="true" aria-labelledby="drawer-title"><div class="drawer-head"><div><span class="eyebrow">جزئیات کامل این بخش</span><h2 id="drawer-title">تحلیل عمیق</h2></div><button class="close" id="drawer-close" aria-label="بستن">×</button></div><div class="drawer-body" id="drawer-body"></div></aside><script id="public-data" type="application/json">{blob}</script><script>{JS}</script></body></html>'''

def render_files(out_dir,model,profile='EXPLORER'):
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True);rid=model.get('audit',{}).get('run_id') or 'ALPHA_DESK_RUN';stem=rid+'_'+profile.lower();jp=out/(stem+'.report.json');hp=out/(stem+'.html');jp.write_text(json.dumps(model,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8');hp.write_text(explorer_html(model,profile),encoding='utf-8')
    return {'report_model_path':str(jp),'html_path':str(hp),'pdf_path':None,'profile':profile,'ux_version':UX_VERSION}

def render_pdf_from_html(html_path,pdf_path):
    candidates=[shutil.which('msedge'),shutil.which('msedge.exe'),shutil.which('chrome'),shutil.which('chrome.exe'),shutil.which('chromium'),shutil.which('chromium-browser')]
    exe=next((x for x in candidates if x),None)
    if not exe:return {'status':'PENDING','reason':'NO_HEADLESS_BROWSER_FOUND','pdf_path':None}
    p=Path(pdf_path).resolve();u=Path(html_path).resolve().as_uri();q=subprocess.run([exe,'--headless','--disable-gpu','--no-pdf-header-footer','--print-to-pdf='+str(p),u],capture_output=True,text=True,timeout=120)
    return {'status':'PASS' if q.returncode==0 and p.is_file() else 'FAIL','pdf_path':str(p) if p.is_file() else None,'stderr':q.stderr[-2000:]}
