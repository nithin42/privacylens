"""Unit tests for HTML report generator module."""

from __future__ import annotations

import os
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from privacylens import audit
from privacylens.report.html import generate_html_report


class TestHTMLReport:
    def test_generate_html_report(self, tmp_path):
        X, y = make_classification(n_samples=100, n_features=5, random_state=42)
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X[:80], y[:80])

        report = audit(model, X[:80], y[:80], X[80:], y[80:])
        out_file = os.path.join(tmp_path, "report.html")

        res_path = generate_html_report(report, out_file)
        assert os.path.exists(res_path)

        with open(res_path, "r", encoding="utf-8") as f:
            html = f.read()

        assert "privacylens — Privacy Audit Report" in html
        assert "RandomForestClassifier" in html
        assert "Membership Inference" in html

    def test_to_html_method_on_audit_report(self, tmp_path):
        X, y = make_classification(n_samples=100, n_features=5, random_state=42)
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X[:80], y[:80])

        report = audit(model, X[:80], y[:80], X[80:], y[80:])
        out_file = os.path.join(tmp_path, "compliance.html")

        res_path = report.to_html(out_file)
        assert os.path.exists(res_path)
