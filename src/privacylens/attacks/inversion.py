"""
Model Inversion Risk Auditor.

Evaluates how easily an attacker can reconstruct sensitive input feature values
given only access to the model output confidence probabilities.

Reference:
    Fredrikson et al. (2015) — "Model Inversion Attacks that Exploit Confidence
    Information and Basic Mathematical Techniques"
    https://dl.acm.org/doi/10.1145/2810103.2813677
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import numpy as np


class ModelInversionAuditor:
    """
    Evaluates feature reconstructability risk via Model Inversion.

    Estimates Model Inversion Risk score (0.0 to 1.0) by measuring how closely
    an optimization-based search over feature space can reconstruct target input features
    matching model output confidence vectors.
    """

    def __init__(self, target_feature_indices: Optional[List[int]] = None) -> None:
        """
        Args:
            target_feature_indices: Feature column indices to test for reconstruction.
                                   If None, tests the first 3 continuous features.
        """
        self.target_feature_indices = target_feature_indices

    def run(
        self,
        model: Any,
        X_samples: np.ndarray,
        y_samples: Optional[np.ndarray] = None,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Execute Model Inversion Risk audit.

        Args:
            model: Trained model with predict_proba() or decision_function().
            X_samples: Sample feature matrix (e.g. test set).
            y_samples: Optional label array.

        Returns:
            Tuple of (inversion_risk_score, details_dict).
        """
        X_arr = np.array(X_samples)
        if X_arr.ndim != 2 or len(X_arr) == 0:
            return 0.0, {
                "inversion_risk_score": 0.0,
                "error": "Empty or invalid feature matrix.",
            }

        if not hasattr(model, "predict_proba") and not hasattr(model, "decision_function"):
            return 0.0, {
                "inversion_risk_score": 0.0,
                "error": "Model does not support confidence scoring for inversion.",
            }

        n_features = X_arr.shape[1]
        target_indices = (
            self.target_feature_indices
            if self.target_feature_indices is not None
            else list(range(min(3, n_features)))
        )

        n_eval_samples = min(len(X_arr), 100)
        eval_samples = X_arr[:n_eval_samples]

        reconstruction_errors: List[float] = []

        for feat_idx in target_indices:
            feat_vals = eval_samples[:, feat_idx]
            feat_min, feat_max = float(np.min(feat_vals)), float(np.max(feat_vals))
            range_span = feat_max - feat_min if feat_max > feat_min else 1.0

            # Grid search reconstruction attempt
            target_confs = self._get_conf(model, eval_samples)
            if target_confs is None:
                continue

            grid = np.linspace(feat_min, feat_max, num=20)
            errors = []

            for sample_idx in range(len(eval_samples)):
                actual_val = eval_samples[sample_idx, feat_idx]
                target_conf = target_confs[sample_idx]

                best_guess = actual_val
                best_diff = float("inf")

                for candidate in grid:
                    candidate_sample = eval_samples[sample_idx].copy()
                    candidate_sample[feat_idx] = candidate
                    cand_conf = self._get_conf(model, candidate_sample.reshape(1, -1))
                    if cand_conf is not None:
                        diff = float(np.linalg.norm(cand_conf[0] - target_conf))
                        if diff < best_diff:
                            best_diff = diff
                            best_guess = candidate

                norm_error = abs(actual_val - best_guess) / range_span
                errors.append(norm_error)

            if errors:
                reconstruction_errors.append(float(np.mean(errors)))

        if not reconstruction_errors:
            return 0.0, {
                "inversion_risk_score": 0.0,
                "error": "Inversion search failed to evaluate features.",
            }

        avg_norm_error = float(np.mean(reconstruction_errors))

        # Lower reconstruction error = higher inversion risk!
        # Inversion score = 1.0 - normalized_error
        inversion_score = max(0.0, min(1.0, round(1.0 - avg_norm_error, 4)))

        details = {
            "inversion_risk_score": inversion_score,
            "avg_reconstruction_error": round(avg_norm_error, 4),
            "target_feature_indices": target_indices,
            "n_samples_evaluated": n_eval_samples,
        }

        return inversion_score, details

    def _get_conf(self, model: Any, X: np.ndarray) -> Optional[np.ndarray]:
        """Extract prediction confidence scores."""
        if hasattr(model, "predict_proba"):
            try:
                return model.predict_proba(X)
            except Exception:
                return None
        if hasattr(model, "decision_function"):
            try:
                res = model.decision_function(X)
                return res.reshape(-1, 1) if res.ndim == 1 else res
            except Exception:
                return None
        return None
