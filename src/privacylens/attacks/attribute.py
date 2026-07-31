"""
Attribute Inference Attack Auditor.

Evaluates if an attacker can infer sensitive secondary attributes
(e.g., demographic group, sensitive labels) from model output confidence vectors.

Reference:
    Yeom et al. (2018) — "Privacy Risk in Machine Learning:
    Analyzing the Connection to Overfitting"
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import numpy as np
from sklearn.linear_model import LogisticRegression


class AttributeInferenceAuditor:
    """Evaluates Attribute Inference Risk score (0.0 to 1.0)."""

    def run(
        self,
        model: Any,
        X_samples: np.ndarray,
        sensitive_attribute: Optional[np.ndarray] = None,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Execute Attribute Inference Attack audit.

        Args:
            model: Trained model with predict_proba() or decision_function().
            X_samples: Feature matrix.
            sensitive_attribute: Optional binary/categorical array representing sensitive attribute.

        Returns:
            Tuple of (attribute_inference_score, details_dict).
        """
        X_arr = np.array(X_samples)
        if len(X_arr) < 20:
            return 0.0, {
                "attribute_inference_score": 0.0,
                "error": "Insufficient samples for attribute inference audit.",
            }

        # Extract confidence scores
        conf = self._get_conf(model, X_arr)
        if conf is None or len(conf) < 20:
            return 0.0, {
                "attribute_inference_score": 0.0,
                "error": "Model does not support confidence scoring for attribute inference.",
            }

        # Synthesize or evaluate sensitive attribute correlation
        if sensitive_attribute is None:
            # Evaluate internal target feature predictability from confidence
            sensitive_attribute = (X_arr[:, 0] > np.median(X_arr[:, 0])).astype(int)
        else:
            sensitive_attribute = np.array(sensitive_attribute).astype(int)

        n_samples = len(conf)
        split = n_samples // 2
        conf_train, conf_test = conf[:split], conf[split:]
        attr_train, attr_test = sensitive_attribute[:split], sensitive_attribute[split:]

        try:
            attacker = LogisticRegression(random_state=42)
            attacker.fit(conf_train, attr_train)
            acc = float(attacker.score(conf_test, attr_test))
            baseline_acc = float(max(np.mean(attr_test), 1.0 - np.mean(attr_test)))
            advantage = max(0.0, (acc - baseline_acc) / (1.0 - baseline_acc + 1e-6))
            score = max(0.0, min(1.0, round(advantage, 4)))
        except Exception:
            score = 0.0
            acc = 0.5
            baseline_acc = 0.5

        details = {
            "attribute_inference_score": score,
            "attack_accuracy": round(acc, 4),
            "baseline_accuracy": round(baseline_acc, 4),
            "samples_evaluated": n_samples,
        }

        return score, details

    def _get_conf(self, model: Any, X: np.ndarray) -> Optional[np.ndarray]:
        if hasattr(model, "predict_proba"):
            try:
                return model.predict_proba(X)
            except Exception:
                pass
        if hasattr(model, "decision_function"):
            try:
                scores = model.decision_function(X)
                return scores.reshape(-1, 1) if scores.ndim == 1 else scores
            except Exception:
                pass
        return None
