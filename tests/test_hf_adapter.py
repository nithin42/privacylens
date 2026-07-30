"""Unit tests for HuggingFaceAdapter."""

from __future__ import annotations

from privacylens.adapters import get_adapter, BaseModelAdapter
from privacylens.adapters.hf_adapter import HuggingFaceAdapter


class TestHuggingFaceAdapter:
    def test_mock_huggingface_adapter(self):
        class MockHFModel:
            def eval(self):
                pass

            def __call__(self, x):
                return x

        model = MockHFModel()
        setattr(model, "__module__", "transformers.models.bert")

        adapter = get_adapter(model)
        assert isinstance(adapter, HuggingFaceAdapter)
        assert isinstance(adapter, BaseModelAdapter)
