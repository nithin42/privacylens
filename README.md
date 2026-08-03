<div align="center">

# 🔍 privacylens

**Audit any ML model for privacy vulnerabilities — in 3 lines of code.**

[![CI](https://github.com/nithin42/privacylens/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/nithin42/privacylens/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)](https://github.com/nithin42/privacylens)
[![PyPI version](https://badge.fury.io/py/privacyaudit.svg?v=1.0.1)](https://pypi.org/project/privacyaudit/)
[![Python](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12-blue)](https://pypi.org/project/privacyaudit/)
[![Discussions](https://img.shields.io/github/discussions/nithin42/privacylens)](https://github.com/nithin42/privacylens/discussions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

---

## 💡 Abstract (Executive Summary)

> **The Problem**: When Machine Learning models are trained on private data (like medical records, financial transactions, or customer emails), they can accidentally **memorize** that sensitive information. Attackers can then extract private data or determine if a specific person's record was in the training set.
> 
> **The Solution**: `privacylens` is an open-source privacy auditing toolkit. In **3 lines of code**, it runs **5 automated security checks** against any ML model (scikit-learn, PyTorch, XGBoost, HuggingFace) to detect data leakage risks before deployment.
> 
> **Why it matters**:
> - 🧑‍💻 **For Developers**: Catch privacy bugs automatically in CI/CD pipelines before pushing models to production.
> - 🏢 **For Enterprises**: Generate standalone interactive HTML compliance reports for GDPR and HIPAA audits.

---

## 🎯 What is privacylens?

Most ML engineers don't know if their model is **leaking private training data**. `privacylens` audits it across 5 core privacy vulnerability vectors.

```python
from privacylens import audit

report = audit(model, X_train, y_train, X_test)
report.summary()

# Export HTML Compliance Report for GDPR/HIPAA sharing
report.to_html("audit_report.html")
```

```text
+-------------------------------------------------------------------+
|             privacylens — 5-Point Privacy Audit Report            |
+------------------------------------+--------------+---------------+
| Check                              | Score        | Risk          |
+------------------------------------+--------------+---------------+
| Membership Inference Attack        | 0.087        | LOW           |
| PII Leakage Detection              | 0.000        | LOW           |
| Model Inversion Risk               | 0.042        | LOW           |
| Attribute Inference Risk           | 0.015        | LOW           |
| Differential Privacy (ε)           | 0.038        | LOW           |
+------------------------------------+--------------+---------------+

Model: RandomForestClassifier
Overall Risk: LOW

• MIA advantage score: 0.087 — model shows low Membership Inference vulnerability.
• PII leakage score: 0.000 — model shows low PII Leakage vulnerability.
• Model Inversion score: 0.042 — model shows low Model Inversion vulnerability.
• Attribute Inference score: 0.015 — model shows low Attribute Inference vulnerability.
• Differential Privacy score: 0.038 — model shows low Differential Privacy vulnerability.
```

---

## ✨ 5-Point Privacy Audit Suite

- 🕵️ **1. Membership Inference Attack (MIA)** — Detect if an attacker can identify training records using shadow model estimation (Shokri et al., 2017)
- 🔎 **2. PII Leakage Detection** — Scan predictions and samples for memorized PII (Emails, SSNs, Credit Cards, Phones, IPs)
- 🔄 **3. Model Inversion Risk Scorer** — Evaluate feature reconstructability risk from confidence probabilities (Fredrikson et al., 2015)
- 🎯 **4. Attribute Inference Attack** — Measure sensitive secondary attribute predictability from confidence vectors (Yeom et al., 2018)
- 🛡️ **5. Differential Privacy (ε) Estimator** — Estimate empirical privacy loss ($\epsilon$) under single-record modifications (Jagielski et al., 2020)
- 🌐 **Native Framework Adapters** — Out-of-the-box support for scikit-learn, PyTorch (`nn.Module`), XGBoost, and HuggingFace Transformers
- 📄 **HTML Compliance Reports** — Export standalone, interactive HTML reports (`--report audit.html`) for security & GDPR/HIPAA compliance sharing
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

# Audit it for all 5 privacy vulnerabilities
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
│   ├── auditor.py          # Core 5-point orchestrator
│   ├── adapters/
│   │   ├── base.py         # BaseModelAdapter & get_adapter() factory
│   │   ├── sklearn_adapter.py
│   │   ├── pytorch_adapter.py
│   │   ├── xgboost_adapter.py
│   │   └── hf_adapter.py   # HuggingFace Transformers Adapter
│   ├── attacks/
│   │   ├── membership.py   # MIA engine (Shokri et al.)
│   │   ├── inversion.py    # Model Inversion Risk Auditor (Fredrikson et al.)
│   │   └── attribute.py    # Attribute Inference Auditor (Yeom et al.)
│   ├── leakage/
│   │   ├── pii.py          # PII Leakage Auditor (Regex + Severity Weighting)
│   │   └── dp.py           # Empirical Differential Privacy Epsilon Estimator
│   ├── report/
│   │   └── html.py         # HTML Compliance Report Generator (Jinja2)
│   └── cli.py              # Click CLI
├── examples/
│   └── benchmark_demo.py   # Enterprise Privacy Audit Benchmark
└── tests/
    ├── test_auditor.py
    ├── test_membership.py
    ├── test_pii_leakage.py
    ├── test_inversion.py
    ├── test_adapters.py
    ├── test_html_report.py
    ├── test_hf_adapter.py
    └── test_5point_audits.py
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
