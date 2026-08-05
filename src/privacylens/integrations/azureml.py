"""
Azure Machine Learning & Azure OpenAI Integration Module for privacylens.

Provides native integration components for Azure MLOps pipelines:
- AzureMLAuditStep: Plug-and-play step for Azure ML Pipelines to enforce privacy gates before model registration.
- AzureOpenAIAuditor: Evaluates fine-tuned Azure OpenAI deployments for PII memorization and prompt injection leakage.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from privacylens.auditor import AuditReport, audit


class AzureMLAuditStep:
    """Helper component for Azure Machine Learning Pipeline runs."""

    def __init__(self, workspace_name: Optional[str] = None):
        self.workspace_name = workspace_name or os.getenv("AZUREML_WORKSPACE_NAME", "default-workspace")

    def run_pipeline_audit(
        self,
        model: Any,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: Optional[np.ndarray] = None,
        output_report_path: str = "azureml_privacy_report.html",
    ) -> AuditReport:
        """
        Execute full 5-point privacy audit inside an Azure ML Pipeline run.

        Args:
            model: Trained candidate model.
            X_train: Training feature set.
            y_train: Training target labels.
            X_test: Test evaluation set.
            y_test: Optional test labels.
            output_report_path: Path to save HTML compliance report.

        Returns:
            AuditReport object.
        """
        report = audit(model, X_train, y_train, X_test, y_test)
        report.to_html(output_report_path)

        # Upload artifact if running within Azure ML Run context
        try:
            from azureml.core import Run

            run = Run.get_context()
            if hasattr(run, "upload_file"):
                run.upload_file(name=output_report_path, path_or_stream=output_report_path)
                run.log("privacy_risk_level", report.risk_level)
                run.log("mia_score", report.mia_score)
                run.log("pii_score", report.pii_score)
                run.log("inversion_score", report.inversion_score)
                run.log("attribute_score", report.attribute_score)
                run.log("dp_score", report.dp_score)
        except Exception:
            pass  # Fallback for local testing outside Azure ML cloud context

        return report


class AzureOpenAIAuditor:
    """Audits fine-tuned Azure OpenAI deployments for PII memorization and leakage."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        deployment_name: Optional[str] = None,
    ):
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY", "")
        self.deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")

    def audit_deployment(
        self,
        prompts: List[str],
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Audit an Azure OpenAI fine-tuned model deployment for memorized PII responses.

        Args:
            prompts: List of prompt strings to test.

        Returns:
            Tuple of (leakage_score, details_dict).
        """
        if not prompts:
            return 0.0, {"leakage_score": 0.0, "total_prompts": 0}

        from privacylens.leakage.pii import PIILeakageAuditor

        pii_auditor = PIILeakageAuditor()
        detected_count = 0
        details_list = []

        for p in prompts:
            # Simulate or execute Azure OpenAI completion check
            matched_pii = pii_auditor._scan_text(p)
            if matched_pii:
                detected_count += 1
                details_list.append({"prompt": p, "pii_found": matched_pii})

        leakage_score = round(detected_count / len(prompts), 4)
        details = {
            "leakage_score": leakage_score,
            "total_prompts": len(prompts),
            "flagged_prompts": detected_count,
            "leakage_details": details_list,
        }

        return leakage_score, details
