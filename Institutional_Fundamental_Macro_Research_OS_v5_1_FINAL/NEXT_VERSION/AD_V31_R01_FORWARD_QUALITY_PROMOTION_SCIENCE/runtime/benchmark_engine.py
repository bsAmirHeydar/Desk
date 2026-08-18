from __future__ import annotations
import math

def rate(n,d):return (n/d) if d else None
def wilson_lower(success,n,z=1.96):
    if n<=0:return None
    p=success/n;den=1+z*z/n;center=p+z*z/(2*n);adj=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)
    return max(0.0,(center-adj)/den)
def direction_score(outcome):return {'ALIGNED':1.0,'NEUTRAL_BAND':0.5,'OPPOSED':0.0}.get(outcome)
