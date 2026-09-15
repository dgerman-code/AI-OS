"""Phase 16 validator wrapper: preserves the established validator while distinguishing
semantic failures from validator/runtime infrastructure faults.

A runtime/import/path/crash fault is RUNNER_ERROR, never a semantic detection. This wrapper is
assurance only and never governance authority.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEGACY = os.path.join(HERE, "_planner_activation_validator_core.py")


def main():
    as_json = "--json" in sys.argv
    args = [sys.executable, LEGACY, "--json"]
    if "--verbose" in sys.argv:
        args.append("--verbose")
    proc = subprocess.run(args, capture_output=True, text=True, env=dict(os.environ))
    try:
        report = json.loads(proc.stdout)
    except Exception as err:
        payload = {
            "status": "RUNNER_ERROR",
            "runner_errors": ["validator produced malformed/no JSON: %s" % err],
            "stderr": (proc.stderr or "")[-500:],
        }
        if as_json:
            print(json.dumps(payload, indent=2))
        else:
            print("RUNNER_ERROR: %s" % payload["runner_errors"][0])
        return 2

    section_faults = []
    for failure in report.get("failed", []):
        name = str(failure.get("name", ""))
        evidence = str(failure.get("evidence", ""))
        if name.startswith("section raised "):
            section_faults.append("%s: %s" % (name, evidence))

    if section_faults:
        payload = {
            "status": "RUNNER_ERROR",
            "runner_errors": section_faults,
            "semantic_report": report,
        }
        if as_json:
            print(json.dumps(payload, indent=2))
        else:
            print("RUNNER_ERROR")
            for item in section_faults:
                print("  - %s" % item)
        return 2

    status = "PASS" if report.get("passed") == report.get("total") else "FAIL"
    report["status"] = status
    report["runner_errors"] = []
    if as_json:
        print(json.dumps(report, indent=2))
    else:
        for failure in report.get("failed", []):
            print("FAIL  %s" % failure.get("name", "?"))
        print("=== %s %s/%s ===" % (status, report.get("passed"), report.get("total")))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
