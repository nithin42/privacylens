"""
privacylens — Enterprise Privacy Audit Benchmark Demo.

Demonstrates auditing a trained Random Forest classifier across all 5 privacy checks:
- Membership Inference Attack (MIA)
- PII Leakage Detection
- Model Inversion Risk Scoring
- Attribute Inference Risk
- Empirical Differential Privacy (ε) Estimator

And exporting the results to an interactive HTML report.
"""

from rich.console import Console
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from privacylens import audit


def main() -> None:
    console = Console()
    console.print("[bold cyan]Starting privacylens Enterprise Privacy Audit Benchmark...[/bold cyan]\n")

    # 1. Generate synthetic dataset
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 2. Train candidate model
    console.print("[yellow]Training RandomForestClassifier candidate model...[/yellow]")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 3. Execute Privacy Audit
    console.print("[yellow]Auditing model across all 5 privacy vulnerability checks...[/yellow]\n")
    report = audit(model, X_train, y_train, X_test, y_test)

    # 4. Display Rich Terminal Report
    report.summary()

    # 5. Export HTML Report
    html_file = report.to_html("privacy_audit_benchmark.html")
    console.print(f"\n[bold green]Interactive Compliance Report exported to: {html_file}[/bold green]")
    console.print("[bold green]Benchmark complete! privacylens is Production Ready.[/bold green]")


if __name__ == "__main__":
    main()
