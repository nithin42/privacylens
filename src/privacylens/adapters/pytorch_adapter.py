"""Adapter for PyTorch nn.Module models."""

from __future__ import annotations

from typing import Optional

import numpy as np

from privacylens.adapters.base import BaseModelAdapter


class PyTorchAdapter(BaseModelAdapter):
    """Adapter for PyTorch nn.Module models, converting raw logits into probabilities."""

    def get_confidence(self, X: np.ndarray) -> Optional[np.ndarray]:
        X_arr = np.array(X, dtype=np.float32)
        try:
            import torch

            self.model.eval()
            with torch.no_grad():
                tensor_in = torch.from_numpy(X_arr)
                logits = self.model(tensor_in)
                if hasattr(logits, "detach"):
                    logits = logits.detach().cpu().numpy()
                probs = np.exp(logits - np.max(logits, axis=1, keepdims=True))
                probs = probs / np.sum(probs, axis=1, keepdims=True)
                return probs
        except Exception:
            return None

    def predict(self, X: np.ndarray) -> np.ndarray:
        conf = self.get_confidence(X)
        if conf is not None:
            return np.argmax(conf, axis=1)
        return np.zeros(len(X))
