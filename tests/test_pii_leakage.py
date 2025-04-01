"""Unit tests for PIILeakageAuditor module."""

from __future__ import annotations

import numpy as np

from privacylens.leakage.pii import PIILeakageAuditor


class TestPIILeakageAuditor:
    def test_clean_samples_returns_zero_score(self):
        X = np.array([["safe_value_1", "safe_value_2"], ["12345", "67890"]])
        auditor = PIILeakageAuditor()
        score, details = auditor.run(None, X)
        assert score == 0.0
        assert details["matches_found"] == 0

    def test_email_leakage_detected(self):
        X = np.array([["alice@example.com", "safe_col"], ["bob@company.org", "other_col"]])
        auditor = PIILeakageAuditor()
        score, details = auditor.run(None, X)
        assert score > 0.0
        assert details["by_type"]["EMAIL"] == 2

    def test_ssn_leakage_detected(self):
        X = np.array([["123-45-6789", "clean_col"], ["234-56-7890", "clean_col"]])
        auditor = PIILeakageAuditor()
        score, details = auditor.run(None, X)
        assert score > 0.0
        assert details["by_type"]["SSN"] == 2

    def test_custom_target_patterns(self):
        X = np.array([["alice@example.com", "123-45-6789"]])
        auditor = PIILeakageAuditor(target_patterns=["EMAIL"])
        score, details = auditor.run(None, X)
        assert "EMAIL" in details["by_type"]
        assert "SSN" not in details["by_type"]

    def test_empty_samples_returns_zero(self):
        X = np.array([])
        auditor = PIILeakageAuditor()
        score, details = auditor.run(None, X)
        assert score == 0.0
        assert details["total_samples_scanned"] == 0

    def test_list_samples_extraction(self):
        samples = ["Contact us at user@domain.com", "No PII here"]
        auditor = PIILeakageAuditor()
        score, details = auditor.run(None, samples)
        assert score > 0.0
        assert details["matches_found"] == 1
