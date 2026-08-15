from html import escape
def render(status,queue):
 items=''.join(f"<tr><td>{escape(str(x.get('priority')))}</td><td>{escape(str(x.get('failure_family')))}</td><td>{escape(str(x.get('counts',{}).get('true_forward_independent_episodes')))}</td><td>{escape(str(x.get('proposal_eligible')))}</td></tr>" for x in queue.get('items',[]))
 html="<!doctype html><html><head><meta charset='utf-8'><title>Alpha Desk V2 - Learning</title><style>body{font-family:Segoe UI,Arial;margin:40px;max-width:1100px}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ddd;padding:8px;text-align:left}.warn{padding:14px;background:#f5efe1}</style></head><body>"
 html+="<h1>Alpha Desk V2 - Scientific Learning</h1><div class='warn'>Learning output is non-authoritative. P09 cannot mutate Pressure, Transmission, Release, Permission, or broker state.</div>"
 html+=f"<p>Cases: {status.get('learning_cases')} - Hypotheses: {status.get('hypotheses')}</p><h2>Research queue</h2><table><tr><th>Priority</th><th>Failure hypothesis</th><th>TF episodes</th><th>Proposal eligible</th></tr>{items}</table></body></html>"
 return html
