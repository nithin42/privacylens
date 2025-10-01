"""Adapter for scikit-learn compatible classifiers."""

from __future__ import annotations

from typing import Optional

import numpy as np

from privacylens.adapters.base import BaseModelAdapter


class SklearnAdapter(BaseModelAdapter):
    """Adapter for scikit-learn models implementing predict_proba or decision_function."""

    def get_confidence(self, X: np.ndarray) -> Optional[np.ndarray]:
        X_arr = np.array(X)
        if hasattr(self.model, "predict_proba"):
            try:
                return self.model.predict_proba(X_arr)
            except Exception:
                pass
        if hasattr(self.model, "decision_function"):
            try:
                scores = self.model.decision_function(X_arr)
                return scores.reshape(-1, 1) if scores.ndim == 1 else scores
            except Exception:
                pass
        return None

    def predict(self, X: np.ndarray) -> np.ndarray:
        X_arr = np.array(X)
        if hasattr(self.model, "predict"):
            return self.model.predict(X_arr)
        conf = self.get_confidence(X_arr)
        if conf is not None:
            return np.argmax(conf, axis=1)
        return np.zeros(len(X_arr))
