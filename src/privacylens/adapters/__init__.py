"""adapters package for privacylens."""

from privacylens.adapters.base import BaseModelAdapter, get_adapter
from privacylens.adapters.hf_adapter import HuggingFaceAdapter
from privacylens.adapters.pytorch_adapter import PyTorchAdapter
from privacylens.adapters.sklearn_adapter import SklearnAdapter
from privacylens.adapters.xgboost_adapter import XGBoostAdapter

__all__ = [
    "BaseModelAdapter",
    "get_adapter",
    "SklearnAdapter",
    "PyTorchAdapter",
    "XGBoostAdapter",
    "HuggingFaceAdapter",
]
