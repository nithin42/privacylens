"""
privacylens — Open-source Python library to audit ML pipelines for privacy vulnerabilities.

Supports:
- Membership Inference Attack (MIA) testing
- PII leakage detection in model embeddings and predictions
- Model inversion risk scoring (Fredrikson et al., 2015)
- Native Framework Adapters (scikit-learn, PyTorch, XGBoost)
- Interactive HTML Compliance Report Generator (Jinja2)
- CLI + Python API
"""

from __future__ import annotations

__version__ = "0.5.0"
__author__ = "Nithin"
__email__ = "kumbam.nithingoud@gmail.com"
__license__ = "MIT"

from privacylens.adapters import get_adapter, BaseModelAdapter
from privacylens.attacks.inversion import ModelInversionAuditor
from privacylens.attacks.membership import MembershipInferenceAuditor
from privacylens.auditor import audit, AuditReport
from privacylens.leakage.pii import PIILeakageAuditor
from privacylens.report.html import generate_html_report

__all__ = [
    "audit",
    "AuditReport",
    "MembershipInferenceAuditor",
    "PIILeakageAuditor",
    "ModelInversionAuditor",
    "BaseModelAdapter",
    "get_adapter",
    "generate_html_report",
    "__version__",
]
