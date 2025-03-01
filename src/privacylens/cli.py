"""CLI entry point for privacylens using Click."""

from __future__ import annotations

import json
import sys

import click
from rich.console import Console

from privacylens import __version__


@click.group()
@click.version_option(__version__, prog_name="privacylens")
def cli() -> None:
    """🔍 privacylens — Audit ML models for privacy vulnerabilities."""


@cli.command()
@click.argument("model_path", type=click.Path(exists=True))
@click.argument("train_data", type=click.Path(exists=True))
@click.argument("test_data", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Choice(["terminal", "json"]), default="terminal",
              help="Output format: terminal table or JSON.")
@click.option("--no-mia", is_flag=True, default=False,
              help="Skip Membership Inference Attack check.")
def audit(model_path: str, train_data: str, test_data: str, output: str, no_mia: bool) -> None:
    """
    Audit a trained model for privacy vulnerabilities.

    MODEL_PATH: Path to saved model file (.pkl or .joblib).
    TRAIN_DATA: Path to training dataset CSV used to train the model.
    TEST_DATA:  Path to held-out test dataset CSV (not seen during training).

    Example:

        privacylens audit model.pkl train.csv test.csv

        privacylens audit model.pkl train.csv test.csv --output json
    """
    import joblib
    import pandas as pd
    from privacylens.auditor import audit as run_audit

    console = Console()

    try:
        model = joblib.load(model_path)
    except Exception as e:
        console.print(f"[red]❌ Failed to load model: {e}[/red]")
        sys.exit(1)

    try:
        train_df = pd.read_csv(train_data)
        test_df = pd.read_csv(test_data)
        X_train = train_df.iloc[:, :-1].values
        y_train = train_df.iloc[:, -1].values
        X_test = test_df.iloc[:, :-1].values
        y_test = test_df.iloc[:, -1].values
    except Exception as e:
        console.print(f"[red]❌ Failed to load data: {e}[/red]")
        sys.exit(1)

    report = run_audit(model, X_train, y_train, X_test, y_test, run_mia=not no_mia)

    if output == "json":
        console.print_json(json.dumps(report.to_dict(), indent=2))
    else:
        report.summary()


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
