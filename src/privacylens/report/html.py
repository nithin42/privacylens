"""
HTML Compliance Report Generator for privacylens.

Generates standalone, self-contained HTML audit reports for sharing
privacy compliance findings with security officers and GDPR/HIPAA auditors.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from jinja2 import Template

if TYPE_CHECKING:
    from privacylens.auditor import AuditReport

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>privacylens — Privacy Audit Report</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-color: #f8fafc;
            --text-muted: #94a3b8;
            --accent-cyan: #38bdf8;
            --low-color: #22c55e;
            --med-color: #eab308;
            --high-color: #ef4444;
            --border-color: #334155;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 40px 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            padding-bottom: 30px;
            border-bottom: 1px solid var(--border-color);
        }
        .header h1 {
            font-size: 2.2rem;
            color: var(--accent-cyan);
            margin: 0 0 10px 0;
        }
        .badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.95rem;
            text-transform: uppercase;
        }
        .badge-low { background-color: rgba(34, 197, 94, 0.2); color: var(--low-color); border: 1px solid var(--low-color); }
        .badge-medium { background-color: rgba(234, 179, 8, 0.2); color: var(--med-color); border: 1px solid var(--med-color); }
        .badge-high { background-color: rgba(239, 68, 68, 0.2); color: var(--high-color); border: 1px solid var(--high-color); }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
        }
        .card h3 {
            margin: 0 0 12px 0;
            color: var(--text-muted);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .score {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .findings {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            margin-top: 30px;
        }
        .findings h2 {
            margin-top: 0;
            color: var(--accent-cyan);
            font-size: 1.3rem;
        }
        .findings ul {
            padding-left: 20px;
            margin: 0;
        }
        .findings li {
            margin-bottom: 10px;
            line-height: 1.6;
        }
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 privacylens — Privacy Audit Report</h1>
            <p style="color: var(--text-muted);">Model: <strong>{{ report.model_type }}</strong></p>
            <div>
                Overall Risk Level:
                <span class="badge badge-{{ report.risk_level.lower() }}">{{ report.risk_level }}</span>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>Membership Inference</h3>
                <div class="score" style="color: {{ get_color(report.mia_score) }};">{{ "%.3f"|format(report.mia_score) }}</div>
                <div><span class="badge badge-{{ get_risk(report.mia_score).lower() }}">{{ get_risk(report.mia_score) }}</span></div>
            </div>
            <div class="card">
                <h3>PII Leakage Score</h3>
                <div class="score" style="color: {{ get_color(report.pii_score) }};">{{ "%.3f"|format(report.pii_score) }}</div>
                <div><span class="badge badge-{{ get_risk(report.pii_score).lower() }}">{{ get_risk(report.pii_score) }}</span></div>
            </div>
            <div class="card">
                <h3>Model Inversion Risk</h3>
                <div class="score" style="color: {{ get_color(report.inversion_score) }};">{{ "%.3f"|format(report.inversion_score) }}</div>
                <div><span class="badge badge-{{ get_risk(report.inversion_score).lower() }}">{{ get_risk(report.inversion_score) }}</span></div>
            </div>
        </div>

        <div class="findings">
            <h2>Audit Findings & Risk Notes</h2>
            <ul>
            {% for finding in report.findings %}
                <li>{{ finding }}</li>
            {% endfor %}
            </ul>
        </div>

        <div class="footer">
            Generated automatically by <strong>privacylens</strong> — Open-source ML Privacy Audit Framework
        </div>
    </div>
</body>
</html>
"""


def generate_html_report(report: AuditReport, output_path: str) -> str:
    """
    Render and save an AuditReport to a standalone HTML file.

    Args:
        report: AuditReport instance produced by audit().
        output_path: Target file path to write HTML report (e.g. 'audit.html').

    Returns:
        The output file path.
    """

    def get_risk(score: float) -> str:
        if score < 0.1:
            return "LOW"
        elif score < 0.3:
            return "MEDIUM"
        return "HIGH"

    def get_color(score: float) -> str:
        if score < 0.1:
            return "#22c55e"
        elif score < 0.3:
            return "#eab308"
        return "#ef4444"

    template = Template(HTML_TEMPLATE)
    html_content = template.render(
        report=report,
        get_risk=get_risk,
        get_color=get_color,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path
