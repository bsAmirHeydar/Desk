#!/usr/bin/env python3
from __future__ import annotations
PHASE='AD-V2-P07'
def receipt(promotion_decision,policy,*,operator_approved=False):
    cls=promotion_decision.get('highest_eligible_class');validator=promotion_decision.get('independent_validator_approved') is True
    reasons=[]
    if cls not in set(policy.get('commissionable_classes',[])):reasons.append('PROMOTION_CLASS_NOT_COMMISSIONABLE')
    if policy.get('requires_independent_validator') and not validator:reasons.append('INDEPENDENT_VALIDATOR_NOT_APPROVED')
    if policy.get('requires_operator_approval') and not operator_approved:reasons.append('OPERATOR_APPROVAL_REQUIRED')
    # P07 only emits eligibility; it never mutates the closed V1 runtime by itself.
    commissioned=False
    status='COMMISSIONABLE_RECEIPT_ONLY' if not reasons else 'NOT_COMMISSIONED_TRUE_FORWARD_PENDING'
    return {'schema_version':'1.0.0','phase':PHASE,'record_type':'V2_COMMISSIONING_RECEIPT','status':status,'commissioned':commissioned,'reason_codes':reasons,'eligible_class':cls,'operator_approved':bool(operator_approved),'runtime_mutation_performed':False,'authority':{'v1_production':'UNCHANGED','trade_permission':'V1_INHERITED','positive_permission_creation':False,'broker':'NONE'}}
