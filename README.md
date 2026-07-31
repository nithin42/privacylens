<div align="center">

# 🔍 privacylens

**Audit any ML model for privacy vulnerabilities — in 3 lines of code.**

[![CI](https://github.com/nithin42/privacylens/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/nithin42/privacylens/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)](https://github.com/nithin42/privacylens)
[![PyPI version](https://badge.fury.io/py/privacyaudit.svg?v=1.0.0)](https://pypi.org/project/privacyaudit/)
[![Python](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12-blue)](https://pypi.org/project/privacyaudit/)
[![Discussions](https://img.shields.io/github/discussions/nithin42/privacylens)](https://github.com/nithin42/privacylens/discussions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

---

## 🎯 What is privacylens?

Most ML engineers don't know if their model is **leaking private training data**. `privacylens` audits it.

```python
from privacylens import audit

report = audit(model, X_train, y_train, X_test)
report.summary()

# Export HTML Compliance Report for GDPR/HIPAA sharing
report.to_html("audit_report.html")
```

```
┌─────────────────────────────────────────────────────────────┐
│             🔍 privacylens — Privacy Audit Report            │
├──────────────────────────────┬────────────┬─────────────────┤
│ Check                        │ Score      │ Risk            │
├──────────────────────────────┼────────────┼─────────────────┤
│ Membership Inference Attack  │ 0.087      │ LOW             │
│ PII Leakage Detection        │ 0.000      │ LOW             │
│ Model Inversion Risk         │ 0.042      │ LOW             │
└──────────────────────────────┴────────────┴─────────────────┘

Model: RandomForestClassifier
Overall Risk: LOW

• MIA advantage score: 0.087 — model shows low Membership Inference vulnerability.
• PII leakage score: 0.000 — model shows low PII Leakage vulnerability.
• Model Inversion score: 0.042 — model shows low Model Inversion vulnerability.
```

---

## ✨ Features

- 🕵️ **Membership Inference Attack (MIA)** — Detect if an attacker can identify training records using shadow model estimation (Shokri et al., 2017)
- 🔎 **PII Leakage Detection** — Detect sensitive PII (Emails, SSNs, Credit Cards, Phones, IPs) memorized in predictions or samples
- 🔄 **Model Inversion Risk Scorer** — Evaluate feature reconstructability risk from output confidence probabilities (Fredrikson et al., 2015)
- 🌐 **Native Framework Adapters** — Out-of-the-box support for scikit-learn, PyTorch (`nn.Module`), XGBoost, and HuggingFace Transformers
- 📄 **HTML Compliance Reports** — Export standalone, interactive HTML reports (`--report audit.html`) for security & GDPR/HIPAA compliance sharing
- 🎨 **Beautiful terminal output** — Rich colour-coded risk tables with LOW / MEDIUM / HIGH classification
- 🤖 **CLI + Python API** — Use in scripts or integrate into CI/CD pipelines (`privacylens audit`)
- 📊 **JSON output** — Machine-readable results for dashboards and reporting (`--output json`)

---

## 📦 Installation

```bash
# Base install (scikit-learn models)
pip install privacyaudit

# With PyTorch support
pip install "privacyaudit[torch]"

# With XGBoost support
pip install "privacyaudit[xgboost]"

# Everything (PyTorch, XGBoost, Transformers)
pip install "privacyaudit[all]"
```

> **Note**: The PyPI package is `privacyaudit`. Import in Python as `from privacylens import audit`.

---

## 🚀 Quick Start

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from privacylens import audit

# Train a model
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Audit it for privacy vulnerabilities (MIA + PII Leakage + Model Inversion)
report = audit(model, X_train, y_train, X_test, y_test)
report.summary()

# Export interactive HTML audit report
report.to_html("compliance_report.html")

# Get audit results as dict (for JSON logging or API responses)
print(report.to_dict())
```

---

## 🖥️ CLI Usage

```bash
# Audit a saved model file
privacylens audit model.pkl train.csv test.csv

# Export interactive HTML report
privacylens audit model.pkl train.csv test.csv --report compliance.html

# Output JSON for CI/CD integration
privacylens audit model.pkl train.csv test.csv --output json

# Skip MIA check in fast pipelines
privacylens audit model.pkl train.csv test.csv --no-mia
```

---

## 🏗️ Architecture

```
privacylens/
├── src/privacylens/
│   ├── __init__.py         # Public API: audit(), AuditReport, Auditors, Adapters
│   ├── auditor.py          # Core orchestrator
│   ├── adapters/
│   │   ├── base.py         # BaseModelAdapter & get_adapter() factory
│   │   ├── sklearn_adapter.py
│   │   ├── pytorch_adapter.py
│   │   ├── xgboost_adapter.py
│   │   └── hf_adapter.py   # HuggingFace Transformers Adapter
│   ├── attacks/
│   │   ├── membership.py   # MIA engine (shadow model + attack classifier)
│   │   └── inversion.py    # Model Inversion Risk Auditor (Fredrikson et al.)
│   ├── leakage/
│   │   └── pii.py          # PII Leakage Auditor (Regex + Severity Weighting)
│   ├── report/
│   │   └── html.py         # HTML Compliance Report Generator (Jinja2)
│   └── cli.py              # Click CLI
├── examples/
│   └── benchmark_demo.py   # Flagship Enterprise Privacy Audit Benchmark
└── tests/
    ├── test_auditor.py
    ├── test_membership.py
    ├── test_pii_leakage.py
    ├── test_inversion.py
    ├── test_adapters.py
    ├── test_html_report.py
    └── test_hf_adapter.py
```

---

## 📖 Risk Score Interpretation

| Check Score | Risk Level | Meaning |
|---|---|---|
| `0.0 – 0.10` | 🟢 **LOW** | Model reveals minimal membership/PII/inversion information |
| `0.10 – 0.30` | 🟡 **MEDIUM** | Moderate risk — review training data exposure |
| `0.30 – 1.00` | 🔴 **HIGH** | Model likely memorising sensitive training data |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions welcome!

## 📄 License

MIT — see [LICENSE](LICENSE).
