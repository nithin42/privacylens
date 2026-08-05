"""Unit tests for Azure ML & Azure OpenAI integration module."""

from __future__ import annotations

import os
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from privacylens.integrations.azureml import AzureMLAuditStep, AzureOpenAIAuditor


class TestAzureMLIntegration:
    def test_azureml_audit_step_local(self, tmp_path):
        X, y = make_classification(n_samples=100, n_features=5, random_state=42)
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X[:80], y[:80])

        step = AzureMLAuditStep(workspace_name="test-workspace")
        report_path = os.path.join(tmp_path, "azure_report.html")

        report = step.run_pipeline_audit(model, X[:80], y[:80], X[80:], y[80:], output_report_path=report_path)

        assert os.path.exists(report_path)
        assert report.model_type == "RandomForestClassifier"
        assert 0.0 <= report.mia_score <= 1.0

    def test_azure_openai_auditor(self):
        auditor = AzureOpenAIAuditor(
            endpoint="https://test.openai.azure.com/",
            api_key="test-key",
            deployment_name="gpt-4",
        )

        test_prompts = [
            "John Doe's SSN is 000-12-3456",
            "Contact user at user@example.com",
            "What is the weather today in Seattle?",
        ]

        score, details = auditor.audit_deployment(test_prompts)
        assert isinstance(score, float)
        assert score > 0.0  # Should detect SSN and email
        assert details["total_prompts"] == 3
        assert details["flagged_prompts"] == 2
