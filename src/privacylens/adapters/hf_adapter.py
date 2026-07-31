"""Adapter for HuggingFace Transformers models and pipelines."""

from __future__ import annotations

from typing import Optional

import numpy as np

from privacylens.adapters.base import BaseModelAdapter


class HuggingFaceAdapter(BaseModelAdapter):
    """Adapter for HuggingFace Transformers models, converting text outputs or logits into probabilities."""

    def get_confidence(self, X: np.ndarray) -> Optional[np.ndarray]:
        try:
            import torch

            if hasattr(self.model, "eval"):
                self.model.eval()

            # Handle HuggingFace Pipeline
            if hasattr(self.model, "task"):
                results = self.model(list(X.flat))
                confs = []
                for item in results:
                    if isinstance(item, list) and item and "score" in item[0]:
                        confs.append([score_dict["score"] for score_dict in item])
                    elif isinstance(item, dict) and "score" in item:
                        confs.append([item["score"], 1.0 - item["score"]])
                if confs:
                    return np.array(confs)

            # Handle PreTrainedModel directly
            X_arr = np.array(X, dtype=np.float32)
            with torch.no_grad():
                tensor_in = torch.from_numpy(X_arr)
                outputs = self.model(tensor_in)
                logits = getattr(outputs, "logits", outputs)
                if hasattr(logits, "detach"):
                    logits = logits.detach().cpu().numpy()
                probs = np.exp(logits - np.max(logits, axis=1, keepdims=True))
                return probs / np.sum(probs, axis=1, keepdims=True)
        except Exception:
            return None

    def predict(self, X: np.ndarray) -> np.ndarray:
        conf = self.get_confidence(X)
        if conf is not None:
            return np.argmax(conf, axis=1)
        return np.zeros(len(X))
