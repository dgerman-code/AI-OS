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
    "tests/FINAL_COLD_START_TEST_RESULT.md",
    "reviews/phase-17-final-approval.md",
    "reviews/phase-18-final-approval.md",
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
    "tests/FINAL_COLD_START_TEST_RESULT.md",
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


def semantic_segments(value):
    raw = value.lower()
    raw = re.sub(r"[*_`~]+", "", raw)
    return [part.strip() for part in re.split(r"[\n.!?;]+", raw) if part.strip()]


def has_active_mode_b_claim(value):
    unsafe = [
        r"\bmode b\b.{0,35}\b(is|remains|now|currently)\s+(active|enabled|implemented|operational)\b",
        r"\b(ai-os|system)\b.{0,35}\b(calls|invokes|routes)\b.{0,25}\b(provider|model)\s+apis?\b",
    ]
    safe_markers = ["not active", "not implemented", "deferred", "out of scope", "must not be implemented", "does not call"]
    for segment in semantic_segments(value):
        if any(marker in segment for marker in safe_markers):
            continue
        if any(re.search(pattern, segment) for pattern in unsafe):
            return True
    return False


def has_mass_promotion_claim(value):
    unsafe = [
        r"\ball\s+(skills?|workflows?|roles?|artifacts?)\s+(are|become|became)\s+(approved|canonical)\b",
        r"\bphase approval\b.{0,45}\b(all|every)\b.{0,20}\b(approved|canonical)\b",
        r"\bchild artifacts?\b.{0,30}\bautomatically\s+(approved|canonical)\b",
    ]
    for segment in semantic_segments(value):
        if any(re.search(pattern, segment) for pattern in unsafe):
            if "does not" not in segment and "not " not in segment and "do not" not in segment:
                return True
    return False


def has_unsupported_production_claim(value):
    """Reject affirmative production/deployment claims, not negative scope notes."""
    unsafe = [
        r"\b(ai-os|system|repository|programme)\b.{0,25}\b(is|remains|now|currently)\s+production[- ]ready\b",
        r"\b(ai-os|system|repository|programme)\b.{0,25}\b(is|now|currently)\s+ready\s+for\s+production\b",
        r"\b(ai-os|system|service)\b.{0,25}\b(is|has been)\s+deployed\s+(to|in)\s+production\b",
        r"\bproduction\s+deployment\s+(is|has been)\s+complete\b",
    ]
    for segment in semantic_segments(value):
        if any(re.search(pattern, segment) for pattern in unsafe):
            if any(marker in segment for marker in ("not production", "does not claim", "not claim", "no deployed", "not deployed")):
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
        check(completion.get("final_cold_start_test_result") == "tests/FINAL_COLD_START_TEST_RESULT.md", "manifest:cold-start-result", "cold-start result mapped", results)
        approvals = manifest.get("approvals", {})
        check(approvals.get("phase_18") == "reviews/phase-18-final-approval.md", "manifest:phase18-approval", "Phase 18 approval record mapped", results)
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
    check("5ab13b4b99cc46e7b68bf370b0230e0af59daef4" in status_text,
          "status:phase18-approval", "Phase 18 human approval commit recorded", results)
    check("phase 1–18 approved" in status_text.lower() or "phase 1-18 approved" in status_text.lower(),
          "status:phase18-current", "system status reflects Phase 18 approval rather than completion-candidate state", results)
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
    check("REUSABLE POST-APPROVAL TEST PROCEDURE" in test_plan,
          "test-plan:post-approval-procedure", "cold-start plan is retained as a reusable post-approval procedure", results)
    check("read-only" in test_plan.lower() and "no repository changes" in test_plan.lower(),
          "test-plan:read-only", "cold-start plan requires read-only/no-write behaviour", results)

    phase18_approval = text("reviews/phase-18-final-approval.md") if (ROOT / "reviews/phase-18-final-approval.md").exists() else ""
    check("APPROVED — HUMAN DECISION" in phase18_approval and
          "eb8a64ec5e79589f7def3a96a740d004f59236f8" in phase18_approval,
          "phase18:human-approval", "Phase 18 explicit human approval and reviewed baseline are recorded", results)

    cold_start = text("tests/FINAL_COLD_START_TEST_RESULT.md") if (ROOT / "tests/FINAL_COLD_START_TEST_RESULT.md").exists() else ""
    check("PASS WITH NON-BLOCKING NOTES" in cold_start and
          "5ab13b4b99cc46e7b68bf370b0230e0af59daef4" in cold_start,
          "cold-start:recorded-pass", "first post-approval cold-start PASS is recorded at an exact tested SHA", results)
    check("read-only" in cold_start.lower() and
          ("no repository modifications" in cold_start.lower() or "no repository changes" in cold_start.lower()),
          "cold-start:no-write", "recorded cold-start preserves read-only/no-write operation", results)
    check("NO_AUTHORITY_EXERCISED" in cold_start,
          "cold-start:no-authority", "recorded cold-start did not exercise human authority", results)

    access = text("docs/GITHUB_ACCESS_MODEL.md") if (ROOT / "docs/GITHUB_ACCESS_MODEL.md").exists() else ""
    check("read-only" in access.lower() and "least privilege" in access.lower(),
          "access:least-privilege", "read-only least-privilege default documented", results)
    check("recommendations only" in access.lower() or "does not claim" in access.lower(),
          "access:no-settings-claim", "guidance does not pretend repository settings were changed", results)

    # Small semantic self-controls for the completion-specific detectors.
    check(has_active_mode_b_claim("Mode B is currently active."),
          "selfcontrol:active-mode-b", "active Mode B claim is detected", results)
    check(not has_active_mode_b_claim("Mode B is deferred and not implemented."),
          "selfcontrol:safe-mode-b", "deferred Mode B wording is accepted", results)
    check(has_mass_promotion_claim("All Skills are approved."),
          "selfcontrol:mass-promotion", "mass Skill approval claim is detected", results)
    check(has_unsupported_production_claim("AI-OS is production-ready."),
          "selfcontrol:production-claim", "affirmative production-readiness claim is detected", results)
    check(not has_unsupported_production_claim("AI-OS does not claim production readiness."),
          "selfcontrol:safe-production-boundary", "negative production boundary is accepted", results)

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
