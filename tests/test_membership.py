"""Unit tests for MembershipInferenceAuditor."""

from __future__ import annotations

import pytest
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from privacylens.attacks.membership import MembershipInferenceAuditor


@pytest.fixture
def rf_data():
    X, y = make_classification(n_samples=400, n_features=10, random_state=42)
    model = RandomForestClassifier(n_estimators=20, random_state=42)
    model.fit(X[:200], y[:200])
    return model, X[:200], y[:200], X[200:], y[200:]


class TestMembershipInferenceAuditor:
    def test_returns_tuple(self, rf_data):
        model, X_train, y_train, X_test, y_test = rf_data
        auditor = MembershipInferenceAuditor()
        score, details = auditor.run(model, X_train, y_train, X_test, y_test)
        assert isinstance(score, float)
        assert isinstance(details, dict)

    def test_score_in_range(self, rf_data):
        model, X_train, y_train, X_test, y_test = rf_data
        auditor = MembershipInferenceAuditor()
        score, _ = auditor.run(model, X_train, y_train, X_test, y_test)
        assert 0.0 <= score <= 1.0

    def test_details_contain_keys(self, rf_data):
        model, X_train, y_train, X_test, y_test = rf_data
        auditor = MembershipInferenceAuditor()
        _, details = auditor.run(model, X_train, y_train, X_test, y_test)
        assert "attack_accuracy" in details
        assert "mia_advantage" in details
        assert "n_members_evaluated" in details
        assert "n_nonmembers_evaluated" in details

    def test_no_predict_proba_model(self, rf_data):
        """SVC without probability=True has no predict_proba but has decision_function.
        The auditor should still run via decision_function and return a valid score."""
        _, X_train, y_train, X_test, y_test = rf_data
        svc = SVC(probability=False)
        svc.fit(X_train, y_train)
        auditor = MembershipInferenceAuditor()
        score, details = auditor.run(svc, X_train, y_train, X_test, y_test)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        assert "attack_accuracy" in details

    def test_rf_attack_model(self, rf_data):
        model, X_train, y_train, X_test, y_test = rf_data
        auditor = MembershipInferenceAuditor(attack_model="rf")
        score, details = auditor.run(model, X_train, y_train, X_test, y_test)
        assert details["attack_model"] == "rf"
        assert 0.0 <= score <= 1.0
