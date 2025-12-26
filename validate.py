import argparse, json
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="SOC2 Evidence Validator")
    p.add_argument("--input", required=True, help="Evidence folder path")
    p.add_argument("--output", default="report.html", help="Output HTML report")
    args = p.parse_args()

    evidence = Path(args.input)
    if not evidence.exists():
        raise SystemExit(f"Input path does not exist: {evidence}")

    controls_path = Path(__file__).with_name("controls.json")
    controls = json.loads(controls_path.read_text(encoding="utf-8"))

    files = [f for f in evidence.rglob("*") if f.is_file()]
    html = f"""<!doctype html><html><meta charset="utf-8">
<title>SOC2 Evidence Report</title><body>
<h1>SOC2 Evidence Validator</h1>
<p><b>Evidence path:</b> {evidence}</p>
<p><b>Files found:</b> {len(files)}</p>
<p><b>Controls loaded:</b> {len(controls.get("controls", []))}</p>
</body></html>"""
    Path(args.output).write_text(html, encoding="utf-8")
    print(f"Report written to: {args.output}")

if __name__ == "__main__":
    main()
