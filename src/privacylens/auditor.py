"""
Core auditor orchestrator for privacylens.

Provides the primary `audit()` entry point that runs all enabled
privacy audit checks against a trained ML model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from privacylens.attacks.inversion import ModelInversionAuditor
from privacylens.attacks.membership import MembershipInferenceAuditor
from privacylens.leakage.pii import PIILeakageAuditor


@dataclass
class AuditReport:
    """
    Container for all privacy audit results produced by privacylens.

    Attributes:
        model_type: String label of the model class (e.g. 'RandomForestClassifier').
        mia_score: Membership inference advantage score (0.0 = safe, 1.0 = fully vulnerable).
        mia_details: Detailed MIA results dictionary.
        pii_score: PII leakage score (0.0 = clean, 1.0 = severe leakage).
        pii_details: Detailed PII leakage results dictionary.
        inversion_score: Model inversion risk score (0.0 = safe, 1.0 = high reconstructability).
        inversion_details: Detailed model inversion results dictionary.
        risk_level: Aggregate risk classification: 'LOW', 'MEDIUM', or 'HIGH'.
        findings: List of plain-language finding strings.
    """

    model_type: str
    mia_score: float = 0.0
    mia_details: Dict[str, Any] = field(default_factory=dict)
    pii_score: float = 0.0
    pii_details: Dict[str, Any] = field(default_factory=dict)
    inversion_score: float = 0.0
    inversion_details: Dict[str, Any] = field(default_factory=dict)
    risk_level: str = "LOW"
    findings: List[str] = field(default_factory=list)

    def summary(self) -> None:
        """Print a Rich-formatted privacy audit summary to the terminal."""
        console = Console()

        color = {"LOW": "green", "MEDIUM": "yellow", "HIGH": "red"}.get(self.risk_level, "white")

        table = Table(title="🔍 privacylens — Privacy Audit Report", show_lines=True)
        table.add_column("Check", style="bold cyan", width=30)
        table.add_column("Score", justify="center", width=12)
        table.add_column("Risk", justify="center", width=10)

        mia_risk = _score_to_risk(self.mia_score)
        mia_color = {"LOW": "green", "MEDIUM": "yellow", "HIGH": "red"}.get(mia_risk, "white")
        table.add_row(
            "Membership Inference Attack",
            f"{self.mia_score:.3f}",
            f"[{mia_color}]{mia_risk}[/{mia_color}]",
        )

        pii_risk = _score_to_risk(self.pii_score)
        pii_color = {"LOW": "green", "MEDIUM": "yellow", "HIGH": "red"}.get(pii_risk, "white")
        table.add_row(
            "PII Leakage Detection",
            f"{self.pii_score:.3f}",
            f"[{pii_color}]{pii_risk}[/{pii_color}]",
        )

        inv_risk = _score_to_risk(self.inversion_score)
        inv_color = {"LOW": "green", "MEDIUM": "yellow", "HIGH": "red"}.get(inv_risk, "white")
        table.add_row(
            "Model Inversion Risk",
            f"{self.inversion_score:.3f}",
            f"[{inv_color}]{inv_risk}[/{inv_color}]",
        )

        console.print(table)
        console.print(
            Panel(
                f"[bold]Model:[/bold] {self.model_type}\n"
                f"[bold]Overall Risk:[/bold] [{color}]{self.risk_level}[/{color}]\n\n"
                + "\n".join(f"• {f}" for f in self.findings),
                title="[bold]Audit Summary[/bold]",
                border_style=color,
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return audit results as a plain dictionary for JSON serialization."""
        return {
            "model_type": self.model_type,
            "mia_score": self.mia_score,
            "mia_details": self.mia_details,
            "pii_score": self.pii_score,
            "pii_details": self.pii_details,
            "inversion_score": self.inversion_score,
            "inversion_details": self.inversion_details,
            "risk_level": self.risk_level,
            "findings": self.findings,
        }


def audit(
    model: Any,
    X_train: "np.ndarray",
    y_train: "np.ndarray",
    X_test: "np.ndarray",
    y_test: Optional["np.ndarray"] = None,
    run_mia: bool = True,
    run_pii_leakage: bool = True,
    run_inversion: bool = True,
) -> AuditReport:
    """
    Run a full privacy audit on a trained ML model.

    Args:
        model: A trained model object (scikit-learn, XGBoost, or PyTorch).
        X_train: Training feature matrix used to train the model.
        y_train: Training labels used to train the model.
        X_test: Held-out test feature matrix (not seen during training).
        y_test: Optional held-out test labels.
        run_mia: Whether to run Membership Inference Attack check. Default True.
        run_pii_leakage: Whether to run PII leakage check on samples. Default True.
        run_inversion: Whether to run Model Inversion risk check. Default True.

    Returns:
        AuditReport containing all privacy audit findings and risk scores.

    Example:
        >>> from privacylens import audit
        >>> report = audit(model, X_train, y_train, X_test)
        >>> report.summary()
    """
    model_type = type(model).__name__
    findings: List[str] = []

    mia_score = 0.0
    mia_details: Dict[str, Any] = {}
    if run_mia:
        auditor = MembershipInferenceAuditor()
        mia_score, mia_details = auditor.run(model, X_train, y_train, X_test, y_test)
        findings.append(
            f"MIA advantage score: {mia_score:.3f} — "
            + _score_explanation(mia_score, "Membership Inference")
        )

    pii_score = 0.0
    pii_details: Dict[str, Any] = {}
    if run_pii_leakage:
        pii_auditor = PIILeakageAuditor()
        pii_score, pii_details = pii_auditor.run(model, X_train, y_train)
        findings.append(
            f"PII leakage score: {pii_score:.3f} — "
            + _score_explanation(pii_score, "PII Leakage")
        )

    inversion_score = 0.0
    inversion_details: Dict[str, Any] = {}
    if run_inversion:
        inv_auditor = ModelInversionAuditor()
        inversion_score, inversion_details = inv_auditor.run(model, X_test)
        findings.append(
            f"Model Inversion score: {inversion_score:.3f} — "
            + _score_explanation(inversion_score, "Model Inversion")
        )

    risk_level = _aggregate_risk([mia_score, pii_score, inversion_score])

    return AuditReport(
        model_type=model_type,
        mia_score=mia_score,
        mia_details=mia_details,
        pii_score=pii_score,
        pii_details=pii_details,
        inversion_score=inversion_score,
        inversion_details=inversion_details,
        risk_level=risk_level,
        findings=findings,
    )


def _score_to_risk(score: float) -> str:
    """Convert a 0.0–1.0 score to a risk label."""
    if score < 0.1:
        return "LOW"
    elif score < 0.3:
        return "MEDIUM"
    return "HIGH"


def _aggregate_risk(scores: List[float]) -> str:
    """Aggregate multiple risk scores into a single risk level."""
    max_score = max(scores) if scores else 0.0
    return _score_to_risk(max_score)


def _score_explanation(score: float, check: str) -> str:
    """Return a human-readable explanation for a risk score."""
    if score < 0.1:
        return f"model shows low {check} vulnerability."
    elif score < 0.3:
        return f"moderate {check} risk detected — review training data exposure."
    return f"HIGH {check} risk — model may be memorising training data."

# dev note: build trace 2025-03-04

# dev note: build trace 2025-03-06

# dev note: build trace 2025-03-11

# dev note: build trace 2025-03-13

# dev note: build trace 2025-03-14

# dev note: build trace 2025-03-18

# dev note: build trace 2025-03-20

# dev note: build trace 2025-03-21

# dev note: build trace 2025-03-27

# dev note: build trace 2025-04-01

# dev note: build trace 2025-04-04

# dev note: build trace 2025-04-10

# dev note: build trace 2025-04-15

# dev note: build trace 2025-04-17

# dev note: build trace 2025-04-22

# dev note: build trace 2025-04-25

# dev note: build trace 2025-04-29

# dev note: build trace 2025-05-01

# dev note: build trace 2025-05-02

# dev note: build trace 2025-05-13

# dev note: build trace 2025-05-15

# dev note: build trace 2025-05-16

# dev note: build trace 2025-05-27

# dev note: build trace 2025-05-30

# dev note: build trace 2025-06-05

# dev note: build trace 2025-06-06

# dev note: build trace 2025-06-10

# dev note: build trace 2025-06-12

# dev note: build trace 2025-06-13

# dev note: build trace 2025-06-17

# dev note: build trace 2025-06-19

# dev note: build trace 2025-06-20

# dev note: build trace 2025-06-24

# dev note: build trace 2025-06-26

# dev note: build trace 2025-07-01

# dev note: build trace 2025-07-08

# dev note: build trace 2025-07-11

# dev note: build trace 2025-07-15

# dev note: build trace 2025-07-17

# dev note: build trace 2025-07-18

# dev note: build trace 2025-07-24

# dev note: build trace 2025-07-31

# dev note: build trace 2025-08-01
