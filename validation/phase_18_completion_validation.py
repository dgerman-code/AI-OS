#!/usr/bin/env python3
"""Static completion checks for Phase 18.

This validator checks repository completion/onboarding consistency only. It does
not create governance approval, validate production deployment, or implement
Mode B.
"""

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "SYSTEM_STATUS.md",
    "AI_OS_ENTRYPOINT.md",
    "ai-os.yaml",
    "contracts/ai-result-envelope.schema.json",
    "docs/HOW_TO_CONNECT_ANY_AI.md",
    "docs/MAIN_READINESS.md",
    "docs/MODE_A_OPERATIONAL_CHECKLIST.md",
    "docs/GITHUB_ACCESS_MODEL.md",
    "tests/FINAL_COLD_START_TEST_PLAN.md",
    "reviews/phase-17-final-approval.md",
    "validation/phase_17_mode_a_validation.py",
    "adapters/mode-a/generic.md",
    "adapters/mode-a/openai-chatgpt.md",
    "adapters/mode-a/anthropic-claude.md",
    "adapters/mode-a/openai-codex.md",
    "adapters/mode-a/google-gemini.md",
]

COMPLETION_DOCS = [
    "README.md",
    "SYSTEM_STATUS.md",
    "AI_OS_ENTRYPOINT.md",
    "docs/MAIN_READINESS.md",
    "docs/MODE_A_OPERATIONAL_CHECKLIST.md",
    "docs/GITHUB_ACCESS_MODEL.md",
    "tests/FINAL_COLD_START_TEST_PLAN.md",
]


def check(condition, name, detail, results):
    results.append({"name": name, "pass": bool(condition), "detail": detail})


def text(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def normalize(value):
    value = value.lower()
    value = re.sub(r"[*_`~]+", "", value)
    value = re.sub(r"\s+", " ", value)
    return value


def has_active_mode_b_claim(value):
    """Reject affirmative statements that make Mode B active/current.

    Negative/deferred wording is accepted. Keep this deliberately narrow: Phase
    18 is a completion validator, while Phase 17 owns detailed Mode A conformance.
    """
    t = normalize(value)
    unsafe = [
        r"\bmode b\b.{0,35}\b(is|remains|now|currently)\s+(active|enabled|implemented|operational)\b",
        r"\b(ai-os|system)\b.{0,35}\b(calls|invokes|routes)\b.{0,25}\b(provider|model)\s+apis?\b",
    ]
    safe_markers = ["not active", "not implemented", "deferred", "out of scope", "must not be implemented"]
    if any(marker in t for marker in safe_markers):
        # Still scan by sentence so one safe clause cannot hide another unsafe claim.
        pass
    for segment in re.split(r"[\n.!?;]+", t):
        segment = segment.strip()
        if not segment:
            continue
        if any(marker in segment for marker in safe_markers):
            continue
        if any(re.search(pattern, segment) for pattern in unsafe):
            return True
    return False


def has_mass_promotion_claim(value):
    t = normalize(value)
    unsafe = [
        r"\ball\s+(skills?|workflows?|roles?|artifacts?)\s+(are|become|became)\s+(approved|canonical)\b",
        r"\bphase approval\b.{0,45}\b(all|every)\b.{0,20}\b(approved|canonical)\b",
        r"\bchild artifacts?\b.{0,30}\bautomatically\s+(approved|canonical)\b",
    ]
    for segment in re.split(r"[\n.!?;]+", t):
        if any(re.search(pattern, segment) for pattern in unsafe):
            if "does not" not in segment and "not " not in segment and "do not" not in segment:
                return True
    return False


def has_unsupported_production_claim(value):
    t = normalize(value)
    unsafe = [
        r"\bproduction[- ]ready\b",
        r"\bready for production\b",
        r"\bdeployed production service\b",
        r"\bproduction deployment is complete\b",
    ]
    for segment in re.split(r"[\n.!?;]+", t):
        if not any(re.search(pattern, segment) for pattern in unsafe):
            continue
        if any(marker in segment for marker in ("not production", "does not claim", "not claim", "no deployed", "not a deployed")):
            continue
        return True
    return False


def main_validate():
    results = []

    for rel in REQUIRED:
        check((ROOT / rel).exists(), f"required:{rel}", "required completion artifact exists", results)

    manifest = None
    manifest_path = ROOT / "ai-os.yaml"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            check(True, "manifest:parse", "JSON-compatible YAML parsed", results)
        except Exception as exc:
            check(False, "manifest:parse", f"{type(exc).__name__}: {exc}", results)

    if manifest is not None:
        check(manifest.get("mode") == "A", "manifest:mode-a", "approved active connection mode remains A", results)
        check(manifest.get("entrypoint") == "AI_OS_ENTRYPOINT.md", "manifest:entrypoint", "root entrypoint unchanged", results)
        completion = manifest.get("completion", {})
        check(completion.get("system_status") == "SYSTEM_STATUS.md", "manifest:system-status", "completion status mapped", results)
        check(completion.get("main_readiness") == "docs/MAIN_READINESS.md", "manifest:main-readiness", "main-readiness mapped", results)
        check(completion.get("mode_a_operational_checklist") == "docs/MODE_A_OPERATIONAL_CHECKLIST.md", "manifest:mode-a-checklist", "Mode A checklist mapped", results)
        check(completion.get("github_access_model") == "docs/GITHUB_ACCESS_MODEL.md", "manifest:access-model", "access model mapped", results)
        check(completion.get("final_cold_start_test_plan") == "tests/FINAL_COLD_START_TEST_PLAN.md", "manifest:cold-start-plan", "cold-start plan mapped", results)
        deferred = " ".join(str(x) for x in manifest.get("prohibited_assumptions", [])) + " " + str(manifest.get("mode_b_status", ""))
        check("mode b" in deferred.lower() and "defer" in deferred.lower(), "manifest:mode-b-deferred", "Mode B explicitly deferred", results)

    combined = "\n".join(text(rel) for rel in COMPLETION_DOCS if (ROOT / rel).exists())
    low = normalize(combined)

    check("human authority" in low or "human approval" in low,
          "completion:human-authority", "human authority boundary remains visible", results)
    check("provider memory" in low and "canonical" in low and ("not canonical" in low or "does not become canonical" in low),
          "completion:provider-memory", "provider memory is explicitly non-canonical", results)
    check(not has_active_mode_b_claim(combined),
          "completion:no-active-mode-b", "completion docs do not activate Mode B", results)
    check(not has_mass_promotion_claim(combined),
          "completion:no-mass-promotion", "completion docs do not mass-promote child artifacts", results)
    check(not has_unsupported_production_claim(combined),
          "completion:no-production-claim", "no unsupported production/deployment readiness claim", results)

    status_text = text("SYSTEM_STATUS.md") if (ROOT / "SYSTEM_STATUS.md").exists() else ""
    check("352c2f056177e43f422b008042b7296799742958" in status_text,
          "status:phase17-approval", "Phase 17 approval commit recorded", results)
    check("47c1c5299db900373cf1adb0efba3bc6820eb226" in status_text,
          "status:phase17-baseline", "Phase 17 approved baseline recorded", results)
    check("does not" in status_text.lower() and "every child" in status_text.lower(),
          "status:no-child-auto-approval", "phase approval does not imply child approval", results)

    readme = text("README.md") if (ROOT / "README.md").exists() else ""
    check("SYSTEM_STATUS.md" in readme and "AI_OS_ENTRYPOINT.md" in readme and "ai-os.yaml" in readme,
          "root:onboarding-links", "README points to status/entrypoint/manifest", results)
    check("Mode A" in readme and "Mode B" in readme,
          "root:modes", "README distinguishes Mode A and Mode B", results)

    entry = text("AI_OS_ENTRYPOINT.md") if (ROOT / "AI_OS_ENTRYPOINT.md").exists() else ""
    check("SYSTEM_STATUS.md" in entry,
          "entrypoint:status-link", "entrypoint points to completion status", results)
    check("exact commit" in entry.lower() and "fail closed" in entry.lower(),
          "entrypoint:provenance", "entrypoint retains exact-source/fail-closed boundary", results)

    test_plan = text("tests/FINAL_COLD_START_TEST_PLAN.md") if (ROOT / "tests/FINAL_COLD_START_TEST_PLAN.md").exists() else ""
    check("DO NOT EXECUTE BEFORE PHASE 18 HUMAN APPROVAL" in test_plan,
          "test-plan:not-executed", "cold-start test explicitly deferred until after approval", results)
    check("read-only" in test_plan.lower() and "no repository changes" in test_plan.lower(),
          "test-plan:read-only", "cold-start plan requires read-only/no-write behaviour", results)

    access = text("docs/GITHUB_ACCESS_MODEL.md") if (ROOT / "docs/GITHUB_ACCESS_MODEL.md").exists() else ""
    check("read-only" in access.lower() and "least privilege" in access.lower(),
          "access:least-privilege", "read-only least-privilege default documented", results)
    check("recommendations only" in access.lower() or "does not claim" in access.lower(),
          "access:no-settings-claim", "guidance does not pretend repository settings were changed", results)

    failed = [r for r in results if not r["pass"]]
    return results, failed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results, failed = main_validate()
    report = {
        "status": "PASS" if not failed else "FAIL",
        "passed": len(results) - len(failed),
        "total": len(results),
        "failed": failed,
    }

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for row in results:
            print(f"{'PASS' if row['pass'] else 'FAIL'} {row['name']} — {row['detail']}")
        print(f"=== {report['status']} {report['passed']}/{report['total']} ===")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
