"""Unit tests for ModelInversionAuditor module."""

from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from privacylens.attacks.inversion import ModelInversionAuditor


class TestModelInversionAuditor:
    def test_returns_tuple_score_details(self):
        X, y = make_classification(n_samples=200, n_features=5, random_state=42)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X[:150], y[:150])

        auditor = ModelInversionAuditor()
        score, details = auditor.run(model, X[150:])
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        assert "inversion_risk_score" in details
        assert "avg_reconstruction_error" in details

    def test_empty_samples_returns_zero(self):
        X = np.array([])
        auditor = ModelInversionAuditor()
        score, details = auditor.run(None, X)
        assert score == 0.0
        assert "error" in details

    def test_custom_target_features(self):
        X, y = make_classification(n_samples=200, n_features=5, random_state=99)
        model = RandomForestClassifier(n_estimators=10, random_state=99)
        model.fit(X[:150], y[:150])

        auditor = ModelInversionAuditor(target_feature_indices=[0, 1])
        score, details = auditor.run(model, X[150:])
        assert details["target_feature_indices"] == [0, 1]
        assert 0.0 <= score <= 1.0
