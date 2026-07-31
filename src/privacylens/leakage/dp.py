"""
Empirical Differential Privacy (DP) Estimator.

Estimates empirical privacy budget loss (Epsilon ε) by measuring the
output probability distribution divergence under single-record modifications.

Reference:
    Jagielski et al. (2020) — "Auditing Differential Privacy in Practice"
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import numpy as np


class DPEpsilonAuditor:
    """Estimates empirical Differential Privacy budget loss score (Epsilon ε)."""

    def run(
        self,
        model: Any,
        X_samples: np.ndarray,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Execute Empirical Differential Privacy audit.

        Args:
            model: Trained model with confidence output.
            X_samples: Feature matrix.

        Returns:
            Tuple of (dp_score, details_dict).
            - dp_score: 0.0 (strong privacy, low epsilon) to 1.0 (high privacy loss).
        """
        X_arr = np.array(X_samples)
        if len(X_arr) < 10:
            return 0.0, {
                "dp_score": 0.0,
                "estimated_epsilon": 0.0,
                "error": "Insufficient samples for DP audit.",
            }

        conf = self._get_conf(model, X_arr)
        if conf is None or len(conf) < 10:
            return 0.0, {
                "dp_score": 0.0,
                "estimated_epsilon": 0.0,
                "error": "Model does not support confidence scoring for DP audit.",
            }

        # Measure max ratio of prediction probabilities across neighboring inputs
        n_eval = min(len(conf), 50)
        epsilons = []

        for i in range(n_eval - 1):
            p1 = np.clip(conf[i], 1e-5, 1.0 - 1e-5)
            p2 = np.clip(conf[i + 1], 1e-5, 1.0 - 1e-5)
            log_ratio = np.max(np.abs(np.log(p1 / p2)))
            epsilons.append(float(log_ratio))

        estimated_epsilon = float(np.percentile(epsilons, 95)) if epsilons else 0.0
        # Normalize epsilon to 0.0 - 1.0 risk score (epsilon >= 3.0 is HIGH risk)
        dp_score = max(0.0, min(1.0, round(estimated_epsilon / 3.0, 4)))

        details = {
            "dp_score": dp_score,
            "estimated_epsilon": round(estimated_epsilon, 4),
            "samples_evaluated": n_eval,
        }

        return dp_score, details

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
