"""
Base Model Adapter interface for privacylens.

Provides unified prediction and confidence scoring methods across
scikit-learn, PyTorch, and XGBoost models.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

import numpy as np


class BaseModelAdapter(ABC):
    """Abstract base class for all framework-specific model adapters."""

    def __init__(self, model: Any) -> None:
        self.model = model

    @abstractmethod
    def get_confidence(self, X: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract output probability/confidence matrix of shape (n_samples, n_classes).

        Returns:
            np.ndarray of probability scores, or None if not supported.
        """
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Return predicted class labels.

        Returns:
            np.ndarray of predicted class indices or labels.
        """
        pass


def get_adapter(model: Any) -> BaseModelAdapter:
    """
    Factory function to select and instantiate the appropriate BaseModelAdapter.

    Args:
        model: Trained model instance (scikit-learn, PyTorch nn.Module, or XGBoost).

    Returns:
        BaseModelAdapter instance wrapping the model.
    """
    model_module = (getattr(model, "__module__", "") or type(model).__module__).lower()
    model_name = type(model).__name__.lower()

    if "transformers" in model_module or "huggingface" in model_module or "hf" in model_name:
        from privacylens.adapters.hf_adapter import HuggingFaceAdapter
        return HuggingFaceAdapter(model)
    elif "torch" in model_module or "module" in model_name:
        from privacylens.adapters.pytorch_adapter import PyTorchAdapter
        return PyTorchAdapter(model)
    elif "xgboost" in model_module or "xgb" in model_name:
        from privacylens.adapters.xgboost_adapter import XGBoostAdapter
        return XGBoostAdapter(model)
    else:
        from privacylens.adapters.sklearn_adapter import SklearnAdapter
        return SklearnAdapter(model)
