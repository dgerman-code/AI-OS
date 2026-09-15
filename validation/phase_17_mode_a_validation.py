#!/usr/bin/env python3
"""Static fail-closed conformance checks for Phase 17 Mode A.

No runtime service, provider API or model invocation is performed.
"""

import argparse
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(os.environ.get("AI_OS_REPO_ROOT", pathlib.Path(__file__).resolve().parents[1]))

REQUIRED = [
    "AI_OS_ENTRYPOINT.md",
    "ai-os.yaml",
    "docs/HOW_TO_CONNECT_ANY_AI.md",
    "contracts/ai-result-envelope.schema.json",
    "adapters/mode-a/generic.md",
    "adapters/mode-a/openai-chatgpt.md",
    "adapters/mode-a/anthropic-claude.md",
    "adapters/mode-a/openai-codex.md",
    "adapters/mode-a/google-gemini.md",
    "examples/mode-a-generic-session.md",
]

CRITICAL_MANIFEST_PATH_KEYS = [
    ("entrypoint",),
    ("registries", "roles"),
    ("registries", "skills"),
    ("registries", "workflows"),
    ("registries", "review_profiles"),
    ("registries", "decision_rights"),
    ("registries", "models"),
    ("planning", "architecture"),
    ("planning", "activation"),
    ("planning", "orchestrator"),
    ("approvals", "records"),
    ("canonical_and_memory", "knowledge"),
    ("result_envelope",),
    ("connection_guide",),
]

ADAPTERS = [
    "adapters/mode-a/generic.md",
    "adapters/mode-a/openai-chatgpt.md",
    "adapters/mode-a/anthropic-claude.md",
    "adapters/mode-a/openai-codex.md",
    "adapters/mode-a/google-gemini.md",
]

# Only affirmative governance-fork language is forbidden. Negative statements such as
# "adds no provider-specific Role" and "cannot self-approve" are required safety language.
FORBIDDEN_ADAPTER_GOVERNANCE = [
    "provider-specific role is authoritative",
    "provider-specific workflow is authoritative",
    "provider-specific decision right is authoritative",
    "provider memory is canonical",
    "automatically approved by the provider",
    "the provider may approve governance",
]


def path_value(obj, keys):
    cur = obj
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def check(condition, name, detail, results):
    results.append({"name": name, "pass": bool(condition), "detail": detail})


def validate():
    results = []

    for rel in REQUIRED:
        check((ROOT / rel).exists(), "required:%s" % rel, "required artifact exists", results)

    manifest_path = ROOT / "ai-os.yaml"
    manifest = None
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            check(True, "manifest:parse", "JSON-compatible YAML parsed", results)
        except Exception as exc:
            check(False, "manifest:parse", "%s: %s" % (type(exc).__name__, exc), results)
    else:
        check(False, "manifest:parse", "manifest missing", results)

    if manifest is not None:
        check(manifest.get("schema") == "ai-os-manifest/v1", "manifest:schema", "schema is ai-os-manifest/v1", results)
        check(manifest.get("mode") == "A", "manifest:mode", "Mode A only", results)
        check(manifest.get("repository") == "dgerman-code/AI-OS", "manifest:repository", "repository identity fixed", results)
        for keys in CRITICAL_MANIFEST_PATH_KEYS:
            rel = path_value(manifest, keys)
            ok = isinstance(rel, str) and bool(rel) and (ROOT / rel).exists()
            check(ok, "manifest:path:%s" % ".".join(keys), str(rel), results)

        skill_rule = str(manifest.get("skill_eligibility_rule", "")).lower()
        check("card" in skill_rule and "not" in skill_rule and "approval" in skill_rule,
              "manifest:skill-eligibility",
              "card existence/applicability is explicitly separated from approval",
              results)

        prohibited = " ".join(manifest.get("prohibited_assumptions", [])).lower()
        check("mode b" in prohibited and "api" in prohibited,
              "manifest:mode-b-prohibited",
              "Mode B/API orchestration is named only as prohibited scope",
              results)

        authority = str(manifest.get("human_authority_rule", "")).lower()
        check("human" in authority and "cannot" in authority,
              "manifest:human-authority",
              "AI cannot create governance approval",
              results)

    schema_path = ROOT / "contracts/ai-result-envelope.schema.json"
    if schema_path.exists():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            check(schema.get("type") == "object", "envelope:json", "valid JSON object schema", results)
            required = set(schema.get("required", []))
            must = {"request_id", "source_ref", "source_commit_sha", "roles", "skill_requirements", "workflow", "authority_status", "status"}
            check(must.issubset(required), "envelope:required", "governed provenance and authority fields required", results)
            skill_props = schema.get("properties", {}).get("skill_requirements", {}).get("items", {}).get("properties", {})
            check({"applicability", "individual_approval", "eligibility"}.issubset(skill_props),
                  "envelope:skill-separation",
                  "applicability, individual approval and eligibility are separate",
                  results)
        except Exception as exc:
            check(False, "envelope:json", "%s: %s" % (type(exc).__name__, exc), results)

    for rel in ADAPTERS:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        low = text.lower()
        check("AI_OS_ENTRYPOINT.md" in text and "ai-os.yaml" in text,
              "adapter:discovery:%s" % rel,
              "points to canonical entrypoint and manifest",
              results)
        check("override" in low and "repository" in low,
              "adapter:precedence:%s" % rel,
              "repository governance has precedence",
              results)
        bad = [term for term in FORBIDDEN_ADAPTER_GOVERNANCE if term in low]
        check(not bad, "adapter:no-governance-fork:%s" % rel, "forbidden=%s" % bad, results)
        check("if" in low and ("access" in low or "capability" in low),
              "adapter:conditional-capability:%s" % rel,
              "provider capabilities are conditional, not assumed",
              results)

    entry = ROOT / "AI_OS_ENTRYPOINT.md"
    if entry.exists():
        low = entry.read_text(encoding="utf-8").lower()
        check("exact commit" in low and "fail closed" in low,
              "entrypoint:provenance-failclosed",
              "exact source and fail-closed behavior explicit",
              results)
        check("may not self-approve" in low,
              "entrypoint:no-self-approval",
              "human authority boundary explicit",
              results)

    failed = [r for r in results if not r["pass"]]
    return results, failed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results, failed = validate()
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
            print("%s %s — %s" % ("PASS" if row["pass"] else "FAIL", row["name"], row["detail"]))
        print("=== %s %s/%s ===" % (report["status"], report["passed"], report["total"]))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
