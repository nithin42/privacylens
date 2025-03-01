<div align="center">

# 🔍 privacylens

**Audit any ML model for privacy vulnerabilities — in 3 lines of code.**

[![CI](https://github.com/nithin42/privacylens/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/nithin42/privacylens/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-89%25-brightgreen)](https://github.com/nithin42/privacylens)
[![PyPI version](https://badge.fury.io/py/privacyaudit.svg)](https://pypi.org/project/privacyaudit/)
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
```

```
┌─────────────────────────────────────────────────────────────┐
│             🔍 privacylens — Privacy Audit Report            │
├──────────────────────────────┬────────────┬─────────────────┤
│ Check                        │ Score      │ Risk            │
├──────────────────────────────┼────────────┼─────────────────┤
│ Membership Inference Attack  │ 0.087      │ LOW             │
└──────────────────────────────┴────────────┴─────────────────┘

Model: RandomForestClassifier
Overall Risk: LOW

• MIA advantage score: 0.087 — model shows low Membership Inference vulnerability.
```

---

## ✨ Features

- 🕵️ **Membership Inference Attack (MIA)** — Detect if an attacker can identify training records using a shadow model approach (Shokri et al., 2017)
- 🌐 **Framework agnostic** — Works with scikit-learn, XGBoost, and any model with `predict_proba()`
- 🎨 **Beautiful terminal output** — Rich colour-coded risk tables with LOW / MEDIUM / HIGH classification
- 🤖 **CLI + Python API** — Use in scripts or integrate into CI/CD pipelines
- 📊 **JSON output** — Machine-readable results for dashboards and reporting

**Coming in future releases:**
- 🔢 PII leakage detection in model embeddings
- 🔄 Model inversion risk scoring
- 🤗 HuggingFace Transformers adapter
- 📄 HTML compliance report export

---

## 📦 Installation

```bash
# Base install (scikit-learn models)
pip install privacyaudit

# With PyTorch support
pip install "privacyaudit[torch]"

# With XGBoost support
pip install "privacyaudit[xgboost]"

# Everything
pip install "privacyaudit[all]"
```

> **Note**: The PyPI package is `privacyaudit`. Import as `from privacylens import audit`.

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

# Audit it for privacy vulnerabilities
report = audit(model, X_train, y_train, X_test, y_test)
report.summary()

# Get results as dict (for JSON logging)
print(report.to_dict())
```

---

## 🖥️ CLI Usage

```bash
# Audit a saved model
privacylens audit model.pkl train.csv test.csv

# JSON output for CI/CD integration
privacylens audit model.pkl train.csv test.csv --output json

# Skip MIA check
privacylens audit model.pkl train.csv test.csv --no-mia
```

---

## 🏗️ Architecture

```
privacylens/
├── src/privacylens/
│   ├── __init__.py         # Public API: audit(), AuditReport
│   ├── auditor.py          # Main orchestrator
│   ├── attacks/
│   │   └── membership.py   # MIA engine (shadow model + attack classifier)
│   └── cli.py              # Click CLI
└── tests/
    ├── test_auditor.py
    └── test_membership.py
```

---

## 📖 Risk Score Interpretation

| MIA Score | Risk Level | Meaning |
|---|---|---|
| `0.0 – 0.10` | 🟢 **LOW** | Model reveals minimal membership information |
| `0.10 – 0.30` | 🟡 **MEDIUM** | Some memorisation risk — review training data |
| `0.30 – 1.00` | 🔴 **HIGH** | Model likely memorising training records |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions welcome!

## 📄 License

MIT — see [LICENSE](LICENSE).
