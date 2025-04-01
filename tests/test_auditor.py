"""Unit tests for privacylens.auditor module."""

from __future__ import annotations

import pytest
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from privacylens import audit, AuditReport
from privacylens.auditor import _score_to_risk, _aggregate_risk


@pytest.fixture
def simple_model():
    """Return a trained RandomForest classifier on synthetic data."""
    X, y = make_classification(n_samples=300, n_features=10, random_state=42)
    model = RandomForestClassifier(n_estimators=20, random_state=42)
    model.fit(X[:200], y[:200])
    return model, X[:200], y[:200], X[200:], y[200:]


@pytest.fixture
def lr_model():
    """Return a trained LogisticRegression on synthetic data."""
    X, y = make_classification(n_samples=300, n_features=10, random_state=99)
    model = LogisticRegression(max_iter=1000, random_state=99)
    model.fit(X[:200], y[:200])
    return model, X[:200], y[:200], X[200:], y[200:]


class TestAuditFunction:
    def test_returns_audit_report(self, simple_model):
        model, X_train, y_train, X_test, y_test = simple_model
        report = audit(model, X_train, y_train, X_test, y_test)
        assert isinstance(report, AuditReport)

    def test_mia_score_in_range(self, simple_model):
        model, X_train, y_train, X_test, y_test = simple_model
        report = audit(model, X_train, y_train, X_test, y_test)
        assert 0.0 <= report.mia_score <= 1.0

    def test_risk_level_valid(self, simple_model):
        model, X_train, y_train, X_test, y_test = simple_model
        report = audit(model, X_train, y_train, X_test, y_test)
        assert report.risk_level in ("LOW", "MEDIUM", "HIGH")

    def test_findings_populated(self, simple_model):
        model, X_train, y_train, X_test, y_test = simple_model
        report = audit(model, X_train, y_train, X_test, y_test)
        assert len(report.findings) >= 1

    def test_no_mia_skipped(self, simple_model):
        model, X_train, y_train, X_test, y_test = simple_model
        report = audit(model, X_train, y_train, X_test, run_mia=False)
        assert report.mia_score == 0.0

    def test_pii_score_in_range(self, simple_model):
        model, X_train, y_train, X_test, y_test = simple_model
        report = audit(model, X_train, y_train, X_test)
        assert 0.0 <= report.pii_score <= 1.0

    def test_no_pii_leakage_skipped(self, simple_model):
        model, X_train, y_train, X_test, y_test = simple_model
        report = audit(model, X_train, y_train, X_test, run_pii_leakage=False)
        assert report.pii_score == 0.0

    def test_model_type_recorded(self, simple_model):
        model, X_train, y_train, X_test, y_test = simple_model
        report = audit(model, X_train, y_train, X_test)
        assert report.model_type == "RandomForestClassifier"

    def test_logistic_regression_model(self, lr_model):
        model, X_train, y_train, X_test, y_test = lr_model
        report = audit(model, X_train, y_train, X_test, y_test)
        assert isinstance(report, AuditReport)
        assert 0.0 <= report.mia_score <= 1.0

    def test_to_dict_returns_dict(self, simple_model):
        model, X_train, y_train, X_test, y_test = simple_model
        report = audit(model, X_train, y_train, X_test, y_test)
        d = report.to_dict()
        assert isinstance(d, dict)
        assert "mia_score" in d
        assert "risk_level" in d
        assert "model_type" in d


class TestRiskHelpers:
    def test_score_low(self):
        assert _score_to_risk(0.05) == "LOW"

    def test_score_medium(self):
        assert _score_to_risk(0.20) == "MEDIUM"

    def test_score_high(self):
        assert _score_to_risk(0.50) == "HIGH"

    def test_aggregate_risk_empty(self):
        assert _aggregate_risk([]) == "LOW"

    def test_aggregate_risk_max(self):
        assert _aggregate_risk([0.05, 0.40]) == "HIGH"
