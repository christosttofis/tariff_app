"""Pass/fail decision for the ZAP workflow.

Reads every zap-*.json report in the given folder, prints a summary of all
alerts to the job log (and the GitHub job summary), and exits non-zero only if
any alert is High risk. Medium/Low/Informational alerts are reported, not fatal.
"""
import json
import os
import sys
from pathlib import Path

RISK = {"3": "High", "2": "Medium", "1": "Low", "0": "Info"}

folder = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
reports = sorted(folder.glob("zap-*.json"))
if not reports:
    print("No ZAP reports found - the scan did not run.")
    sys.exit(1)

lines = ["## ZAP scan results", ""]
high = 0
for rep in reports:
    role = rep.stem.removeprefix("zap-")
    alerts = [a for site in json.loads(rep.read_text(encoding="utf-8")).get("site", [])
              for a in site.get("alerts", [])]
    alerts.sort(key=lambda a: -int(a["riskcode"]))
    lines += [f"### {role}: {len(alerts)} alert types", "", "| Risk | Alert | Count | Example |", "|---|---|---|---|"]
    for a in alerts:
        risk = RISK.get(a["riskcode"], a["riskcode"])
        high += risk == "High"
        example = (a.get("instances") or [{}])[0]
        lines.append(f"| {risk} | {a['name']} | {a['count']} | `{example.get('method', '')} {example.get('uri', '')}` |")
    lines.append("")

lines.append(f"**High-risk alerts: {high}** (the run fails only on these)")
text = "\n".join(lines)
print(text)
if os.getenv("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
        f.write(text + "\n")
sys.exit(1 if high else 0)
