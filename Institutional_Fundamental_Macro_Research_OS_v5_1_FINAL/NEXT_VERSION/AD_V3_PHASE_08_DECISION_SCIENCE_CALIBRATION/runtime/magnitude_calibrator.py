from __future__ import annotations
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.magnitude_engine import root_magnitude

def magnitude_from_root(root,rows,history=None,as_of=None):
    """Compatibility facade. R02 is the magnitude-science authority for P08."""
    return root_magnitude(root,rows,history,as_of)
