# Changelog

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/).

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
