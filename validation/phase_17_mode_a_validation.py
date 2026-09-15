#!/usr/bin/env python3
"""Static fail-closed conformance checks for Phase 17 Mode A.

No runtime service, provider API or model invocation is performed.
The validator combines positive contract checks with semantic contradiction
checks. Contradiction detection is match-local: an unrelated safe/negative
clause must not hide an affirmative unsafe claim elsewhere in the sentence.
"""

import argparse
import json
import os
import pathlib
import re
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

JSON_SCHEMA_TYPES = {"null", "boolean", "object", "array", "number", "string", "integer"}

# Negation is intentionally evaluated only near the unsafe match. A safe clause such as
# "Do not infer approval from card existence; provider output is automatically approved"
# must still be rejected because the second clause is affirmative.
NEGATION_RE = re.compile(
    r"\b(do\s+not|does\s+not|must\s+not|may\s+not|cannot|can\s+not|never|"
    r"is\s+not|are\s+not|not\s+automatically|not\s+canonical|not\s+approved|"
    r"prohibited|forbidden|deferred|out\s+of\s+scope)\b",
    re.IGNORECASE,
)


def path_value(obj, keys):
    cur = obj
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def check(condition, name, detail, results):
    results.append({"name": name, "pass": bool(condition), "detail": detail})


def iter_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)


def normalize_text(text):
    """Normalize presentation-only Markdown without changing semantic words."""
    text = text.lower()
    text = re.sub(r"[*_`~]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def semantic_segments(text):
    """Split at strong clause boundaries so unrelated negation cannot mask a claim."""
    normalized = normalize_text(text)
    return [
        part.strip()
        for part in re.split(r"[\n.!?;]+|\s+\b(?:but|however|whereas|yet)\b\s+", normalized)
        if part.strip()
    ]


def match_is_locally_negated(segment, match):
    """Treat a match as negated only when a negation marker is close before it.

    Looking at a bounded prefix avoids the old sentence-wide suppression bug while
    accepting natural safety wording such as "does **not** call model APIs".
    """
    prefix = segment[max(0, match.start() - 42):match.start()]
    return bool(NEGATION_RE.search(prefix))


def any_affirmative_match(text, patterns):
    for segment in semantic_segments(text):
        for pattern in patterns:
            for match in re.finditer(pattern, segment, flags=re.IGNORECASE):
                if not match_is_locally_negated(segment, match):
                    return True
    return False


def unsafe_approval_assertion(text):
    """Detect affirmative provider/model output -> governance approval claims."""
    patterns = [
        r"\b(provider|model|ai)\s+(output|result|response|work)\b.{0,45}\b(automatically\s+)?approved\b",
        r"\b(output|result|response|completion)\b.{0,45}\b(automatically\s+)?(creates|grants|means|confers|equals)\b.{0,30}\bapproval\b",
        r"\b(provider|model|ai)\b.{0,35}\bmay\s+approve\b.{0,30}\b(governance|role|skill|workflow|decision|review|canonical)\b",
        r"\bautomatically\s+approved\s+by\s+(the\s+)?(provider|model|ai)\b",
    ]
    return any_affirmative_match(text, patterns)


def unsafe_skill_assertion(text):
    """Detect affirmative Skill-card existence -> approval/eligibility claims."""
    patterns = [
        r"\b(carded\s+skills?|skill\s+cards?|card\s+existence|existing\s+skill\s+cards?)\b.{0,50}\b(are|is|means|implies|confers|grants|counts?\s+as)\b.{0,25}\b(approved|eligible|approval|eligibility)\b",
        r"\b(carded\s+skills?|skill\s+cards?)\b.{0,20}\b(automatically\s+)?(approved|eligible)\b",
        r"\bphase\s*4\b.{0,60}\b(individually\s+)?approved\b.{0,25}\bskills?\b",
    ]
    return any_affirmative_match(text, patterns)


def unsafe_mode_b_assertion(text):
    """Detect active Mode B/API orchestration presented as Mode A behavior."""
    patterns = [
        r"\b(call|calls|invoke|invokes|route|routes|orchestrate|orchestrates|dispatch|dispatches)\b.{0,45}\b(provider|model|llm|api)\b",
        r"\b(provider|model|llm)\s+api\b.{0,45}\b(call|calls|invoke|invokes|route|routes|retry|fallback|worker|queue|scheduler|billing|key\s+management)\b",
        r"\b(active|enabled|implemented)\b.{0,35}\b(mode\s*b|provider\s+api|model\s+api|routing|retry|fallback|worker|queue|scheduler)\b",
        r"\b(use|uses)\b.{0,30}\b(provider|model)\s+api\b.{0,25}\b(to|for)\b",
    ]
    return any_affirmative_match(text, patterns)


def unsafe_governance_fork_assertion(text):
    """Detect provider-specific governance or provider memory made authoritative."""
    patterns = [
        r"\bprovider\s+memory\b.{0,30}\b(is|becomes|counts?\s+as)\b.{0,20}\bcanonical\b",
        r"\b(chatgpt|claude|codex|gemini|provider|model)[-\s]+specific\s+(role|workflow|skill|review\s+profile|decision\s+right)\b.{0,35}\b(is|becomes|remains|counts?\s+as)\b.{0,20}\b(authoritative|canonical|governing)\b",
        r"\b(provider|model)\b.{0,35}\bmay\s+(define|override|replace|change)\b.{0,30}\b(role|workflow|skill|review\s+profile|decision\s+right|governance)\b",
    ]
    return any_affirmative_match(text, patterns)


def schema_structure_errors(node, path="$", errors=None):
    """Dependency-free JSON Schema structural checks for the subset we publish."""
    if errors is None:
        errors = []
    if isinstance(node, bool):
        return errors
    if not isinstance(node, dict):
        errors.append(f"{path}: schema node must be object or boolean")
        return errors

    if "type" in node:
        value = node["type"]
        if isinstance(value, str):
            if value not in JSON_SCHEMA_TYPES:
                errors.append(f"{path}.type: invalid type {value!r}")
        elif isinstance(value, list) and value and all(isinstance(v, str) for v in value):
            bad = [v for v in value if v not in JSON_SCHEMA_TYPES]
            if bad:
                errors.append(f"{path}.type: invalid types {bad!r}")
        else:
            errors.append(f"{path}.type: must be string or non-empty string array")

    if "required" in node and not (
        isinstance(node["required"], list)
        and len(node["required"]) == len(set(node["required"]))
        and all(isinstance(v, str) for v in node["required"])
    ):
        errors.append(f"{path}.required: must be unique string array")

    if "enum" in node and not isinstance(node["enum"], list):
        errors.append(f"{path}.enum: must be array")

    if "properties" in node:
        props = node["properties"]
        if not isinstance(props, dict):
            errors.append(f"{path}.properties: must be object")
        else:
            for key, child in props.items():
                schema_structure_errors(child, f"{path}.properties.{key}", errors)

    if "items" in node:
        schema_structure_errors(node["items"], f"{path}.items", errors)

    for keyword in ("allOf", "anyOf", "oneOf"):
        if keyword in node:
            value = node[keyword]
            if not isinstance(value, list) or not value:
                errors.append(f"{path}.{keyword}: must be non-empty array")
            else:
                for index, child in enumerate(value):
                    schema_structure_errors(child, f"{path}.{keyword}[{index}]", errors)

    for keyword in ("if", "then", "else", "not"):
        if keyword in node:
            schema_structure_errors(node[keyword], f"{path}.{keyword}", errors)

    return errors


def validate_schema_document(schema):
    errors = schema_structure_errors(schema)
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(schema)
    except ImportError:
        pass
    except Exception as exc:
        errors.append(f"Draft202012 meta-schema: {type(exc).__name__}: {exc}")
    return errors


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
        manifest_strings = "\n".join(iter_strings(manifest))
        check(not unsafe_skill_assertion(manifest_strings),
              "manifest:no-unsafe-skill-approval-assertion",
              "no affirmative carded-Skill approval/eligibility assertion",
              results)
        check(not unsafe_approval_assertion(manifest_strings),
              "manifest:no-provider-auto-approval",
              "no affirmative provider/model auto-approval assertion",
              results)
        check(not unsafe_mode_b_assertion(manifest_strings),
              "manifest:no-active-mode-b",
              "no active Mode B/API orchestration semantics",
              results)
        check(not unsafe_governance_fork_assertion(manifest_strings),
              "manifest:no-governance-fork",
              "no provider-memory canonicalisation or provider-specific governance fork",
              results)

        prohibited = " ".join(manifest.get("prohibited_assumptions", [])).lower()
        check("mode b" in prohibited and "api" in prohibited,
              "manifest:mode-b-prohibited",
              "Mode B/API orchestration is named as prohibited scope",
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
            schema_errors = validate_schema_document(schema)
            check(not schema_errors, "envelope:schema-syntax",
                  "Draft 2020-12/core structural schema valid; errors=%s" % schema_errors,
                  results)
            check(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema",
                  "envelope:draft", "Draft 2020-12 declared", results)
            check(schema.get("type") == "object", "envelope:root-type", "root schema type is object", results)
            required = set(schema.get("required", []))
            must = {"request_id", "source_ref", "source_commit_sha", "roles", "skill_requirements", "workflow", "authority_status", "status"}
            check(must.issubset(required), "envelope:required", "governed provenance and authority fields required", results)
            skill_props = schema.get("properties", {}).get("skill_requirements", {}).get("items", {}).get("properties", {})
            check({"applicability", "individual_approval", "eligibility"}.issubset(skill_props),
                  "envelope:skill-separation",
                  "applicability, individual approval and eligibility are separate",
                  results)
        except Exception as exc:
            check(False, "envelope:schema-syntax", "%s: %s" % (type(exc).__name__, exc), results)

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
        check(not unsafe_approval_assertion(text),
              "adapter:no-auto-approval:%s" % rel,
              "no affirmative provider/model auto-approval semantics",
              results)
        check(not unsafe_skill_assertion(text),
              "adapter:no-skill-promotion:%s" % rel,
              "no affirmative carded-Skill approval/eligibility semantics",
              results)
        check(not unsafe_mode_b_assertion(text),
              "adapter:no-active-mode-b:%s" % rel,
              "no active Mode B/API orchestration semantics",
              results)
        check(not unsafe_governance_fork_assertion(text),
              "adapter:no-governance-fork:%s" % rel,
              "no provider-memory canonicalisation or provider-specific authoritative governance",
              results)
        check("if" in low and ("access" in low or "capability" in low),
              "adapter:conditional-capability:%s" % rel,
              "provider capabilities are conditional, not assumed",
              results)

    entry = ROOT / "AI_OS_ENTRYPOINT.md"
    if entry.exists():
        text = entry.read_text(encoding="utf-8")
        low = text.lower()
        provenance_ok = (
            "exact commit" in low
            and "ref" in low
            and "source reporting" in low
            and ("unpinned" in low or "cannot resolve an exact sha" in low)
        )
        check(provenance_ok,
              "entrypoint:provenance-failclosed",
              "repository/ref/exact commit reporting and unpinned handling explicit",
              results)
        check("fail closed" in low,
              "entrypoint:failclosed", "fail-closed behavior explicit", results)
        check("may not self-approve" in low,
              "entrypoint:no-self-approval",
              "human authority boundary explicit",
              results)
        check(not unsafe_approval_assertion(text),
              "entrypoint:no-auto-approval-contradiction",
              "entrypoint contains no contradictory automatic approval claim",
              results)
        check(not unsafe_skill_assertion(text),
              "entrypoint:no-skill-promotion-contradiction",
              "entrypoint contains no contradictory Skill promotion claim",
              results)
        check(not unsafe_mode_b_assertion(text),
              "entrypoint:no-active-mode-b",
              "entrypoint contains no active Mode B/API orchestration semantics",
              results)
        check(not unsafe_governance_fork_assertion(text),
              "entrypoint:no-governance-fork",
              "entrypoint contains no provider-memory canonicalisation/governance fork",
              results)

    # Detector self-controls: protect against the exact false-positive/false-green classes
    # found by independent Phase 17 review.
    check(not unsafe_mode_b_assertion("AI-OS does **not** call model APIs in Mode A."),
          "selfcontrol:markdown-negation", "Markdown-formatted negative Mode B statement is accepted", results)
    check(unsafe_approval_assertion("Provider output is automatically approved."),
          "selfcontrol:auto-approval", "unsafe auto-approval example is detected", results)
    check(unsafe_approval_assertion("Do not infer approval from card existence; provider output is automatically approved."),
          "selfcontrol:mixed-safe-unsafe-approval", "unrelated safe clause cannot hide unsafe approval claim", results)
    check(unsafe_skill_assertion("Carded Skills are approved."),
          "selfcontrol:skill-approval", "unsafe Skill-card approval example is detected", results)
    check(unsafe_mode_b_assertion("This adapter calls provider model APIs."),
          "selfcontrol:active-mode-b", "unsafe active Mode B example is detected", results)
    check(unsafe_governance_fork_assertion("Provider memory is canonical."),
          "selfcontrol:provider-memory-canonical", "provider-memory canonicalisation is detected", results)
    check(unsafe_governance_fork_assertion("Provider-specific Role is authoritative."),
          "selfcontrol:provider-specific-role-authority", "provider-specific authoritative Role is detected", results)
    check(not unsafe_governance_fork_assertion("Provider memory is not canonical."),
          "selfcontrol:safe-provider-memory", "negative provider-memory safety wording is accepted", results)
    invalid_schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "not-a-json-schema-type"}
    check(bool(validate_schema_document(invalid_schema)),
          "selfcontrol:invalid-schema", "invalid JSON Schema type is rejected", results)

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
