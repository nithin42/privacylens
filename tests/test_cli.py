"""Unit tests for privacylens CLI module."""

from __future__ import annotations

import os

import pytest
from click.testing import CliRunner
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from privacylens.cli import cli


@pytest.fixture
def trained_model_path(tmp_path):
    """Create a trained model pickle file for CLI testing."""
    import joblib

    X, y = make_classification(n_samples=200, n_features=10, random_state=42)
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X[:150], y[:150])
    model_path = tmp_path / "test_model.pkl"
    joblib.dump(model, model_path)
    return str(model_path)


@pytest.fixture
def csv_data_paths(tmp_path):
    """Create train and test CSV files for CLI testing."""
    import pandas as pd
    from sklearn.datasets import make_classification

    X, y = make_classification(n_samples=200, n_features=10, random_state=42)
    train_df = pd.DataFrame(X[:150])
    train_df["target"] = y[:150]
    test_df = pd.DataFrame(X[150:])
    test_df["target"] = y[150:]

    train_path = tmp_path / "train.csv"
    test_path = tmp_path / "test.csv"
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    return str(train_path), str(test_path)


class TestCLI:
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "privacylens" in result.output

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Audit ML models" in result.output

    def test_audit_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["audit", "--help"])
        assert result.exit_code == 0
        assert "MODEL_PATH" in result.output

    def test_audit_json_output(self, trained_model_path, csv_data_paths):
        train_path, test_path = csv_data_paths
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["audit", trained_model_path, train_path, test_path, "--output", "json", "--trust"],
        )
        assert result.exit_code == 0

    def test_audit_terminal_output(self, trained_model_path, csv_data_paths):
        train_path, test_path = csv_data_paths
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["audit", trained_model_path, train_path, test_path, "--trust"],
        )
        assert result.exit_code == 0

    def test_audit_invalid_model_path(self, csv_data_paths):
        train_path, test_path = csv_data_paths
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["audit", "nonexistent.pkl", train_path, test_path, "--trust"],
        )
        assert result.exit_code != 0

    def test_audit_no_mia_flag(self, trained_model_path, csv_data_paths):
        train_path, test_path = csv_data_paths
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["audit", trained_model_path, train_path, test_path, "--no-mia", "--trust"],
        )
        assert result.exit_code == 0

    def test_audit_html_report(self, trained_model_path, csv_data_paths, tmp_path):
        train_path, test_path = csv_data_paths
        report_path = str(tmp_path / "test_report.html")
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["audit", trained_model_path, train_path, test_path, "--report", report_path, "--trust"],
        )
        assert result.exit_code == 0
        assert os.path.exists(report_path)

    def test_logging_configuration(self):
        from privacylens._logging import get_logger

        logger = get_logger("privacylens.test")
        assert logger.name == "privacylens.test"
        assert len(logger.handlers) >= 1
