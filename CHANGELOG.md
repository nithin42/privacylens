# Changelog

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.1] — 2026-07-31

### Added
- **Attribute Inference Attack Auditor**: Added `AttributeInferenceAuditor` (`src/privacylens/attacks/attribute.py`) implementing Yeom et al. (2018) sensitive attribute prediction risk scoring
- **Empirical Differential Privacy Epsilon Estimator**: Added `DPEpsilonAuditor` (`src/privacylens/leakage/dp.py`) implementing Jagielski et al. (2020) empirical privacy loss ($\epsilon$) estimation
- **5-Point Privacy Audit Suite**: Updated `AuditReport`, terminal table, and HTML compliance reports to display all 5 privacy vulnerability checks
- **Test Suite**: Added unit tests for attribute inference and differential privacy auditors

## [1.0.0] — 2026-07-31

### Added
- **HuggingFace Transformers Adapter**: Added `HuggingFaceAdapter` (`src/privacylens/adapters/hf_adapter.py`) to audit LLM embeddings and classification pipelines for privacy leakage
- **Benchmark Suite**: Added `examples/benchmark_demo.py` showcasing full end-to-end privacy auditing across scikit-learn, XGBoost, PyTorch, and HuggingFace models
- **Test Suite**: Added `test_hf_adapter.py` unit test suite
- **Production Flagship Release**: General Availability (GA) v1.0.0

## [0.5.0] — 2026-01-15

### Added
- **HTML Compliance Report Generator**: Added `src/privacylens/report/html.py` implementing `generate_html_report()` Jinja2 standalone HTML report exporter
- **`to_html()` Method**: Added `to_html(output_path)` export method to `AuditReport` dataclass
- **CLI `--report` Flag**: Added `--report audit.html` flag to `privacylens audit` command
- **Test Suite**: Added `test_html_report.py` unit test suite

## [0.4.0] — 2025-10-01

### Added
- **Native Framework Adapters**: Added `src/privacylens/adapters/` containing `BaseModelAdapter`, `SklearnAdapter`, `PyTorchAdapter`, and `XGBoostAdapter`
- **Automatic Model Factory**: Added `get_adapter(model)` factory function for seamless model wrapper instantiation
- **PyTorch Softmax Logit Normalization**: Automatically converts raw neural network output logits into probabilities
- **Test Suite**: Added `test_adapters.py` unit test suite

## [0.3.0] — 2025-07-01

### Added
- **Model Inversion Risk Scorer**: Added `ModelInversionAuditor` (`src/privacylens/attacks/inversion.py`) implementing Fredrikson et al. (2015) feature reconstruction risk scoring
- **Inversion Score in AuditReport**: Added `inversion_score` and `inversion_details` to `AuditReport` and Rich summary table
- **`run_inversion` Flag**: Integrated `run_inversion=True` flag in `audit()` function
- **Test Suite**: Added `test_inversion.py` unit test suite

## [0.2.0] — 2025-04-01

### Added
- **PII Leakage Detection Engine**: Added `PIILeakageAuditor` (`src/privacylens/leakage/pii.py`) to scan model predictions and samples for memorized sensitive PII (Emails, SSNs, Credit Cards, Phones, IPs)
- **PII Score in AuditReport**: Added `pii_score` and `pii_details` to `AuditReport` and Rich summary table
- **`run_pii_leakage` Flag**: Integrated `run_pii_leakage=True` flag in `audit()` function
- **Test Suite**: Added `test_pii_leakage.py` with 100% test coverage

## [0.1.1] — 2025-03-02

### Fixed
- **SVC Decision Function Auditing**: Fixed assertion in `test_no_predict_proba_model` to validate scikit-learn `SVC` models that utilize `decision_function()` for MIA confidence scores.

## [0.1.0] — 2025-03-01

### Added
- Core `audit()` entry point with `AuditReport` dataclass
- Membership Inference Attack (MIA) engine using shadow model approach (Shokri et al., 2017)
- Support for scikit-learn models with `predict_proba()` and `decision_function()`
- Rich terminal audit report with colour-coded risk levels (LOW / MEDIUM / HIGH)
- `to_dict()` serialization for JSON output
- Click CLI with `privacylens audit` command
- `--output json` flag for machine-readable results
- `--no-mia` flag to skip MIA check in pipelines
- Full test suite: `test_auditor.py`, `test_membership.py`
- `src/` layout with `pythonpath = ["src"]` pytest configuration
