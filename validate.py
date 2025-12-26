import argparse
import json
import uuid
from pathlib import Path
from datetime import datetime


def render_report(template_path: Path, output_path: Path, context: dict):
    template = template_path.read_text(encoding="utf-8")

    for key, value in context.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))

    output_path.write_text(template, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="SOC2 Evidence Validator")
    parser.add_argument("--input", required=True, help="Evidence folder path")
    parser.add_argument("--output", default="report.html", help="Output HTML report")
    args = parser.parse_args()

    evidence_path = Path(args.input)
    if not evidence_path.exists():
        raise SystemExit(f"Input path does not exist: {evidence_path}")

    controls_path = Path(__file__).with_name("controls.json")
    template_path = Path(__file__).with_name("report_template.html")
    output_path = Path(args.output)

    controls = json.loads(controls_path.read_text(encoding="utf-8"))
    files = [f for f in evidence_path.rglob("*") if f.is_file()]

    context = {
        "report_id": f"SCRL-{uuid.uuid4().hex[:8].upper()}",
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "validator_version": "1.0.0",
        "client_or_system": "Demo SaaS Platform",
        "standard": "SOC 2 Type II",
        "evidence_scope": "Access control, logging, governance",
        "evidence_path": evidence_path,
        "files_scanned": len(files),
        "controls_mapped": len(controls.get("controls", [])),
        "findings_total": 3,
        "crit_high_count": 1,
        "evidence_gaps_count": 1,
        "retest_required": "Yes",
        "proof_ref_1": "access_review_q3.pdf",
        "proof_ref_2": "logs_export.csv",
        "proof_ref_3": "policy_docs/",
        "owner_1": "Security Lead",
        "owner_2": "DevOps",
        "owner_3": "Compliance",
        "evidence_cc11": "policies/*.pdf",
        "evidence_cc21": "logs/*.csv",
        "evidence_cc61": "iam_exports/*.json",
    }

    render_report(
        template_path=template_path,
        output_path=output_path,
        context=context,
    )

    print(f"Report written to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
