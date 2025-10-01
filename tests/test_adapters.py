"""Unit tests for framework adapters (Sklearn, PyTorch, XGBoost)."""

from __future__ import annotations

from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from privacylens.adapters import get_adapter, BaseModelAdapter
from privacylens.adapters.sklearn_adapter import SklearnAdapter


class TestAdapters:
    def test_sklearn_adapter_factory(self):
        X, y = make_classification(n_samples=100, n_features=5, random_state=42)
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X, y)

        adapter = get_adapter(model)
        assert isinstance(adapter, SklearnAdapter)
        assert isinstance(adapter, BaseModelAdapter)

        conf = adapter.get_confidence(X[:10])
        assert conf is not None
        assert conf.shape == (10, 2)

        preds = adapter.predict(X[:10])
        assert len(preds) == 10

    def test_mock_pytorch_adapter(self):
        class MockPyTorchModel:

            def eval(self):
                pass

            def __call__(self, x):
                return x

        model = MockPyTorchModel()
        setattr(model, "__module__", "torch.nn.modules")

        adapter = get_adapter(model)
        assert type(adapter).__name__ == "PyTorchAdapter"

    def test_mock_xgboost_adapter(self):
        class MockXGBModel:
            pass

        model = MockXGBModel()
        setattr(model, "__module__", "xgboost.core")

        adapter = get_adapter(model)
        assert type(adapter).__name__ == "XGBoostAdapter"
