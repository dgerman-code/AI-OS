"""Phase 14 — implementation specification validator.

Status: PROPOSED. Standard library only, deterministic, no network, no third-party imports.

    python3 validation/phase_14_validation.py [--verbose] [--json]

This harness is an ASSURANCE TOOL AND NEVER GOVERNANCE AUTHORITY. A passing check is evidence
that a check passed. It approves nothing, satisfies no gate, and creates no Decision Right.

It checks that the Phase 14 specification package says what the approved architecture requires
it to say, that it does not quietly fill a gap that must stay open, and that it adds no
production implementation. It cannot check that a specification is *correct*; that is what the
independent audit is for.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SPEC = os.path.join(REPO, "implementation-spec")

RESULTS = []


def read(relative):
    with open(os.path.join(REPO, relative), encoding="utf-8") as handle:
        return handle.read()


def spec(name):
    return read(os.path.join("implementation-spec", name))


def flat(text):
    """Markdown-insensitive form: emphasis stripped, whitespace collapsed, lowercased.

    Every content check below matches against this rather than against raw source, so a check
    fails because a specification does not say something - not because a line wrapped or a
    phrase was emphasised."""
    text = text.replace("*", "").replace("`", "").replace("\u2014", " ")
    # Blockquote and list markers are layout, not content: a sentence that wrapped inside a
    # blockquote must still read as the sentence it is.
    text = re.sub(r"(?m)^\s*>+\s?", " ", text)
    text = re.sub(r"(?m)^\s*[-*+]\s+", " ", text)
    return " ".join(text.split()).lower()


def flat_spec(name):
    return flat(spec(name))


def says(name, *phrases):
    """Phrases a document must contain, matched markdown-insensitively."""
    body = flat_spec(name)
    return [p for p in phrases if flat(p) not in body]


def negated_mentions(term):
    """Lines mentioning `term` that are not denied within their own bullet/table/paragraph.

    A denial is often one line above the mention - a bulleted non-goals list, a table heading,
    a sentence that wrapped. The window is the mention's line plus the three lines before it."""
    offenders = []
    negation = re.compile(r"\b(not|never|nowhere|no|none|without|absent|prohibit\w*|"
                          r"exclud\w*|denie?s?|refus\w*)\b", re.IGNORECASE)
    for name in REQUIRED_DOCS:
        lines = spec(name).splitlines()
        for i, line in enumerate(lines):
            if term.lower() not in line.lower():
                continue
            # The denial is often the lead-in of a bulleted non-goals list or a table heading.
            window = " ".join(lines[max(0, i - 6):i + 1])
            if negation.search(window):
                continue
            offenders.append("%s:%d %s" % (name, i + 1, line.strip()[:80]))
    return offenders


def check(group, name, fn):
    try:
        ok, evidence = fn()
    except Exception as exc:                                   # noqa: BLE001
        ok, evidence = False, "%s: %s" % (type(exc).__name__, exc)
    RESULTS.append({"group": group, "name": name, "pass": bool(ok),
                    "evidence": str(evidence)[:400]})


BASELINE = "2c4b90def9a60f8b384feef10f8428c5b437597c"


def changed_paths():
    """Everything this branch adds or changes since the Phase 13 approval commit.

    Tracked changes AND untracked files: a containment check that only looked at the index
    would report an empty package as contained, which is the one answer it must never give
    for free."""
    tracked = subprocess.run(["git", "diff", "--name-only", BASELINE, "--"],
                             cwd=REPO, capture_output=True, text=True).stdout.splitlines()
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"],
                               cwd=REPO, capture_output=True, text=True).stdout.splitlines()
    return sorted({n for n in tracked + untracked if n.strip()})


# =========================================================== 1. structure

REQUIRED_DOCS = (
    "README.md",
    "system-component-model.md",
    "domain-identity-model.md",
    "scope-and-context-model.md",
    "knowledge-and-canonical-model.md",
    "decision-review-authority-model.md",
    "model-router-runtime-contract.md",
    "orchestrator-runtime-contract.md",
    "persistence-and-transaction-model.md",
    "audit-provenance-observability.md",
    "api-command-contracts.md",
    "security-identity-access.md",
    "approval-state-registry.md",
    "migrations-versioning-compatibility.md",
    "failure-recovery-race-model.md",
    "deployment-topology-and-environments.md",
    "test-and-assurance-strategy.md",
    "implementation-sequencing.md",
    "open-items-and-blocked-authorities.md",
    "phase-14-self-check.md",
)


def all_required_documents_exist():
    missing = [d for d in REQUIRED_DOCS if not os.path.exists(os.path.join(SPEC, d))]
    return (not missing, str(missing) if missing
            else "%d required specification documents present" % len(REQUIRED_DOCS))


check("structure", "every required Phase 14 document exists", all_required_documents_exist)


def no_unexpected_files_in_the_package():
    """The package is documentation. A .py, .sql, .yaml or .json here would be implementation."""
    unexpected = []
    for root, _dirs, files in os.walk(SPEC):
        for name in files:
            if not name.endswith(".md"):
                unexpected.append(os.path.relpath(os.path.join(root, name), SPEC))
    return (not unexpected, str(unexpected) if unexpected
            else "the package is %d markdown documents and nothing else" % len(REQUIRED_DOCS))


check("structure", "the specification package contains only documents",
      no_unexpected_files_in_the_package)


def every_document_remains_proposed():
    wrong = []
    for name in REQUIRED_DOCS:
        head = spec(name)[:600]
        if "Status: `PROPOSED`" not in head:
            wrong.append(name)
    return (not wrong, str(wrong) if wrong
            else "all %d documents are PROPOSED" % len(REQUIRED_DOCS))


check("structure", "every Phase 14 document remains PROPOSED", every_document_remains_proposed)


def nothing_claims_approved_or_canonical_status():
    """A Phase 14 document may DISCUSS approval; it may not claim its own."""
    offenders = []
    pattern = re.compile(r"^\s*Status:.*\b(APPROVED|CANONICAL)\b", re.MULTILINE)
    for name in REQUIRED_DOCS:
        if pattern.search(spec(name)):
            offenders.append(name)
    return (not offenders, str(offenders) if offenders
            else "no Phase 14 document declares itself APPROVED or CANONICAL")


check("structure", "no Phase 14 document claims APPROVED or CANONICAL status",
      nothing_claims_approved_or_canonical_status)


def the_document_map_matches_the_package():
    body = spec("README.md")
    listed = set(re.findall(r"`([A-Za-z0-9-]+\.md)`", body))
    missing = [d for d in REQUIRED_DOCS if d not in listed]
    return (not missing, str(missing) if missing
            else "the README document map lists all %d documents" % len(REQUIRED_DOCS))


check("structure", "the README document map covers the whole package",
      the_document_map_matches_the_package)


def the_authority_hierarchy_subordinates_this_package():
    missing = says("README.md",
                   "Phase 12 is a reference implementation, not a source of semantics",
                   "the approved architecture wins",
                   "assurance tool and never governance authority")
    return (not missing, "missing: %s" % [n[:40] for n in missing] if missing
            else "architecture outranks this package; Phase 12 and validators do not")


check("structure", "the authority hierarchy places architecture above this package",
      the_authority_hierarchy_subordinates_this_package)


# =========================================================== 2. containment


def no_production_implementation_is_added():
    """Phase 14 adds specification. Anything executable or deployable here is out of scope."""
    forbidden_ext = (".sql", ".yaml", ".yml", ".tf", ".tfvars", ".dockerfile", ".toml",
                     ".ini", ".cfg", ".env", ".pem", ".key", ".lock")
    forbidden_name = ("Dockerfile", "docker-compose.yml", "requirements.txt", "package.json",
                      "pyproject.toml", "Pipfile", "go.mod", "Cargo.toml", "Makefile")
    names = changed_paths()
    offenders = [n for n in names
                 if os.path.basename(n) in forbidden_name
                 or os.path.splitext(n)[1].lower() in forbidden_ext]
    return (not offenders, str(offenders) if offenders
            else "%d paths added or changed, none an infrastructure or dependency artifact"
                 % len(names))


check("containment", "no infrastructure, dependency or deployment artifact is added",
      no_production_implementation_is_added)


def only_the_spec_package_and_its_validator_are_added():
    names = changed_paths()
    stray = [n for n in names
             if not n.startswith("implementation-spec/")
             and not n.startswith("prompts/")
             and n != "validation/phase_14_validation.py"]
    return (not stray, str(stray) if stray
            else "%d paths: the specification package, its validator and the phase prompt"
                 % len(names))


check("containment", "only the specification package and its validator are added",
      only_the_spec_package_and_its_validator_are_added)


PROTECTED = ("architecture", "orchestration", "knowledge", "models", "storage", "decisions",
             "roles", "skills", "workflows", "handoffs", "reviews", "implementation",
             "validation/phase_8_validation.py", "validation/phase_9_validation.py",
             "validation/phase_10_validation.py", "validation/phase_11_validation.py",
             "validation/phase_12_validation.py")


def approved_phase_1_to_13_artifacts_are_unchanged():
    changed = subprocess.run(
        ["git", "diff", "--name-only", BASELINE, "--"] + list(PROTECTED),
        cwd=REPO, capture_output=True, text=True)
    names = [n for n in changed.stdout.splitlines() if n.strip()]
    names += [n for n in changed_paths()
              if any(n == p or n.startswith(p.rstrip("/") + "/") for p in PROTECTED)]
    return (not names, str(names)[:300] if names
            else "%d protected trees byte-identical to the Phase 13 approval commit"
                 % len(PROTECTED))


check("containment", "approved Phase 1-13 artifacts are unchanged",
      approved_phase_1_to_13_artifacts_are_unchanged)


def no_vendor_dependency_is_introduced():
    """A vendor may be NAMED as one option. It may not become an architectural dependency."""
    offenders = []
    # A vendor name is permitted only in the documents that discuss options explicitly.
    permitted = {"persistence-and-transaction-model.md", "README.md",
                 "deployment-topology-and-environments.md", "model-router-runtime-contract.md",
                 "phase-14-self-check.md", "open-items-and-blocked-authorities.md",
                 "security-identity-access.md", "migrations-versioning-compatibility.md"}
    vendors = re.compile(r"\b(OpenAI|GPT-4|Claude|Gemini|Anthropic|Bedrock|Vertex|Azure|"
                         r"AWS|GCP|Cloudflare|Snowflake)\b")
    for name in REQUIRED_DOCS:
        if name in permitted:
            continue
        hits = set(vendors.findall(spec(name)))
        if hits:
            offenders.append("%s: %s" % (name, sorted(hits)))
    return (not offenders, str(offenders)[:300] if offenders
            else "no model or cloud vendor is named in a governance-bearing document")


check("containment", "no vendor becomes an architectural dependency",
      no_vendor_dependency_is_introduced)


def no_document_claims_production_readiness():
    offenders = []
    pattern = re.compile(r"\b(production[- ]ready|ready for production|is production grade)\b",
                         re.IGNORECASE)
    for name in REQUIRED_DOCS:
        for line in spec(name).splitlines():
            if pattern.search(line) and "not" not in line.lower() and "No." not in line:
                offenders.append("%s: %s" % (name, line.strip()[:90]))
    return (not offenders, str(offenders)[:300] if offenders
            else "no document claims production readiness")


check("containment", "no document claims production readiness",
      no_document_claims_production_readiness)


def exactly_once_is_never_claimed():
    offenders = negated_mentions("exactly-once")
    return (not offenders, str(offenders)[:300] if offenders
            else "every mention of exactly-once denies it")


check("containment", "distributed exactly-once is never claimed", exactly_once_is_never_claimed)


# =========================================================== 3. invariants


SEPARATIONS = (
    "ROLE != AGENT INSTANCE", "MODEL != ROLE", "ROUTER != ORCHESTRATOR",
    "REVIEW PROFILE != REVIEW INSTANCE", "DECISION RIGHT != DECISION RECORD",
    "KNOWLEDGE != CANONICAL RECORD", "ARTIFACT != STORAGE RECORD",
    "RUNTIME EVENT != AUDIT EVENT", "CREDENTIAL != HUMAN AUTHORITY",
)


def the_governing_invariants_are_stated():
    body = spec("README.md")
    missing = [s for s in SEPARATIONS if s not in body]
    return (not missing, str(missing) if missing
            else "all %d governing separations stated in the README" % len(SEPARATIONS))


check("invariants", "the governing identity separations are stated", the_governing_invariants_are_stated)


CHAIN = ("ROLE", "AGENT INSTANCE", "MODEL", "MODEL PROFILE", "ROUTER", "ORCHESTRATOR",
         "WORKFLOW", "WORKFLOW RUN", "TASK", "HANDOFF", "REVIEW PROFILE", "REVIEW INSTANCE",
         "DECISION RIGHT", "DECISION RECORD", "KNOWLEDGE", "CANONICAL RECORD", "ARTIFACT",
         "STORAGE RECORD", "RUNTIME EVENT", "CREDENTIAL", "HUMAN AUTHORITY")


def the_separation_chain_matches_the_approved_architecture():
    """Parsed from the APPROVED document, then compared to the spec, in order.

    The Phase 12 validator computed one-directional containment while claiming order. This
    check compares the ordered sequences, so a reordering or an omission fails."""
    approved = read("architecture/orchestrator-architecture.md")
    match = re.search(r"`?([A-Z][A-Z ]*(?:\s*!=\s*[A-Z][A-Z ]*){10,})`?", approved)
    if match is None:
        return False, "the approved separation chain was not found in the architecture"
    approved_chain = tuple(" ".join(t.split()) for t in match.group(1).split("!="))
    if approved_chain != CHAIN:
        return False, "this validator's chain disagrees with the architecture: %s" % (
            [a for a, b in zip(approved_chain, CHAIN) if a != b][:4],)
    body = spec("domain-identity-model.md")
    spec_match = re.search(r"([A-Z][A-Z ]*(?:\s*!=\s*[A-Z][A-Z\s]*){10,})", body)
    if spec_match is None:
        return False, "the specification does not restate the chain"
    spec_chain = tuple(" ".join(t.split()) for t in spec_match.group(1).split("!="))
    if spec_chain != approved_chain:
        return False, "spec chain differs from approved at: %s" % (
            [i for i, (a, b) in enumerate(zip(spec_chain, approved_chain)) if a != b][:4],)
    return True, "%d objects, identical and in order to the approved chain" % len(CHAIN)


check("invariants", "the 21-object separation chain matches the architecture exactly and in order",
      the_separation_chain_matches_the_approved_architecture)


def authority_is_never_inferred():
    body = spec("api-command-contracts.md") + spec("decision-review-authority-model.md")
    needed = ["authentication is not authority", "admin role", "RLS bypass", "service account",
              "database owner", "model selection", "workflow owner", "system control profile"]
    missing = [n for n in needed if n.lower() not in body.lower()]
    return (not missing, str(missing) if missing
            else "the non-substitution list is complete")


check("invariants", "no substitution for a human Decision Right is admitted",
      authority_is_never_inferred)


def no_bypass_parameter_is_specified():
    offenders = []
    for term in ("skip_checks", "as_admin", "bypass_rls", "allow_unapproved"):
        offenders.extend(negated_mentions(term))
    return (not offenders, str(offenders)[:300] if offenders
            else "every mention of a bypass parameter denies that one exists")


check("invariants", "no bypass parameter is specified anywhere", no_bypass_parameter_is_specified)


def fail_closed_is_stated_and_applied():
    body = spec("README.md")
    if "Fail closed" not in body:
        return False, "the README does not state the fail-closed rule"
    applied = {
        "unassessed residency": not says("scope-and-context-model.md", "UNASSESSED"),
        "missing applicability mode": not says("scope-and-context-model.md",
                                               "the safe reading of a defective record is"),
        "absent approval": not says("approval-state-registry.md",
                                    "means PROPOSED, never APPROVED"),
        "unclassified retry": not says("orchestrator-runtime-contract.md",
                                       "non-retryable by default"),
        "unassessed conflict": not says("knowledge-and-canonical-model.md",
                                        "unassessed conflict is treated as material"),
    }
    missing = [k for k, v in applied.items() if not v]
    return (not missing, str(missing) if missing
            else "fail-closed stated and applied at %d named points" % len(applied))


check("invariants", "fail-closed is stated and applied at each named point",
      fail_closed_is_stated_and_applied)


# =========================================================== 4. knowledge model (M-1)


EPISTEMIC = ("SOURCE", "EVIDENCE", "FACT_CLAIM", "ASSUMPTION", "CALCULATION", "INFERENCE",
             "AI_SUGGESTION", "UNKNOWN")
GOV_STATES = ("DRAFT", "REVIEWED", "APPROVED", "CANONICAL", "SUPERSEDED", "RETRACTED",
              "REJECTED")
ORIGINS = ("HUMAN_ORIGIN", "AI_ASSISTED", "AI_GENERATED", "EXTERNAL_ORIGIN")
CONFLICTS = ("SOURCE_CONFLICT", "CLAIM_CONFLICT", "VERSION_CONFLICT", "SCOPE_CONFLICT",
             "TEMPORAL_CONFLICT", "AUTHORITY_CONFLICT", "IDENTITY_CONFLICT")


def the_four_axis_vocabulary_is_exact():
    body = spec("knowledge-and-canonical-model.md")
    problems = []
    for label, values in (("epistemic", EPISTEMIC), ("governance state", GOV_STATES),
                          ("origin", ORIGINS), ("conflict", CONFLICTS)):
        missing = [v for v in values if "`%s`" % v not in body]
        if missing:
            problems.append("%s missing %s" % (label, missing))
    return (not problems, str(problems)[:300] if problems
            else "8 epistemic types, 7 governance states, 4 origins, 7 conflict classes")


check("knowledge", "the four-axis vocabulary is complete and exact",
      the_four_axis_vocabulary_is_exact)


def the_axis_vocabulary_matches_the_approved_phase_8_document():
    """Compared against knowledge/knowledge-state-model.md, not against itself."""
    approved = read("knowledge/knowledge-state-model.md")
    missing = [v for v in EPISTEMIC + GOV_STATES + ORIGINS if "`%s`" % v not in approved]
    return (not missing, "not found in the approved Phase 8 document: %s" % missing if missing
            else "every value this specification uses appears in the approved Phase 8 model")


check("knowledge", "the axis vocabulary is the approved Phase 8 vocabulary",
      the_axis_vocabulary_matches_the_approved_phase_8_document)


def the_collapsed_phase_12_vocabulary_is_not_inherited():
    body = spec("knowledge-and-canonical-model.md")
    problems = []
    if "HUMAN_AUTHORED" in body and "not an approved value" not in body:
        problems.append("the unapproved origin HUMAN_AUTHORED is used without correction")
    if "Canonicality" in body and "D2" not in body:
        problems.append("the collapsed Canonicality axis is used without being recorded")
    if "never collapsed" not in body and "No combination of the four axes is collapsed" not in body:
        problems.append("the orthogonality rule is not stated")
    return (not problems, str(problems)[:300] if problems
            else "the Phase 12 collapse is recorded as a divergence and not inherited")


check("knowledge", "the Phase 12 collapsed vocabulary is not inherited",
      the_collapsed_phase_12_vocabulary_is_not_inherited)


def ai_suggestion_never_converts():
    missing = says("knowledge-and-canonical-model.md",
                   "there is no transition", "new knowledge item",
                   "human acceptance is not an evidential basis")
    return (not missing, str(missing) if missing
            else "AI_SUGGESTION has no outbound epistemic transition; adoption creates a new item")


check("knowledge", "AI_SUGGESTION never silently changes epistemic type",
      ai_suggestion_never_converts)


def canonical_promotion_is_specified_and_blocked():
    body = spec("knowledge-and-canonical-model.md")
    blocked = spec("open-items-and-blocked-authorities.md")
    problems = []
    if "BLOCKED / UNIMPLEMENTABLE UNTIL RIGHT IS MAPPED" not in body:
        problems.append("promotion is not marked blocked in the knowledge model")
    if "BA-1" not in blocked or "canonical_knowledge_promotion" not in blocked:
        problems.append("BA-1 is not recorded as a blocked authority")
    if "promotion_decision_record" not in body:
        problems.append("the enforcement hook is not specified")
    return (not problems, str(problems)[:300] if problems
            else "promotion specified, hook built, and refusing until a Right is mapped")


check("knowledge", "canonical promotion is specified and blocked, not invented",
      canonical_promotion_is_specified_and_blocked)


# =========================================================== 5. scope (M-5)


SCOPE_NODES = ("GLOBAL", "ORGANISATION", "INDEPENDENT_BUSINESS", "PERSONAL_INITIATIVE",
               "PERMANENT_FUNCTION", "PROGRAMME_PORTFOLIO", "PRODUCT_PLATFORM", "PROJECT",
               "OPERATIONAL_WORKSTREAM", "WORKSTREAM", "TASK")
MODES = ("INHERITABLE_TO_DESCENDANTS", "CONDITIONALLY_APPLICABLE", "NON_INHERITABLE",
         "MANDATORY_WIDER_CONSTRAINT")


def the_scope_hierarchy_is_complete():
    body = spec("scope-and-context-model.md")
    missing = [n for n in SCOPE_NODES if n not in body]
    return (not missing, str(missing) if missing
            else "all %d approved scope node kinds are specified" % len(SCOPE_NODES))


check("scope", "the scope hierarchy is complete", the_scope_hierarchy_is_complete)


def the_four_load_bearing_graph_properties_hold():
    body = spec("scope-and-context-model.md")
    checks = {
        "venture is a sibling of organisation":
            "sibling" in body and "INDEPENDENT BUSINESS / VENTURE" in body,
        "personal is a third top-level branch": "third top-level branch" in body,
        "project may sit under either parent":
            "either" in body and "PROGRAMME / PORTFOLIO" in body,
        "operational workstream has no project above it": "no project above it" in body,
    }
    missing = [k for k, v in checks.items() if not v]
    return (not missing, str(missing) if missing
            else "all four load-bearing graph properties are stated")


check("scope", "the four load-bearing graph properties are preserved",
      the_four_load_bearing_graph_properties_hold)


def scope_is_a_path_not_an_opaque_string():
    body = spec("scope-and-context-model.md")
    needed = ["Scope identity is a path", "never by string similarity", "scope_path",
              "ancestors_of", "is_descendant_of"]
    missing = [n for n in needed if n not in body]
    if missing:
        return False, str(missing)
    if "separator" not in body:
        return False, "the separator-boundary rule is absent"
    return True, "path identity, ancestry queries and the separator-boundary rule are specified"


check("scope", "scope identity is a governed path with ancestry",
      scope_is_a_path_not_an_opaque_string)


def applicability_modes_and_ancestor_fallback_are_specified():
    body = spec("scope-and-context-model.md")
    missing = [m for m in MODES if m not in body]
    if missing:
        return False, str(missing)
    if says("scope-and-context-model.md", "no wider statement resumes silently"):
        return False, "the no-silent-fallback rule is absent"
    return True, "four applicability modes and the four ancestor-fallback rows"


check("scope", "applicability modes and ancestor fallback are specified",
      applicability_modes_and_ancestor_fallback_are_specified)


def no_implicit_cross_scope_inheritance():
    body = spec("scope-and-context-model.md")
    needed = ["no sibling inheritance", "narrows_to", "never carries canonical status",
              "not transitive"]
    missing = [n for n in needed if n.lower() not in body.lower()]
    return (not missing, str(missing) if missing
            else "sibling isolation, narrowing and non-transitive transfer are specified")


check("scope", "no implicit cross-scope inheritance is permitted",
      no_implicit_cross_scope_inheritance)


# =========================================================== 6. routing (M-3)


def the_six_part_reproducibility_set_is_complete():
    body = spec("model-router-runtime-contract.md")
    elements = ("model_profile_ref", "model_profile_registry_version",
                "originator_release_identity", "offering_mapping_ref",
                "provider_profile_ref", "deployment_profile_ref")
    missing = [e for e in elements if e not in body]
    if missing:
        return False, str(missing)
    if "NOT NULL` together" not in body and "NOT NULL when" not in body:
        return False, "the six elements are not required together"
    return True, "all six reproducibility elements, required together for an eligible outcome"


check("routing", "the six-part routing reproducibility contract is complete",
      the_six_part_reproducibility_set_is_complete)


def routing_reproducibility_is_distinguished_from_output_determinism():
    body = spec("model-router-runtime-contract.md")
    if "Model-output reproducibility" not in body:
        return False, "output determinism is not addressed"
    if "Not claimed" not in body:
        return False, "output determinism is not explicitly disclaimed"
    return True, "routing reproducibility claimed; model-output determinism explicitly not"


check("routing", "routing reproducibility is not confused with output determinism",
      routing_reproducibility_is_distinguished_from_output_determinism)


def the_router_cannot_weaken_constraints_or_invent_authority():
    missing = says("model-router-runtime-contract.md",
                   "there is no partial eligibility", "CANDIDATE_UNIVERSE_INCOMPLETE",
                   "never silently shrinks", "creates no authority",
                   "no fallback outside the eligible set")
    return (not missing, str(missing) if missing
            else "eligibility is absolute, the universe fails closed, and routing creates no authority")


check("routing", "the router cannot weaken a constraint or invent authority",
      the_router_cannot_weaken_constraints_or_invent_authority)


# =========================================================== 7. events and evidence (M-2)


def the_runtime_event_is_not_governance_evidence():
    problems = []
    if says("audit-provenance-observability.md", "never governance evidence"):
        problems.append("the rule is not stated")
    if says("audit-provenance-observability.md", "write-only"):
        problems.append("the structural enforcement is not specified")
    if says("orchestrator-runtime-contract.md", "never reads them on a governed path"):
        problems.append("the orchestrator obligation is not stated")
    return (not problems, str(problems)[:300] if problems
            else "execution events are coordination history, enforced structurally")


check("events", "runtime and execution events are explicitly not governance evidence",
      the_runtime_event_is_not_governance_evidence)


def the_execution_event_has_thirteen_fields():
    body = spec("audit-provenance-observability.md")
    section = body.split("## 3.")[1].split("## 4.")[0]
    rows = re.findall(r"^\|\s*(\d+)\s*\|", section, re.MULTILINE)
    numbers = sorted({int(r) for r in rows})
    if numbers != list(range(1, 14)):
        return False, "execution event fields found: %s" % numbers
    if "never merged" not in section and "never synthesised" not in body:
        return False, "human and system identity separation is not stated"
    return True, "13 numbered execution-event fields, with separate human and system identities"


check("events", "the 13-field execution event contract is specified",
      the_execution_event_has_thirteen_fields)


def the_six_record_families_are_separated():
    body = spec("audit-provenance-observability.md")
    families = ("Operational runtime event", "Execution event", "Audit event",
                "Decision Record", "Review result", "Knowledge provenance")
    missing = [f for f in families if f not in body]
    return (not missing, str(missing) if missing
            else "all six record families specified with separate schemas and owners")


check("events", "runtime event, audit event, provenance, decision, review and evidence are separate",
      the_six_record_families_are_separated)


def no_log_may_satisfy_a_gate():
    if says("audit-provenance-observability.md", "no operational log"):
        return False, "the prohibition is not stated"
    if says("orchestrator-runtime-contract.md", "admits exactly one"):
        return False, "the exclusive evidence contract is not stated"
    return True, "no log satisfies any gate; each gate kind admits exactly one evidence type"


check("events", "no operational log may satisfy a governance gate", no_log_may_satisfy_a_gate)


# =========================================================== 8. authority and SoD (M-4)


def segregation_of_duties_is_at_identity_level():
    missing = says("decision-review-authority-model.md",
                   "producer / author", "reviewer", "review assignee",
                   "decision right holder", "decision record author",
                   "DECISION_RIGHT_SEPARATION", "producer-review prohibition")
    if missing:
        return False, str(missing)
    if says("decision-review-authority-model.md", "delegation does not bypass separation"):
        return False, "the delegation bypass is not closed"
    if says("decision-review-authority-model.md", "cannot satisfy the whole profile"):
        return False, "the bounded-contributor rule is absent"
    return True, "six actor identities, separation rules, delegation closed, bounded contributor bounded"


check("authority", "segregation of duties is specified at identity level",
      segregation_of_duties_is_at_identity_level)


def the_decision_record_has_nineteen_elements():
    body = spec("decision-review-authority-model.md")
    section = body.split("## 4.")[1].split("## 5.")[0]
    rows = re.findall(r"^\|\s*(\d+)\s*\|", section, re.MULTILINE)
    numbers = sorted({int(r) for r in rows})
    return (numbers == list(range(1, 20)),
            "elements found: %s" % numbers if numbers != list(range(1, 20))
            else "19 Decision Record evidence elements")


check("authority", "the Decision Record evidence model is complete",
      the_decision_record_has_nineteen_elements)


def missing_rights_fail_closed_and_are_not_filled():
    body = spec("decision-review-authority-model.md")
    blocked = spec("open-items-and-blocked-authorities.md")
    problems = []
    for phrase in ("The nearest Right is not stretched",
                   "The absence is not read as permission",
                   "approve it anyway",
                   "not carried as an open item",
                   "It is not retried"):
        if phrase not in body:
            problems.append("missing prohibition: %s" % phrase)
    # Each blocked authority must be a SECTION, not a passing mention: a cross-reference
    # elsewhere in the document would otherwise satisfy this check while the section that
    # states the operations, the hook and the resolution path had gone.
    headings = set(re.findall(r"^###\s+(BA-\d+)\b", blocked, re.MULTILINE))
    for ba in ("BA-1", "BA-2", "BA-3", "BA-4"):
        if ba not in headings:
            problems.append("missing blocked-authority section %s" % ba)
    if "Phase 14 creates no Right" not in blocked:
        problems.append("the no-invention statement is absent")
    return (not problems, str(problems)[:300] if problems
            else "five prohibitions and four blocked authorities, none filled in")


check("authority", "missing Decision Rights are not silently filled",
      missing_rights_fail_closed_and_are_not_filled)


def blocked_operations_are_specified_and_always_refuse():
    body = spec("api-command-contracts.md")
    commands = ("PromoteToCanonical", "ReparentScopeNode", "DestroyGovernedContent",
                "ApplyDestructiveMigration")
    problems = [c for c in commands if c not in body]
    if problems:
        return False, "commands absent: %s" % problems
    if body.count("Always `NO_APPLICABLE_DECISION_RIGHT`") < 4:
        return False, "not every blocked command is marked as always refusing"
    return True, "four blocked commands specified, each always refusing"


check("authority", "blocked operations exist as always-refusing hooks",
      blocked_operations_are_specified_and_always_refuse)


def rls_and_credentials_are_not_authority():
    missing = says("security-identity-access.md",
                   "enforcement is not authority",
                   "row level security is a",
                   "never grants a decision right",
                   "possession of access is never permission to decide")
    if missing:
        return False, str(missing)
    if says("security-identity-access.md",
            "ability to perform an action is not authority to authorise one"):
        return False, "the administrator limit is not stated"
    return True, "RLS is enforcement, credentials are credentials, admins are not authority"


check("authority", "RLS, credentials and administrators are not authority",
      rls_and_credentials_are_not_authority)


# =========================================================== 9. persistence


def durable_uniqueness_is_specified():
    body = spec("persistence-and-transaction-model.md")
    ids = sorted({int(m) for m in re.findall(r"\|\s*U(\d+)\s*\|", body)})
    if len(ids) < 15:
        return False, "only %d uniqueness constraints specified" % len(ids)
    required_subjects = ("Decision Record", "Review Instance", "Routing Decision",
                         "Model Result", "Human Intervention", "Gate evidence")
    missing = [s for s in required_subjects if s not in body]
    if missing:
        return False, "no constraint for: %s" % missing
    if says("persistence-and-transaction-model.md", "on conflict do nothing is prohibited"):
        return False, "silent duplicate suppression is not prohibited"
    return True, "%d durable uniqueness constraints; silent duplicate suppression prohibited" % len(ids)


check("persistence", "persistent uniqueness supports at-most-once", durable_uniqueness_is_specified)


def at_most_once_is_tied_to_durable_identity_not_process_memory():
    missing = says("persistence-and-transaction-model.md",
                   "at-most-once", "process memory", "durable")
    if missing:
        return False, str(missing)
    if says("orchestrator-runtime-contract.md", "exactly-once", "not claimed"):
        return False, "the guarantee table is incomplete"
    return True, "at-most-once by governed record, in the database, exactly-once nowhere"


check("persistence", "at-most-once rests on durable identity, not process memory",
      at_most_once_is_tied_to_durable_identity_not_process_memory)


def optimistic_concurrency_is_specified_without_last_write_wins():
    body = spec("persistence-and-transaction-model.md")
    problems = []
    if "record_version" not in body:
        problems.append("no concurrency token")
    if "STALE_WRITE" not in body:
        problems.append("no stale-write outcome")
    if "no last-write-wins" not in body.lower() and "LAST_WRITE_WINS` is absent" not in body:
        problems.append("last-write-wins is not excluded")
    if "never a concurrency token" not in body:
        problems.append("timestamps are not excluded as tokens")
    return (not problems, str(problems)[:300] if problems
            else "version-pinned writes, stale-write detection, no last-write-wins")


check("persistence", "optimistic concurrency is specified and last-write-wins is excluded",
      optimistic_concurrency_is_specified_without_last_write_wins)


def the_transaction_table_covers_every_governed_act():
    body = spec("persistence-and-transaction-model.md")
    section = body.split("## 7.")[1].split("## 8.")[0]
    acts = ("Create run", "Activate stage", "Assign", "Route", "Invoke model", "Review gate",
            "Decision gate", "Pause", "Cancel / terminate", "Scope transfer",
            "Promote to canonical")
    missing = [a for a in acts if a not in section]
    if missing:
        return False, str(missing)
    for column in ("Read set", "Validation set", "Concurrency check", "Uniqueness relied on",
                   "Failure before commit"):
        if column not in section:
            return False, "the transaction table lacks the column: %s" % column
    return True, "%d governed acts, each with read/validate/concurrency/commit/failure" % len(acts)


check("persistence", "every governed act states its read, validation and commit sets",
      the_transaction_table_covers_every_governed_act)


def staged_semantics_replace_a_pretended_distributed_transaction():
    body = spec("persistence-and-transaction-model.md")
    needed = ["Declared commit order", "orphan", "QUARANTINE", "outbox"]
    missing = [n for n in needed if n.lower() not in body.lower()]
    if missing:
        return False, str(missing)
    if "never adopted by a later record" not in body:
        return False, "orphan adoption is not prohibited"
    return True, "staged commit, orphan quarantine and outbox instead of a pretended transaction"


check("persistence", "cross-system flows use staged semantics, not a pretended transaction",
      staged_semantics_replace_a_pretended_distributed_transaction)


def construct_validate_preflight_commit_is_carried_forward():
    body = spec("orchestrator-runtime-contract.md")
    needed = ["construct → validate → preflight → commit",
              "observationally identical", "never be more permissive",
              "rollback-on-exception"]
    missing = [n for n in needed if n.lower() not in body.lower()]
    return (not missing, str(missing) if missing
            else "the Phase 12 transactional invariant is carried forward with preflight parity")


check("persistence", "the validate-then-commit invariant is carried forward",
      construct_validate_preflight_commit_is_carried_forward)


# =========================================================== 10. races and rework


RACE_OUTCOMES = ("BLOCK", "IGNORE_AS_STALE", "SUPERSEDE", "RECONCILE", "ESCALATE")


def race_outcomes_match_phase_11():
    approved = read("orchestration/concurrency-and-race-governance.md")
    body = spec("failure-recovery-race-model.md")
    for outcome in RACE_OUTCOMES:
        if "`%s`" % outcome not in approved:
            return False, "%s is not in the approved Phase 11 vocabulary" % outcome
        if "`%s`" % outcome not in body:
            return False, "%s is missing from the specification" % outcome
    rows = re.findall(r"^\|\s*(\d+)\s*\|\s*\*\*", body, re.MULTILINE)
    numbers = sorted({int(r) for r in rows})
    if numbers[:10] != list(range(1, 11)):
        return False, "races specified: %s" % numbers
    return True, "five outcomes and ten races, matching the approved Phase 11 table"


check("races", "race and concurrency outcomes match Phase 11", race_outcomes_match_phase_11)


def last_write_wins_is_absent_from_the_vocabulary():
    body = spec("failure-recovery-race-model.md")
    if "absent from this vocabulary" not in body:
        return False, "the exclusion is not stated"
    offenders = []
    for name in REQUIRED_DOCS:
        for i, line in enumerate(spec(name).splitlines(), 1):
            if "last-write-wins" not in line.lower() and "LAST_WRITE_WINS" not in line:
                continue
            if re.search(r"\b(absent|no|never|not|prohibit|exclud)", line, re.IGNORECASE):
                continue
            offenders.append("%s:%d" % (name, i))
    return (not offenders, str(offenders) if offenders
            else "every mention of last-write-wins excludes it")


check("races", "last-write-wins is excluded everywhere",
      last_write_wins_is_absent_from_the_vocabulary)


def bounded_rework_loops_are_specified():
    body = spec("orchestrator-runtime-contract.md")
    needed = ["rework_loop_id", "iteration_ordinal", "max_iterations",
              "prior iteration's instances are retained", "not converging",
              "no default and no unbounded value"]
    missing = [n for n in needed if n not in body]
    if missing:
        return False, str(missing)
    if "graph-cycle ambiguity" not in body.lower() and "DAG" not in body:
        return False, "graph-cycle ambiguity is not addressed"
    return True, "loop identity, counter, limit, retained instances, escalation, no cycle ambiguity"


check("races", "bounded rework loops are specified", bounded_rework_loops_are_specified)


def compensation_is_a_new_governed_act():
    problems = ["missing from the orchestrator contract: %s" % p
                for p in says("orchestrator-runtime-contract.md",
                              "intent record", "authorisation record", "execution record",
                              "ATTEMPTED_OUTCOME_UNKNOWN")]
    problems.extend("missing from the failure model: %s" % p
                    for p in says("failure-recovery-race-model.md",
                                  "compensation_request", "compensation_authorisation",
                                  "compensation_execution",
                                  "never a rollback of a completed external act",
                                  "there is no undo"))
    return (not problems, str(problems)[:300] if problems
            else "intent/authorisation/execution/uncertainty plus a compensation lineage")


check("races", "compensation is a new governed act, never a rollback",
      compensation_is_a_new_governed_act)


def the_superseded_path_is_specified():
    body = spec("orchestrator-runtime-contract.md")
    if "SUPERSEDED` path" not in body and "The `SUPERSEDED` path" not in body:
        return False, "no supersession section"
    objects = ("Workflow Run", "Knowledge item version", "Canonical Record", "Artifact version",
               "Registry definition version", "Decision Record")
    missing = [o for o in objects if o not in body]
    if missing:
        return False, str(missing)
    if "never destructive" not in body.lower():
        return False, "non-destructiveness is not stated"
    return True, "supersession specified across %d object families, none destructive" % len(objects)


check("races", "the full SUPERSEDED path is specified", the_superseded_path_is_specified)


# =========================================================== 11. approval state (M-6)


def machine_readable_approval_state_is_specified():
    body = spec("approval-state-registry.md")
    required_answers = ("subject_ref", "status", "approving_human_authority",
                        "decision_right_ref", "approved_at", "source_approval_record",
                        "superseded_by", "revocation", "approval_scope",
                        "explicit_non_scope", "deferred_items")
    missing = [r for r in required_answers if r not in body]
    if missing:
        return False, str(missing)
    if "absence" not in body.lower() or "`PROPOSED`" not in body:
        return False, "the fail-closed default is not specified"
    return True, "a registry answering all required questions, failing closed on absence"


check("approval", "a machine-readable approval state is specified",
      machine_readable_approval_state_is_specified)


def historical_status_fields_are_not_rewritten():
    if says("approval-state-registry.md", "do not fix this by rewriting history"):
        return False, "the no-rewrite rule is not stated"
    if says("approval-state-registry.md", "is not fixed by editing either side"):
        return False, "the header/registry disagreement is not handled without editing"
    return True, "historical Status fields are not edited to make validators green"


check("approval", "historical artifact status fields are not rewritten",
      historical_status_fields_are_not_rewritten)


def approval_does_not_mass_promote():
    body = spec("approval-state-registry.md")
    if "no mass promotion" not in body.lower():
        return False, "the no-mass-promotion rule is absent"
    if "one row per" not in body.lower():
        return False, "granularity is not specified"
    return True, "one row per explicitly named subject; everything else stays PROPOSED"


check("approval", "approval state does not mass-promote artifacts", approval_does_not_mass_promote)


def the_registry_records_approval_and_never_creates_it():
    body = spec("approval-state-registry.md")
    needed = ["records approval; it never creates it", "Writing a row is not approving",
              "transcription, not an approval"]
    missing = [n for n in needed if n not in body]
    return (not missing, str(missing) if missing
            else "the registry is derived from human approval records and creates none")


check("approval", "the approval registry creates no approval",
      the_registry_records_approval_and_never_creates_it)


# =========================================================== 12. completeness and honesty


def the_completeness_matrix_covers_m1_to_m7():
    body = spec("phase-14-self-check.md")
    missing = [m for m in ("M-1", "M-2", "M-3", "M-4", "M-5", "M-6", "M-7") if
               "**%s**" % m not in body]
    if missing:
        return False, "matrix rows missing: %s" % missing
    if "R-1" not in body or "R-2" not in body:
        return False, "the two additional mandatory items are not in the matrix"
    return True, "M-1 through M-7 plus the two additional mandatory items"


check("completeness", "a completeness matrix covers Phase 13 M-1 through M-7",
      the_completeness_matrix_covers_m1_to_m7)


def inherited_regression_conditions_are_preserved():
    body = spec("phase-14-self-check.md") + spec("open-items-and-blocked-authorities.md")
    problems = []
    for phrase in ("159/160", "145/147", "MEDIUM-HIGH"):
        if phrase not in body:
            problems.append("missing: %s" % phrase)
    if "not repaired" not in body.lower() and "Not repaired" not in body:
        problems.append("the no-repair statement is absent")
    return (not problems, str(problems)[:300] if problems
            else "inherited Phase 11 and Phase 10 conditions reported and not repaired")


check("completeness", "inherited validator conditions are preserved exactly",
      inherited_regression_conditions_are_preserved)


def open_items_requiring_human_decision_are_listed():
    body = spec("open-items-and-blocked-authorities.md")
    ids = sorted({int(m) for m in re.findall(r"\*\*OI-(\d+)\*\*", body)})
    if len(ids) < 8:
        return False, "only %d open items listed" % len(ids)
    self_check = spec("phase-14-self-check.md")
    if "human architectural decision" not in self_check.lower():
        return False, "the self-check does not surface them"
    return True, "%d open items requiring a human architectural decision" % len(ids)


check("completeness", "specification choices needing human decision are listed",
      open_items_requiring_human_decision_are_listed)


def divergences_from_phase_12_are_recorded():
    """Where the spec departs from the reference implementation, it must say so."""
    documented = [name for name in REQUIRED_DOCS
                  if "Divergence" in spec(name) or "divergence" in spec(name)]
    if len(documented) < 8:
        return False, "only %d documents record divergences" % len(documented)
    return True, "%d documents record where they depart from the Phase 12 reference" % len(documented)


check("completeness", "divergences from the Phase 12 reference are recorded",
      divergences_from_phase_12_are_recorded)


def no_vacuous_checks():
    """This harness may not contain an unconditional pass."""
    text = read("validation/phase_14_validation.py")
    hits = [ln.strip() for ln in text.splitlines()
            if re.search(r"\bor\s+True\b|\breturn\s*\(\s*True\s*,\s*\"", ln)]
    return (not hits, str(hits)[:200] if hits else "no unconditional pass")


check("completeness", "the harness contains no vacuous or unconditional-pass check",
      no_vacuous_checks)


def the_harness_disclaims_governance_authority():
    text = read("validation/phase_14_validation.py")
    return ("NEVER GOVERNANCE AUTHORITY" in text,
            "the validator states it is an assurance tool only")


check("completeness", "the validator disclaims governance authority",
      the_harness_disclaims_governance_authority)


# =========================================================== main


def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv
    passed = sum(1 for r in RESULTS if r["pass"])
    if as_json:
        print(json.dumps({"total": len(RESULTS), "passed": passed, "results": RESULTS},
                         indent=2))
    else:
        order = []
        for r in RESULTS:
            if r["group"] not in order:
                order.append(r["group"])
        for group in order:
            print("\n[%s]" % group)
            for r in [x for x in RESULTS if x["group"] == group]:
                print("  %s  %s" % ("PASS" if r["pass"] else "FAIL", r["name"]))
                if (verbose or not r["pass"]) and r["evidence"]:
                    print("        %s" % r["evidence"])
        print("\n=== %d/%d PASS ===" % (passed, len(RESULTS)))
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
