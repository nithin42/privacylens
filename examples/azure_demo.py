"""
privacylens v1.1.0 — Azure Machine Learning & Azure OpenAI Demo Script.

Demonstrates executing an automated Azure MLOps privacy audit step,
logging metrics, and exporting the Azure ML HTML Compliance Report.
"""

from rich.console import Console
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from privacylens.integrations import AzureMLAuditStep, AzureOpenAIAuditor


def main() -> None:
    console = Console()
    console.print("[bold cyan]Executing Azure MLOps Privacy Governance Step...[/bold cyan]\n")

    # 1. Simulate Azure ML Pipeline Training
    console.print("[yellow]1. Training candidate model inside Azure ML Pipeline job...[/yellow]")
    X, y = make_classification(n_samples=500, n_features=15, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # 2. Execute Azure ML Audit Step
    console.print("[yellow]2. Running AzureMLAuditStep 5-point privacy check...[/yellow]")
    azure_step = AzureMLAuditStep(workspace_name="demo-azureml-workspace")
    report = azure_step.run_pipeline_audit(
        model=model,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        output_report_path="azureml_privacy_report.html",
    )

    # 3. Display Terminal Table
    report.summary()

    # 4. Audit Azure OpenAI Fine-Tuned Model Deployment
    console.print("\n[yellow]3. Auditing Azure OpenAI Service Fine-Tuned Model...[/yellow]")
    aoai_auditor = AzureOpenAIAuditor(
        endpoint="https://my-aoai.openai.azure.com/",
        deployment_name="gpt-4",
    )

    prompts = [
        "User SSN is 123-45-6789",
        "Contact email user@enterprise.com",
        "What is the capital of Washington state?",
    ]

    score, details = aoai_auditor.audit_deployment(prompts)
    console.print(f"[bold green]Azure OpenAI PII Leakage Score: {score:.3f}[/bold green]")
    console.print(f"Flagged Prompts: {details['flagged_prompts']} / {details['total_prompts']}")

    console.print(
        "\n[bold green]Demo Complete! HTML report generated: azureml_privacy_report.html[/bold green]"
    )


if __name__ == "__main__":
    main()
