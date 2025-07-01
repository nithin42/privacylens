"""
privacylens — Open-source Python library to audit ML pipelines for privacy vulnerabilities.

Supports:
- Membership Inference Attack (MIA) testing
- PII leakage detection in model embeddings and predictions
- Model inversion risk scoring (Fredrikson et al., 2015)
- Works with scikit-learn, PyTorch, XGBoost
- CLI + Python API
"""

from __future__ import annotations

__version__ = "0.3.0"
__author__ = "Nithin"
__email__ = "kumbam.nithingoud@gmail.com"
__license__ = "MIT"

from privacylens.attacks.inversion import ModelInversionAuditor
from privacylens.attacks.membership import MembershipInferenceAuditor
from privacylens.auditor import audit, AuditReport
from privacylens.leakage.pii import PIILeakageAuditor

__all__ = [
    "audit",
    "AuditReport",
    "MembershipInferenceAuditor",
    "PIILeakageAuditor",
    "ModelInversionAuditor",
    "__version__",
]
