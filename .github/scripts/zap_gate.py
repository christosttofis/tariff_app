"""Pass/fail decision for the ZAP workflow.

Reads every zap-*.json report in the given folder, prints a summary of all
alerts to the job log (and the GitHub job summary), and exits non-zero only if
any alert is High risk. Medium/Low/Informational alerts are reported, not fatal.

High-risk findings that were investigated and confirmed as false positives are
listed in ACCEPTED below. They still appear in the summary, marked as accepted,
but don't fail the run. Each entry matches one rule, one method, one endpoint
and named parameters only, so the same rule anywhere else still fails the run.
Every entry must also be recorded in SECURITY_REMEDIATION_CHECKLIST.md.
"""
import json
import os
import re
import sys
from pathlib import Path

RISK = {"3": "High", "2": "Medium", "1": "Low", "0": "Info"}

ACCEPTED = [
    {
        "pluginid": "40018",   # SQL Injection
        "method": "PUT",
        "uri": r"^http://127\.0\.0\.1:8002/api/admin/profiles/[^/?#]+$",
        "params": {"name", "desc"},
        "why": "False positive (SECURITY_REMEDIATION_CHECKLIST.md, Round 16). The profile is saved through "
               "SQLAlchemy's ORM with bound parameters; the app has no SQL built from text. The endpoint echoes "
               "the whole saved profile, which ZAP's parallel attacks change between its AND/OR probes, so the "
               "two replies differ for reasons unrelated to the payload. Not reproducible: flagged in runs "
               "37010580557 and 37330744487, absent from the complete run 37285323887.",
    },
]


def accepted(alert, inst):
    return next((e for e in ACCEPTED
                 if alert.get("pluginid") == e["pluginid"]
                 and inst.get("method") == e["method"]
                 and re.match(e["uri"], inst.get("uri", ""))
                 and inst.get("param") in e["params"]), None)


folder = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
reports = sorted(folder.glob("zap-*.json"))
if not reports:
    print("No ZAP reports found - the scan did not run.")
    sys.exit(1)

lines = ["## ZAP scan results", ""]
high = 0
notes = []
for rep in reports:
    role = rep.stem.removeprefix("zap-")
    alerts = [a for site in json.loads(rep.read_text(encoding="utf-8")).get("site", [])
              for a in site.get("alerts", [])]
    alerts.sort(key=lambda a: -int(a["riskcode"]))
    lines += [f"### {role}: {len(alerts)} alert types", "", "| Risk | Alert | Count | Example |", "|---|---|---|---|"]
    for a in alerts:
        risk = RISK.get(a["riskcode"], a["riskcode"])
        instances = a.get("instances") or [{}]
        if risk == "High":
            open_ = [i for i in instances if not accepted(a, i)]
            for i in instances:
                if (e := accepted(a, i)):
                    notes.append(f"- **Accepted false positive:** {a['name']} on `{i.get('method')} {i.get('uri')}` "
                                 f"(param `{i.get('param')}`). {e['why']}")
            high += len(open_)
            if not open_:
                risk = "High (accepted)"
        example = instances[0]
        lines.append(f"| {risk} | {a['name']} | {a['count']} | `{example.get('method', '')} {example.get('uri', '')}` |")
    lines.append("")

lines += notes + ([""] if notes else [])
lines.append(f"**High-risk alerts: {high}** (the run fails only on these; accepted false positives are excluded)")
text = "\n".join(lines)
print(text)
if os.getenv("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
        f.write(text + "\n")
sys.exit(1 if high else 0)
