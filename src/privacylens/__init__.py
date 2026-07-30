"""
privacylens — Open-source Python library to audit ML pipelines for privacy vulnerabilities.

Supports:
- Membership Inference Attack (MIA) testing (Shokri et al., 2017)
- PII leakage detection in model embeddings and predictions
- Model inversion risk scoring (Fredrikson et al., 2015)
- Native Framework Adapters (scikit-learn, PyTorch, XGBoost, HuggingFace Transformers)
- Interactive HTML Compliance Report Generator (Jinja2)
- CLI + Python API
"""

from __future__ import annotations

__version__ = "1.0.0"
__author__ = "Nithin"
__email__ = "kumbam.nithingoud@gmail.com"
__license__ = "MIT"

from privacylens.adapters import (
    BaseModelAdapter,
    HuggingFaceAdapter,
    PyTorchAdapter,
    SklearnAdapter,
    XGBoostAdapter,
    get_adapter,
)
from privacylens.attacks.inversion import ModelInversionAuditor
from privacylens.attacks.membership import MembershipInferenceAuditor
from privacylens.auditor import AuditReport, audit
from privacylens.leakage.pii import PIILeakageAuditor
from privacylens.report.html import generate_html_report

__all__ = [
    "audit",
    "AuditReport",
    "MembershipInferenceAuditor",
    "PIILeakageAuditor",
    "ModelInversionAuditor",
    "BaseModelAdapter",
    "SklearnAdapter",
    "PyTorchAdapter",
    "XGBoostAdapter",
    "HuggingFaceAdapter",
    "get_adapter",
    "generate_html_report",
    "__version__",
]
