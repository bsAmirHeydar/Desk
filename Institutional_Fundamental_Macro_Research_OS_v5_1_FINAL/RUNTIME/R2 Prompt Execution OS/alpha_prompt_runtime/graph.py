class GraphError(RuntimeError): pass

class ProcessGraph:
    def __init__(self,graph): self.graph=graph; self.nodes=graph['nodes']
    def validate(self):
        errs=[]
        for n,cfg in self.nodes.items():
            for d in cfg.get('dependencies',[]):
                if d not in self.nodes: errs.append(f'{n}: missing dep {d}')
        # kahn
        indeg={n:0 for n in self.nodes}; rev={n:[] for n in self.nodes}
        for n,cfg in self.nodes.items():
            for d in cfg.get('dependencies',[]): indeg[n]+=1; rev[d].append(n)
        q=[n for n,v in indeg.items() if v==0]; seen=[]
        while q:
            x=q.pop(0); seen.append(x)
            for y in rev[x]:
                indeg[y]-=1
                if indeg[y]==0:q.append(y)
        if len(seen)!=len(self.nodes): errs.append('process graph cycle')
        return errs
    def ready(self,status):
        ready=[]
        for n,cfg in self.nodes.items():
            if status.get(n,'PENDING')!='PENDING': continue
            if all(status.get(d) in ('COMPLETED','NOT_APPLICABLE','UNAVAILABLE','UNDETERMINED') for d in cfg.get('dependencies',[])): ready.append(n)
        return ready
    def stage(self,pid): return self.nodes[pid]['stage']
