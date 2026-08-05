"""
privacylens — Open-source Python library to audit ML pipelines for privacy vulnerabilities.

Supports 5-Point Privacy Audit:
1. Membership Inference Attack (MIA) (Shokri et al., 2017)
2. PII Leakage Detection (Emails, SSNs, Credit Cards, Phones, IPs)
3. Model Inversion Risk Scoring (Fredrikson et al., 2015)
4. Attribute Inference Attack (Yeom et al., 2018)
5. Empirical Differential Privacy Epsilon (ε) Estimator (Jagielski et al., 2020)

Framework Adapters: scikit-learn, PyTorch, XGBoost, HuggingFace Transformers
Azure Integrations: Azure ML Pipeline Step, Azure OpenAI Deployment Auditor
Interactive HTML Compliance Reports & CLI + Python API
"""

from __future__ import annotations

__version__ = "1.1.0"
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
from privacylens.attacks.attribute import AttributeInferenceAuditor
from privacylens.attacks.inversion import ModelInversionAuditor
from privacylens.attacks.membership import MembershipInferenceAuditor
from privacylens.auditor import AuditReport, audit
from privacylens.integrations.azureml import AzureMLAuditStep, AzureOpenAIAuditor
from privacylens.leakage.dp import DPEpsilonAuditor
from privacylens.leakage.pii import PIILeakageAuditor
from privacylens.report.html import generate_html_report

__all__ = [
    "audit",
    "AuditReport",
    "MembershipInferenceAuditor",
    "PIILeakageAuditor",
    "ModelInversionAuditor",
    "AttributeInferenceAuditor",
    "DPEpsilonAuditor",
    "AzureMLAuditStep",
    "AzureOpenAIAuditor",
    "BaseModelAdapter",
    "SklearnAdapter",
    "PyTorchAdapter",
    "XGBoostAdapter",
    "HuggingFaceAdapter",
    "get_adapter",
    "generate_html_report",
    "__version__",
]
