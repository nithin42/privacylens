"""
privacylens — Open-source Python library to audit ML pipelines for privacy vulnerabilities.

Supports:
- Membership Inference Attack (MIA) testing
- PII leakage detection in model embeddings and predictions
- Model inversion risk scoring
- Works with scikit-learn, PyTorch, XGBoost
- CLI + Python API
"""

from __future__ import annotations

__version__ = "0.1.1"
__author__ = "Nithin"
__email__ = "kumbam.nithingoud@gmail.com"
__license__ = "MIT"

from privacylens.auditor import audit, AuditReport

__all__ = ["audit", "AuditReport", "__version__"]
