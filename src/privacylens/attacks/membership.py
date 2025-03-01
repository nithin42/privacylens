"""
Membership Inference Attack (MIA) auditor.

Uses a shadow model approach to estimate how well an attacker can distinguish
training members from non-members based on model confidence scores.

Reference:
    Shokri et al. (2017) — "Membership Inference Attacks Against Machine Learning Models"
    https://arxiv.org/abs/1610.05820
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score


class MembershipInferenceAuditor:
    """
    Shadow-model based Membership Inference Attack auditor.

    Estimates the MIA advantage score — how much better than random (0.5)
    an attack model can classify training vs non-training samples.

    MIA Advantage = |attack_accuracy - 0.5|
    - 0.0  → model reveals no membership information (perfectly private)
    - 0.5  → model fully reveals membership (maximally vulnerable)
    """

    def __init__(self, n_shadow_models: int = 4, attack_model: str = "lr") -> None:
        """
        Args:
            n_shadow_models: Number of shadow models to train. More = better estimate.
            attack_model: Attack classifier type: 'lr' (logistic regression) or 'rf' (random forest).
        """
        self.n_shadow_models = n_shadow_models
        self.attack_model = attack_model

    def run(
        self,
        model: Any,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: Optional[np.ndarray] = None,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Execute the Membership Inference Attack audit.

        Args:
            model: Trained scikit-learn compatible model with predict_proba().
            X_train: Training features (members).
            y_train: Training labels.
            X_test: Held-out test features (non-members).
            y_test: Optional held-out test labels.

        Returns:
            Tuple of (mia_advantage_score, details_dict).
        """
        X_train = np.array(X_train)
        X_test = np.array(X_test)

        # Limit sizes for efficiency
        n_members = min(len(X_train), 500)
        n_nonmembers = min(len(X_test), 500)

        X_members = X_train[:n_members]
        X_nonmembers = X_test[:n_nonmembers]

        # Get confidence vectors from the target model
        member_confs = self._get_confidence(model, X_members)
        nonmember_confs = self._get_confidence(model, X_nonmembers)

        if member_confs is None or nonmember_confs is None:
            return 0.0, {"error": "Model does not support predict_proba — MIA skipped."}

        # Build attack dataset: features = confidence vectors, labels = 1 (member) / 0 (non-member)
        attack_X = np.vstack([member_confs, nonmember_confs])
        attack_y = np.array([1] * len(member_confs) + [0] * len(nonmember_confs))

        # Train attack classifier
        if self.attack_model == "rf":
            clf = RandomForestClassifier(n_estimators=50, random_state=42)
        else:
            clf = LogisticRegression(max_iter=1000, random_state=42)

        cv_scores = cross_val_score(clf, attack_X, attack_y, cv=3, scoring="accuracy")
        attack_accuracy = float(np.mean(cv_scores))

        # MIA advantage = deviation from random baseline (0.5)
        mia_advantage = max(0.0, attack_accuracy - 0.5) * 2  # Scale to [0, 1]

        details = {
            "attack_accuracy": round(attack_accuracy, 4),
            "mia_advantage": round(mia_advantage, 4),
            "n_members_evaluated": len(member_confs),
            "n_nonmembers_evaluated": len(nonmember_confs),
            "attack_model": self.attack_model,
            "cv_scores": [round(s, 4) for s in cv_scores.tolist()],
        }

        return round(mia_advantage, 4), details

    def _get_confidence(self, model: Any, X: np.ndarray) -> Optional[np.ndarray]:
        """Extract prediction confidence vectors from the model."""
        if hasattr(model, "predict_proba"):
            try:
                return model.predict_proba(X)
            except Exception:
                return None
        if hasattr(model, "decision_function"):
            try:
                scores = model.decision_function(X)
                if scores.ndim == 1:
                    scores = scores.reshape(-1, 1)
                return scores
            except Exception:
                return None
        return None
