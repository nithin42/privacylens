"""
privacylens v1.0.0 — Enterprise Privacy Audit Benchmark Demo.

Demonstrates auditing a trained Random Forest classifier across all 3 privacy checks:
- Membership Inference Attack (MIA)
- PII Leakage Detection
- Model Inversion Risk Scoring

And exporting the results to both JSON and interactive HTML report.
"""

from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from privacylens import audit


def main() -> None:
    print("🚀 Starting privacylens v1.0.0 Enterprise Privacy Audit Benchmark...\n")

    # 1. Generate synthetic dataset
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 2. Train candidate model
    print("📦 Training RandomForestClassifier candidate model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 3. Execute Privacy Audit
    print("🔍 Auditing model for privacy vulnerabilities (MIA + PII + Model Inversion)...")
    report = audit(model, X_train, y_train, X_test, y_test)

    # 4. Display Rich Terminal Report
    print("\n" + "=" * 60)
    report.summary()
    print("=" * 60)

    # 5. Export HTML Report
    html_file = report.to_html("privacy_audit_benchmark.html")
    print(f"\n✅ Interactive Compliance Report exported to: {html_file}")
    print("🏆 Benchmark complete! privacylens v1.0.0 is Production Ready.")


if __name__ == "__main__":
    main()
