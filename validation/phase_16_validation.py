"""Phase 16 validator wrapper: preserves the established validator while distinguishing
semantic failures from validator/runtime infrastructure faults.

A runtime/import/path/crash fault is RUNNER_ERROR, never a semantic detection. This wrapper is
assurance only and never governance authority.

Astra 6 remediation changed one historical positive MATCH fixture: an approved Workflow identity
and version are no longer sufficient when the planner payload omits Workflow-declared mandatory
requirements. The legacy core is intentionally preserved; this wrapper marks that single old
expectation as superseded only when the targeted Astra 6 validator passes.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEGACY = os.path.join(HERE, "_planner_activation_validator_core.py")
ASTRA_6 = os.path.join(HERE, "astra_6_remediation_validation.py")
SUPERSEDED_MATCH_CHECK = "an approved Workflow at its declared version proceeds"


def _run_json_validator(path, extra_args=()):
    args = [sys.executable, path, "--json"] + list(extra_args)
    return subprocess.run(args, capture_output=True, text=True, env=dict(os.environ))


def main():
    as_json = "--json" in sys.argv
    extra = ["--verbose"] if "--verbose" in sys.argv else []
    proc = _run_json_validator(LEGACY, extra)
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

    # Targeted Astra 6 validator is intentionally plain-text and returns 0 only when all targeted
    # remediation checks pass. It does not approve anything; it only allows this wrapper to state
    # transparently that the old C5d expectation has been superseded by the stronger MATCH rule.
    astra = subprocess.run(
        [sys.executable, ASTRA_6], capture_output=True, text=True, env=dict(os.environ))
    superseded = []
    if astra.returncode == 0:
        remaining = []
        for failure in report.get("failed", []):
            if str(failure.get("name", "")) == SUPERSEDED_MATCH_CHECK:
                superseded.append({
                    "name": SUPERSEDED_MATCH_CHECK,
                    "reason": "Astra 6 F1: approved identity/version no longer suffices when "
                              "mandatory Workflow requirements are omitted",
                })
            else:
                remaining.append(failure)
        if superseded:
            report["failed"] = remaining
            report["passed"] = int(report.get("total", 0)) - len(remaining)

    report["superseded"] = superseded
    report["astra_6_validator"] = {
        "status": "PASS" if astra.returncode == 0 else "FAIL",
        "output": (astra.stdout or astra.stderr or "")[-1500:],
    }

    status = "PASS" if report.get("passed") == report.get("total") else "FAIL"
    report["status"] = status
    report["runner_errors"] = []
    if as_json:
        print(json.dumps(report, indent=2))
    else:
        for failure in report.get("failed", []):
            print("FAIL  %s" % failure.get("name", "?"))
        for item in superseded:
            print("SUPERSEDED  %s" % item["name"])
        if astra.returncode != 0:
            print("FAIL  Astra 6 targeted remediation validator")
        print("=== %s %s/%s ===" % (status, report.get("passed"), report.get("total")))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())