"""Unit tests for AttributeInferenceAuditor and DPEpsilonAuditor modules."""

from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from privacylens import audit
from privacylens.attacks.attribute import AttributeInferenceAuditor
from privacylens.leakage.dp import DPEpsilonAuditor


class Test5PointAudits:
    def test_attribute_inference_auditor(self):
        X, y = make_classification(n_samples=100, n_features=5, random_state=42)
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X[:80], y[:80])

        auditor = AttributeInferenceAuditor()
        score, details = auditor.run(model, X[80:])
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        assert "attribute_inference_score" in details

    def test_dp_epsilon_auditor(self):
        X, y = make_classification(n_samples=100, n_features=5, random_state=42)
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X[:80], y[:80])

        auditor = DPEpsilonAuditor()
        score, details = auditor.run(model, X[80:])
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        assert "dp_score" in details
        assert "estimated_epsilon" in details

    def test_audit_report_contains_all_5_checks(self):
        X, y = make_classification(n_samples=100, n_features=5, random_state=42)
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X[:80], y[:80])

        report = audit(model, X[:80], y[:80], X[80:], y[80:])
        assert 0.0 <= report.mia_score <= 1.0
        assert 0.0 <= report.pii_score <= 1.0
        assert 0.0 <= report.inversion_score <= 1.0
        assert 0.0 <= report.attribute_score <= 1.0
        assert 0.0 <= report.dp_score <= 1.0
        assert len(report.findings) == 5
