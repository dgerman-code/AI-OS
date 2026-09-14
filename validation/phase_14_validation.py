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


def table_rows(name, section=None):
    """Only the table rows of a document (or one section of it).

    Content checks that scan whole documents fire on the prose that *explains a correction* -
    "an earlier revision invented `model_profile.<name>`" is a sentence saying the prefix is
    gone, and a naive scan reads it as the prefix being present. Structural claims are made in
    tables, so structural checks read tables."""
    body = spec(name) if section is None else section
    return [ln for ln in body.splitlines() if ln.lstrip().startswith("|")]


def command_rows():
    """The canonical governed-command inventory: (number, command, auth, act) per row.

    `api-command-contracts.md` §5.1 owns this set. Every cross-document coverage check in this
    harness derives from here rather than from a list restated in the validator, so adding a
    command to the specification without a transaction contract fails a check instead of
    quietly widening the system."""
    body = spec("api-command-contracts.md").split("### 5.1")[1].split("### 5.2")[0]
    rows = []
    for line in body.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*`(\w+)`\s*\|\s*\**(\w+)\**\s*\|\s*`(\w+)`\s*\|", line)
        if m:
            rows.append((int(m.group(1)), m.group(2), m.group(3), m.group(4)))
    return rows


#: Column positions in the §7.2 transaction table, named once so a table change breaks one
#: constant rather than five checks that each counted cells for themselves.
TXN = {"act": 0, "branch": 1, "read": 2, "validate": 3, "occ": 4, "writes": 5,
       "audit": 6, "exec": 7, "constraints": 8, "failure": 9}


def transaction_branch_rows():
    """Every row of §7.2 as a cell list. One act may have several branch rows."""
    rows = []
    for line in transaction_section().splitlines():
        if not line.startswith("| **"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= len(TXN):
            rows.append(cells)
    return rows


def transaction_rows():
    """Act key -> its branch rows. The act set is what the command inventory is compared to."""
    rows = {}
    for cells in transaction_branch_rows():
        rows.setdefault(cells[TXN["act"]].strip("*"), []).append(cells)
    return rows


def txn_single(act):
    """The one row of an unbranched act, or None where the act branches."""
    rows = transaction_rows().get(act, [])
    return rows[0] if len(rows) == 1 else None


def adversarial_rows():
    """Structured adversarial-test metadata: (id, commands, basis, attack, expected)."""
    body = spec("test-and-assurance-strategy.md")
    section = body.split("## 3. Adversarial tests")[1].split("## 4.")[0]
    rows = []
    for line in section.splitlines():
        m = re.match(r"^\|\s*(A\d+[a-z]?|P-A\d+[a-z]?)\s*\|(.+?)\|\s*\**(CURRENT|HYPOTHETICAL)\**\s*\|(.+?)\|(.+)\|\s*$", line)
        if m:
            commands = set(re.findall(r"`(\w+)`", m.group(2)))
            rows.append((m.group(1), commands, m.group(3), m.group(4).strip(), m.group(5).strip()))
    return rows


def uniqueness_ids():
    body = spec("persistence-and-transaction-model.md")
    return sorted({int(m) for m in re.findall(r"\|\s*U(\d+)\s*\|", body)})


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
    allowed_files = ("validation/phase_14_validation.py",
                     "validation/phase_14_mutation_probes.py")
    stray = [n for n in names
             if not n.startswith("implementation-spec/")
             and not n.startswith("prompts/")
             and n not in allowed_files]
    return (not stray, str(stray) if stray
            else "%d paths: the specification package, its validator, its mutation fixture "
                 "and the phase prompt" % len(names))


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


def transaction_section():
    body = spec("persistence-and-transaction-model.md")
    return body.split("### 7.2")[1].split("**Rule P-15.**")[0]


def the_transaction_table_is_exhaustive_over_the_command_inventory():
    """Exact set equality, both directions, derived from both documents.

    An omission on either side is the audit's second finding: a governed command with no commit
    contract cannot be built, and a contract nothing calls is a contract for nothing."""
    commands = command_rows()
    if not commands:
        return False, "the governed-command inventory could not be parsed"
    api_acts = {act for _n, _c, _a, act in commands}
    txn_acts = set(transaction_rows())
    if not txn_acts:
        return False, "the transaction contracts could not be parsed"
    problems = []
    missing = sorted(api_acts - txn_acts)
    extra = sorted(txn_acts - api_acts)
    if missing:
        problems.append("commands with no transaction contract: %s" % missing)
    if extra:
        problems.append("transaction contracts with no command: %s" % extra)
    # Duplicate coverage is permitted only through an explicit alias - the same act key on two
    # command rows - and any such alias must be visible here rather than implied.
    counts = {}
    for _n, cmd, _a, act in commands:
        counts.setdefault(act, []).append(cmd)
    aliased = {a: c for a, c in counts.items() if len(c) > 1}
    for column in ("Branch", "Read set", "Validation / preflight set", "Concurrency check",
                   "Audit events", "Exec events", "Constraints", "Failure before commit"):
        if column not in transaction_section():
            problems.append("the transaction table lacks the column: %s" % column)
    return (not problems, str(problems)[:300] if problems
            else "%d commands, %d transaction contracts, sets equal; %d explicit aliases"
                 % (len(commands), len(txn_acts), len(aliased)))


check("persistence", "the transaction table is exhaustive over the governed-command inventory",
      the_transaction_table_is_exhaustive_over_the_command_inventory)


def the_omitted_governed_acts_are_now_covered():
    """The specific acts the re-audit named as missing."""
    named = ("RecordIntervention", "ResumeRun", "UnblockRun", "SupplyGateEvidence",
             "CreateKnowledgeItem", "AdoptAISuggestion", "RaiseConflict",
             "ApplyConsequentStatusChange", "CompleteRun")
    commands = {c: act for _n, c, _a, act in command_rows()}
    txn = transaction_rows()
    missing = [c for c in named if c not in commands or commands[c] not in txn]
    return (not missing, "still uncovered: %s" % missing if missing
            else "all %d previously omitted governed acts have transaction contracts" % len(named))


def the_transaction_table_covers_every_governed_act():
    return the_omitted_governed_acts_are_now_covered()


check("persistence", "every previously omitted governed act now has a transaction contract",
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
              "bounded, reviewable transcription, not a standing privilege"]
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


# =========================================================== 13. fidelity to approved phases


def model_profile_identity_matches_phase_9():
    """The Model Profile's stable ID is Phase 9's, parsed from the approved Phase 9 document.

    Phase 9 `models/model-lifecycle-and-versioning.md` §0 gives the Model Profile the identity
    `model.<stable_snake_case_name>`. An earlier revision of this package invented
    `model_profile.<name>` and gave `model.<name>` to a separate `ModelRef`. Either way the
    approved scheme was not being used, so this check reads the approved document."""
    approved = read("models/model-lifecycle-and-versioning.md")
    stack = approved.split("## 0. The identity stack")[1].split("## 1.")[0]
    row = [ln for ln in stack.splitlines() if "**Model Profile**" in ln]
    if not row:
        return False, "the approved Model Profile layer row was not found"
    approved_id = re.search(r"`(model\.[a-z_<>]+)`", row[0])
    if approved_id is None:
        return False, "the approved Model Profile identity pattern was not found"
    body = spec("domain-identity-model.md")
    problems = []
    if "`model.<stable_snake_case_name>`" not in body:
        problems.append("the specification does not use Phase 9's Model Profile identity")
    # Section 3 only: the identity inventory. The divergence table in section 7 legitimately
    # names `ModelRef` when describing what the Phase 12 reference does, and recording a
    # divergence is the opposite of committing it.
    inventory = spec("domain-identity-model.md").split("## 3.")[1].split("## 4.")[0]
    rows = "\n".join(table_rows("domain-identity-model.md", inventory))
    if "model_profile.<" in rows:
        problems.append("the invented model_profile.< > prefix is still used in an identity table")
    if re.search(r"`ModelRef`", rows):
        problems.append("an independent stable ModelRef is still declared in an identity table")
    for layer in ("Model Family", "Underlying Model Release", "Model Profile",
                  "Registry Profile Version", "Provider Offering Mapping", "Deployment Profile"):
        if layer not in body:
            problems.append("identity stack layer absent: %s" % layer)
    if says("domain-identity-model.md", "there is no independent stable"):
        problems.append("the no-ModelRef rule is not stated")
    return (not problems, str(problems)[:300] if problems
            else "the six-layer Phase 9 identity stack, with %s as the Model Profile identity"
                 % approved_id.group(1))


check("fidelity", "Model Profile identity matches the approved Phase 9 scheme",
      model_profile_identity_matches_phase_9)


def model_result_lineage_uses_fields_the_routing_decision_persists():
    """Every field the Model Result is checked against must exist on the Routing Decision."""
    body = spec("model-router-runtime-contract.md")
    decision = body.split("## 5. `routing_decision`")[1].split("## 6.")[0]
    result = body.split("### 6.2 `model_result`")[1].split("## 7.")[0]
    problems = []
    # The five equality-checked elements must be columns of the decision.
    for field in ("model_profile_ref", "model_profile_registry_version", "offering_mapping_ref",
                  "provider_profile_ref", "deployment_profile_ref"):
        if field not in decision:
            problems.append("Routing Decision lacks %s" % field)
        if field not in result:
            problems.append("Model Result lacks %s" % field)
    # A lineage check against a field the decision does not hold is the audit's finding.
    result_rows = "\n".join(table_rows("model-router-runtime-contract.md", result))
    if re.search(r"`model_ref`", result_rows):
        problems.append("the Model Result table still names a non-existent model_ref")
    if "originator_release_identity" not in decision:
        problems.append("element 22 is missing from the Routing Decision")
    if "observed_release_identity" not in result or "release_identity_match" not in result:
        problems.append("the release-identity observation is not recorded on the result")
    if says("model-router-runtime-contract.md", "PROVIDER_VERSION_CHANGE"):
        problems.append("a diverged release identity has no specified outcome")
    return (not problems, str(problems)[:300] if problems
            else "five elements compared for equality, the sixth observed and compared")


check("fidelity", "Model Result lineage is checked against persisted Routing Decision fields",
      model_result_lineage_uses_fields_the_routing_decision_persists)


def conflict_resolution_is_not_authority_bearing():
    """Phase 8 §3 rule 2: a Decision Right cannot decide which source is accurate."""
    approved = read("knowledge/conflict-and-provenance-model.md")
    if "professional conclusion" not in approved:
        return False, "the approved Phase 8 rule was not found"
    api = spec("api-command-contracts.md")
    problems = []
    auth = {c: a for _n, c, a, _act in command_rows()}
    if "ResolveConflict" not in auth:
        problems.append("ResolveConflict is not in the command inventory")
    elif auth["ResolveConflict"] != "R":
        problems.append("ResolveConflict is auth class %s, not R" % auth["ResolveConflict"])
    row = [ln for ln in api.splitlines() if "`ResolveConflict`" in ln and ln.startswith("|")]
    if row and "NO_APPLICABLE_DECISION_RIGHT" in row[0]:
        problems.append("ResolveConflict still refuses for want of a Decision Right")
    if says("knowledge-and-canonical-model.md",
            "It cannot decide", "owned by an eligible Role and checked by review"):
        problems.append("the Phase 8 distinction is not restored in the knowledge model")
    if says("knowledge-and-canonical-model.md", "decision_record_ref"):
        problems.append("the resolution record does not model the optional consequent authority")
    return (not problems, str(problems)[:300] if problems
            else "resolution is a Role conclusion checked by review; authority is a separate act")


check("fidelity", "conflict resolution is a Role conclusion, not an exercise of authority",
      conflict_resolution_is_not_authority_bearing)


def cancellation_and_termination_are_asymmetric():
    """Phase 11: CANCELLED is a human act; TERMINATED is the system stopping a breach."""
    approved = read("orchestration/state-machine-and-transitions.md")
    if "Stopped by the system because continuing would breach a constraint" not in approved:
        return False, "the approved TERMINATED definition was not found"
    api = spec("api-command-contracts.md")
    problems = []
    inventory = {c: (a, act) for _n, c, a, act in command_rows()}
    for name, expected_auth in (("CancelRun", "h"), ("TerminateRun", "S")):
        if name not in inventory:
            problems.append("%s is not a distinct command" % name)
            continue
        if inventory[name][0] != expected_auth:
            problems.append("%s auth is %s, expected %s" % (name, inventory[name][0], expected_auth))
    if inventory.get("CancelRun", (None, None))[1] == inventory.get("TerminateRun", (None, ""))[1]:
        problems.append("cancel and terminate share one transaction act")
    api_lines = {c: ln for ln in api.splitlines()
                 for c in re.findall(r"^\|\s*\d+\s*\|\s*`(\w+)`", ln)}
    cancel_line = api_lines.get("CancelRun", "")
    terminate_line = api_lines.get("TerminateRun", "")
    if "intervention" not in cancel_line.lower():
        problems.append("CancelRun does not require an intervention")
    if "no human intervention is accepted" not in terminate_line.lower():
        problems.append("TerminateRun does not refuse a human intervention")
    txn = transaction_rows()
    for act in ("cancel_run", "terminate_run"):
        if act not in txn:
            problems.append("no transaction contract for %s" % act)
    terminate = txn_single("terminate_run")
    if terminate is None:
        problems.append("terminate_run has no single transaction contract")
    elif "NULL" not in terminate[TXN["exec"]]:
        problems.append("terminate_run does not record a null human identity")
    if says("audit-provenance-observability.md", "never synthesised"):
        problems.append("the audit model permits a synthesised human identity")
    return (not problems, str(problems)[:300] if problems
            else "cancellation is human with an intervention; termination is system with a constraint")


check("fidelity", "cancellation and termination keep their approved asymmetry",
      cancellation_and_termination_are_asymmetric)


def audit_cardinality_is_one_per_governed_record_mutation():
    """One rule, stated once, and every act in the table states its exact audit row count."""
    problems = []
    if says("persistence-and-transaction-model.md",
            "one audit event per persisted governed-record mutation"):
        problems.append("the cardinality rule is not stated in the persistence model")
    if says("audit-provenance-observability.md",
            "one audit event per persisted governed-record mutation"):
        problems.append("the audit model does not state the same rule")
    if says("persistence-and-transaction-model.md", "no grouping"):
        problems.append("grouping is not prohibited")
    section = transaction_section()
    rows = transaction_branch_rows()
    for cells in rows:
        audit = cells[TXN["audit"]].replace("*", "")
        if not re.match(r"^(\d+|\d+ \+ .+|\d+ or \d+)$", audit):
            problems.append("%s/%s: audit column is not a count: %r"
                            % (cells[TXN["act"]].strip("*"), cells[TXN["branch"]], audit[:30]))
    if not rows:
        problems.append("no act rows parsed")
    return (not problems, str(problems)[:300] if problems
            else "%d branch rows, each stating its exact audit-event count" % len(rows))


check("fidelity", "audit-event cardinality is one per governed-record mutation, everywhere",
      audit_cardinality_is_one_per_governed_record_mutation)


APPROVAL_STATUSES = ("PROPOSED", "APPROVED", "APPROVED_WITH_CONDITIONS", "SUPERSEDED", "REVOKED")


def approval_state_currentness_is_a_pointer_not_a_status():
    persistence = spec("persistence-and-transaction-model.md")
    registry = spec("approval-state-registry.md")
    problems = []
    u19 = [ln for ln in table_rows("persistence-and-transaction-model.md") if "| U19 " in ln]
    if not u19:
        problems.append("U19 is not in the uniqueness table")
    else:
        constraint_cell = [c.strip() for c in u19[0].strip().strip("|").split("|")][2]
        if re.search(r"status\s*=\s*'ACTIVE'", constraint_cell):
            problems.append("U19 still keys on a nonexistent ACTIVE approval status")
        if "approval_state_current" not in constraint_cell:
            problems.append("U19 does not key on the current pointer")
    if "approval_state_current" not in persistence:
        problems.append("the current pointer is absent from the persistence model")
    if "approval_state_current" not in registry:
        problems.append("the current pointer is absent from the approval registry")
    declared = set(re.findall(r"^\| `([A-Z_]+)` \|", registry, re.MULTILINE))
    if "ACTIVE" in declared:
        problems.append("an ACTIVE approval status is declared")
    missing = [v for v in APPROVAL_STATUSES if "`%s`" % v not in registry]
    if missing:
        problems.append("approval status vocabulary missing: %s" % missing)
    if says("approval-state-registry.md", "at most one current row per subject version"):
        problems.append("the totality of the uniqueness rule is not stated")
    if says("approval-state-registry.md", "APPROVED_WITH_CONDITIONS"):
        problems.append("APPROVED_WITH_CONDITIONS is not covered")
    return (not problems, str(problems)[:300] if problems
            else "currentness is a pointer; %d statuses, none of them ACTIVE" % len(APPROVAL_STATUSES))


check("fidelity", "approval-state currentness is a pointer and the status vocabulary is exact",
      approval_state_currentness_is_a_pointer_not_a_status)


def the_phase_4_baseline_is_read_from_its_approval_record():
    """Read the SHA from the approval record; verify the specification cites that exact SHA."""
    record = read("reviews/phase-4-final-approval.md")
    match = re.search(r"Approved Baseline Commit:\s*`([0-9a-f]{40})`", record)
    if match is None:
        return False, "the Phase 4 approval record states no baseline commit"
    sha = match.group(1)
    readme = spec("README.md")
    row = [ln for ln in readme.splitlines() if "Phase 4" in ln and "|" in ln]
    if not row:
        return False, "the README baseline table has no Phase 4 row"
    if sha not in row[0]:
        return False, "the README cites %s, the record states %s" % (row[0][:80], sha[:12])
    # Resolution is checked where a git directory is available. Where it is not - a detached
    # copy of the package, as the mutation fixture builds - the citation comparison above is
    # still the substance of the check and still fails on a wrong or missing SHA.
    resolvable = os.path.isdir(os.path.join(REPO, ".git"))
    if resolvable:
        resolved = subprocess.run(["git", "cat-file", "-t", sha], cwd=REPO,
                                  capture_output=True, text=True)
        if resolved.stdout.strip() != "commit":
            return False, "%s does not resolve in this repository" % sha[:12]
    blocked = spec("open-items-and-blocked-authorities.md")
    if "OI-12" in blocked and "removed" not in blocked.lower():
        return False, "OI-12 is still recorded as an open item"
    return True, "Phase 4 baseline %s read from the approval record and cited correctly" % sha[:12]


check("fidelity", "the Phase 4 baseline is the one its approval record states",
      the_phase_4_baseline_is_read_from_its_approval_record)


def identity_versioning_rule_is_category_aware():
    body = spec("domain-identity-model.md")
    problems = []
    if says("domain-identity-model.md", "two reference categories"):
        problems.append("Rule I-1 does not distinguish categories")
    for marker in ("Governed definition or profile", "Immutable runtime-instance"):
        if marker not in body:
            problems.append("category missing: %s" % marker)
    if says("domain-identity-model.md", "reproducibility without invented versions"):
        problems.append("the reproducibility rationale is not stated")
    return (not problems, str(problems)[:300] if problems
            else "versioned definitions and unversioned instance identities are distinguished")


check("fidelity", "the identity versioning rule distinguishes definitions from instances",
      identity_versioning_rule_is_category_aware)


def self_review_is_refused_on_identity_not_on_a_label():
    body = spec("decision-review-authority-model.md")
    problems = []
    if says("decision-review-authority-model.md",
            "equals any producer identity recorded on the reviewed artifact version"):
        problems.append("producer identity inequality is not specified")
    if says("decision-review-authority-model.md", "equals the assignee of the producing assignment"):
        problems.append("assignee inequality is not specified")
    if says("decision-review-authority-model.md", "diversity of models is not"):
        problems.append("model diversity is not excluded as independence")
    tests = spec("test-and-assurance-strategy.md")
    if "PRODUCER_REVIEW_PROHIBITED" not in tests:
        problems.append("no adversarial test for producer review")
    return (not problems, str(problems)[:300] if problems
            else "self-review is refused by identity comparison, not by a class label")


check("fidelity", "self-review is refused on identity inequality", self_review_is_refused_on_identity_not_on_a_label)


def no_admin_substitution_for_a_missing_right():
    migrations = spec("migrations-versioning-compatibility.md")
    security = spec("security-identity-access.md")
    problems = []
    if says("migrations-versioning-compatibility.md", "no --force"):
        problems.append("the migration applier does not forbid a force path")
    if "NO_APPLICABLE_DECISION_RIGHT" not in migrations:
        problems.append("a destructive migration does not fail on a missing Right")
    if says("security-identity-access.md",
            "ability to perform an action is not authority to authorise one"):
        problems.append("the administrator limit is not stated")
    for substitution in ("admin role", "service account", "database owner", "RLS bypass"):
        if substitution.lower() not in spec("decision-review-authority-model.md").lower():
            problems.append("not excluded as a substitution: %s" % substitution)
    return (not problems, str(problems)[:300] if problems
            else "no administrative path substitutes for the destructive-migration Right")


check("fidelity", "no admin path substitutes for a missing destructive-migration Right",
      no_admin_substitution_for_a_missing_right)


def governed_uniqueness_has_no_on_conflict_exception():
    body = spec("persistence-and-transaction-model.md")
    if says("persistence-and-transaction-model.md", "on conflict do nothing is prohibited"):
        return False, "the prohibition is absent"
    offenders = []
    for name in REQUIRED_DOCS:
        for i, line in enumerate(spec(name).splitlines(), 1):
            if "ON CONFLICT" not in line.upper():
                continue
            if re.search(r"\b(prohibit\w*|never|not|no)\b", line, re.IGNORECASE):
                continue
            offenders.append("%s:%d" % (name, i))
    static = spec("test-and-assurance-strategy.md")
    if "ON CONFLICT DO NOTHING" not in static:
        offenders.append("no static check enforces it")
    return (not offenders, str(offenders)[:300] if offenders
            else "prohibited in the model and enforced by a static check")


check("fidelity", "governed uniqueness admits no ON CONFLICT DO NOTHING exception",
      governed_uniqueness_has_no_on_conflict_exception)


def the_origin_axis_is_exactly_the_approved_four():
    """Not "contains four values" - the four APPROVED values, parsed from the Phase 8 document.

    A mutation that renames `EXTERNAL_ORIGIN` to something plausible keeps the count at four
    and passes a completeness check that only counts. This one compares the sets."""
    approved = read("knowledge/knowledge-state-model.md")
    section = approved.split("## 2a.")[1].split("## 3.")[0]
    approved_origins = set(re.findall(r"^\| `([A-Z_]+)` \|", section, re.MULTILINE))
    if approved_origins != set(ORIGINS):
        return False, ("this validator's origin set disagrees with Phase 8: %s"
                       % sorted(approved_origins ^ set(ORIGINS)))
    body = spec("knowledge-and-canonical-model.md")
    axis = body.split("### 2.3 Axis 3")[1].split("### 2.4")[0]
    spec_origins = set(re.findall(r"^\| `([A-Z_]+)` \|", axis, re.MULTILINE))
    if spec_origins != approved_origins:
        return False, ("origin axis differs from the approved set: extra %s, missing %s"
                       % (sorted(spec_origins - approved_origins),
                          sorted(approved_origins - spec_origins)))
    return True, "the origin axis is exactly the approved four: %s" % sorted(approved_origins)


check("knowledge", "the origin axis is exactly the approved four values",
      the_origin_axis_is_exactly_the_approved_four)


def the_separator_boundary_rule_is_stated_as_a_rule():
    """The prefix trap is the one scope defect a string-handling mistake produces silently."""
    body = spec("scope-and-context-model.md")
    problems = []
    if not re.search(r"\*\*Rule S-2 — the prefix trap\.\*\*", body):
        problems.append("Rule S-2 is not stated as the prefix trap")
    if says("scope-and-context-model.md",
            "the next character in `d` is the separator"):
        problems.append("the separator-boundary test is not defined")
    if says("scope-and-context-model.md", "acme_holdings"):
        problems.append("the worked counterexample is absent")
    tests = spec("test-and-assurance-strategy.md")
    if "separator-boundary" not in tests:
        problems.append("no mandatory test case for the boundary rule")
    security = spec("security-identity-access.md")
    if says("security-identity-access.md", "never on a plain"):
        problems.append("the RLS predicate does not forbid a plain prefix match")
    return (not problems, str(problems)[:300] if problems
            else "the prefix trap is a named rule, a test case and an RLS predicate constraint")


check("scope", "the separator-boundary ancestry rule is stated and enforced",
      the_separator_boundary_rule_is_stated_as_a_rule)


def operational_events_are_inadmissible_as_evidence():
    """Stated, enforced structurally, and unreachable through the evidence contract."""
    problems = []
    if says("audit-provenance-observability.md",
            "may satisfy a **review**", "and none may serve as evidence in any of them"):
        problems.append("the inadmissibility rule is not stated in full")
    if says("audit-provenance-observability.md",
            "has an `append` operation and **no read operation at all**"):
        problems.append("the write-only interface is not specified")
    if says("audit-provenance-observability.md", "observability is never authority"):
        problems.append("observability is not excluded as authority")
    # The gate evidence contract must admit exactly four typed classes, none an event.
    gates = spec("orchestrator-runtime-contract.md").split("### 6.1")[1].split("### 6.2")[0]
    admissible = set(re.findall(r"\| `([A-Z_]+)` \| `?([A-Za-z]+)`? \|", gates))
    evidence_types = {t for _k, t in admissible}
    forbidden = {"ExecutionEvent", "RuntimeEvent", "AuditEvent", "ModelResult", "Log"}
    if evidence_types & forbidden:
        problems.append("an event type is admissible gate evidence: %s"
                        % sorted(evidence_types & forbidden))
    if not evidence_types:
        problems.append("the gate evidence contract could not be parsed")
    # No sentence anywhere may assert the opposite. A denial repeated in three places is not
    # protection if a fourth place quietly affirms it, and "never" changed to "ordinarily" in
    # one line is exactly the mutation a count-based check misses.
    # Only PREDICATIVE forms are assertions: "is/are/becomes/counts as/serves as/admissible as
    # governance evidence". A label like "runtime event vs governance evidence" asserts nothing,
    # and a scan that cannot tell the two apart forces documents to be reworded around it
    # instead of checked by it.
    predicative = re.compile(
        r"\b(is|are|becomes?|counts? as|serves? as|admissible as|treated as|acts? as|"
        r"usable as|accepted as)\s+(a\s+|an\s+|the\s+)?governance evidence")
    negated = re.compile(r"\b(not|never|nowhere|no|none|cannot|may not|must not|prohibit\w*|"
                         r"exclud\w*|inadmissib\w*|denie?s?|refus\w*)\b")
    affirmations = []
    for name in REQUIRED_DOCS:
        lines = spec(name).splitlines()
        for i, line in enumerate(lines):
            window = flat(" ".join(lines[max(0, i - 1):i + 1]))
            if not predicative.search(window):
                continue
            if negated.search(window):
                continue
            affirmations.append("%s:%d %s" % (name, i + 1, line.strip()[:70]))
    if affirmations:
        problems.append("governance evidence asserted rather than denied: %s" % affirmations[:2])
    # In the two documents that OWN the rule, every mention must carry its denial. This is the
    # stricter form, applied only where the rule lives, so that removing one denial is caught
    # even when the phrase survives elsewhere.
    for owner in ("audit-provenance-observability.md", "orchestrator-runtime-contract.md"):
        lines = spec(owner).splitlines()
        for i, line in enumerate(lines):
            if "governance evidence" not in flat(line):
                continue
            window = flat(" ".join(lines[max(0, i - 1):i + 2]))
            if negated.search(window) or "which it is not" in window:
                continue
            problems.append("%s:%d states governance evidence without a denial: %s"
                            % (owner, i + 1, line.strip()[:60]))
    return (not problems, str(problems)[:300] if problems
            else "inadmissible by rule, by interface and by the evidence contract (%d types)"
                 % len(evidence_types))


check("events", "operational and execution events can never satisfy governance evidence",
      operational_events_are_inadmissible_as_evidence)


# =========================================================== 14. cross-document exact sets


def the_uniqueness_count_is_derived_not_restated():
    """Every document that states a count must state the count of the canonical inventory."""
    ids = uniqueness_ids()
    if not ids:
        return False, "the canonical uniqueness inventory could not be parsed"
    if ids != list(range(1, len(ids) + 1)):
        return False, "the inventory is not contiguous: %s" % ids
    n = len(ids)
    problems = []
    canonical = spec("persistence-and-transaction-model.md")
    if "canonical uniqueness inventory" not in canonical:
        problems.append("the inventory is not declared canonical")
    # Any document citing a count of "uniqueness constraints" must cite n.
    pattern = re.compile(r"(\d+)\s+(?:durable\s+)?uniqueness constraints", re.IGNORECASE)
    for name in REQUIRED_DOCS:
        for i, line in enumerate(spec(name).splitlines(), 1):
            for stated in pattern.findall(flat(line)):
                if int(stated) != n:
                    problems.append("%s:%d states %s uniqueness constraints, inventory has %d"
                                    % (name, i, stated, n))
    # Milestones and gates must reference the inventory rather than a frozen number.
    sequencing = spec("implementation-sequencing.md")
    for marker in ("canonical uniqueness inventory",):
        if marker not in sequencing:
            problems.append("the sequencing document does not reference the inventory")
    if "currently **%d**" % n not in sequencing:
        problems.append("the sequencing document does not state the current count %d" % n)
    return (not problems, str(problems)[:300] if problems
            else "U1-U%d canonical; every stated count agrees" % n)


check("crossdoc", "the uniqueness count is one inventory, cited consistently",
      the_uniqueness_count_is_derived_not_restated)


def adversarial_metadata_agrees_with_the_command_contracts():
    """Rule T-3a: a test row may not contradict the contract of the command it attacks."""
    rows = adversarial_rows()
    if not rows:
        return False, "the adversarial test metadata could not be parsed"
    inventory = {c: (a, act) for _n, c, a, act in command_rows()}
    problems = []
    for test_id, commands, basis, attack, expected in rows:
        for cmd in commands:
            if cmd not in inventory:
                problems.append("%s attacks unknown command %s" % (test_id, cmd))
                continue
            # The repaired terminal contract: TerminateRun accepts no intervention, so a test
            # may attack the fact that it is refused - and may not expect the intervention
            # contract's own errors, which belong to commands that take one.
            if cmd == "TerminateRun":
                if "FOREIGN_RUN_LINEAGE" in expected or "INTERVENTION_INVALID" in expected:
                    problems.append("%s expects an intervention-contract error from "
                                    "TerminateRun, which accepts no intervention" % test_id)
                if "human intervention" in flat(attack) and "unexpected_human_intervention" \
                        not in flat(expected) and not test_id.startswith("P-"):
                    problems.append("%s supplies a human intervention to TerminateRun without "
                                    "expecting it to be refused as unexpected" % test_id)
        if basis == "HYPOTHETICAL" and re.search(r"\bis mapped\b|\bmapped Right exists\b",
                                                 flat(expected)):
            problems.append("%s is HYPOTHETICAL but claims a mapped Right exists" % test_id)
    # The terminal asymmetry must be attacked on its own terms and controlled positively.
    terminate_tests = [r for r in rows if "TerminateRun" in r[1] and not r[0].startswith("P-")]
    if len(terminate_tests) < 4:
        problems.append("only %d adversarial tests attack the TerminateRun contract"
                        % len(terminate_tests))
    positives = [r for r in rows if r[0].startswith("P-") and "TerminateRun" in r[1]]
    if not positives:
        problems.append("no positive control for valid constraint-driven termination")
    else:
        control = positives[0][4]
        if "null" not in flat(control) or "terminated" not in flat(control):
            problems.append("the termination positive control does not assert a null human "
                            "identity on a successful TERMINATED")
    return (not problems, str(problems)[:400] if problems
            else "%d adversarial rows, %d attacking TerminateRun, with a positive control"
                 % (len(rows), len(terminate_tests)))


check("crossdoc", "adversarial test metadata agrees with the command contracts",
      adversarial_metadata_agrees_with_the_command_contracts)


def the_canonical_promotion_tests_are_not_contradictory():
    """A17a is about today; A17b is explicitly hypothetical and claims nothing about today."""
    rows = {r[0]: r for r in adversarial_rows()}
    problems = []
    if "A17a" not in rows or "A17b" not in rows:
        problems.append("the canonical-promotion test is not split into current and hypothetical")
        return False, str(problems)
    current = rows["A17a"]
    hypothetical = rows["A17b"]
    if current[2] != "CURRENT":
        problems.append("A17a is not marked CURRENT")
    if hypothetical[2] != "HYPOTHETICAL":
        problems.append("A17b is not marked HYPOTHETICAL")
    if "NO_APPLICABLE_DECISION_RIGHT" not in current[4]:
        problems.append("A17a does not expect NO_APPLICABLE_DECISION_RIGHT")
    if "zero governed writes" not in flat(current[4]):
        problems.append("A17a does not assert zero mutation")
    if "not evidence that ba-1 is resolved" not in flat(hypothetical[4]):
        problems.append("A17b does not disclaim being evidence about BA-1")
    # And no row anywhere may claim a mapped Right is available today.
    for test_id, _c, basis, attack, expected in adversarial_rows():
        if basis == "CURRENT" and "mapped right" in flat(attack) and \
                "no applicable" not in flat(attack) and "not mapped" not in flat(attack):
            problems.append("%s claims a mapped Right under CURRENT basis" % test_id)
    return (not problems, str(problems)[:300] if problems
            else "A17a is current and refuses; A17b is hypothetical and claims nothing about today")


check("crossdoc", "the canonical-promotion tests are not internally contradictory",
      the_canonical_promotion_tests_are_not_contradictory)


def the_approval_commands_match_the_registry_semantics():
    inventory = {c: (a, act) for _n, c, a, act in command_rows()}
    registry = spec("approval-state-registry.md")
    txn = transaction_rows()
    problems = []
    if "RecordApprovalState" in inventory:
        problems.append("the ambiguous single RecordApprovalState command still exists")
    for name, expected_auth in (("TranscribeApprovalState", "h"),
                                ("RecordNewApprovalState", "H")):
        if name not in inventory:
            problems.append("%s is not a command" % name)
            continue
        if inventory[name][0] != expected_auth:
            problems.append("%s auth is %s, expected %s"
                            % (name, inventory[name][0], expected_auth))
        if name not in registry:
            problems.append("%s is not described in the approval registry" % name)
        act = inventory[name][1]
        row = txn_single(act)
        if row is None:
            problems.append("%s has no single transaction contract" % act)
            continue
        writes = row[TXN["writes"]]
        if "approval_state_record" not in writes or "approval_state_current" not in writes:
            problems.append("%s does not write both the history row and the pointer" % act)
        if row[TXN["audit"]].replace("*", "") != "2":
            problems.append("%s does not write 2 audit events" % act)
    if says("approval-state-registry.md", "transcription is mechanical or it is refused"):
        problems.append("mechanical transcription is not required")
    if says("approval-state-registry.md", "nullable Right lineage is a historical fact"):
        problems.append("nullable historical Right lineage is not stated")
    if says("approval-state-registry.md", "history and pointer move together or not at all"):
        problems.append("the atomic history+pointer rule is not stated")
    if says("security-identity-access.md", "a recording API is not an authority surface"):
        problems.append("the security model does not close the recording-API route")
    return (not problems, str(problems)[:400] if problems
            else "two approval acts, h and H, each writing history and pointer atomically")


check("crossdoc", "approval command classes match the approval-state registry semantics",
      the_approval_commands_match_the_registry_semantics)


AUDIT_MUTATION_KINDS = ("INSERT", "VERSION_APPEND", "UPDATE", "LINK_APPEND",
                        "LIFECYCLE_STATE_CHANGE", "SUPERSEDE", "POINTER_MOVE", "DESTROY")


def the_audit_version_nullability_matrix_is_complete():
    body = spec("audit-provenance-observability.md")
    if "### 4.1" not in body:
        return False, "the version-nullability matrix section is absent"
    matrix = body.split("### 4.1")[1].split("**Rule V-5.**")[0]
    problems = []
    parsed = {}
    for line in matrix.splitlines():
        m = re.match(r"^\|\s*`([A-Z_]+)`\s*\|(.+?)\|(.+?)\|(.+?)\|\s*$", line)
        if m:
            parsed[m.group(1)] = (flat(m.group(3)), flat(m.group(4)))
    missing = [k for k in AUDIT_MUTATION_KINDS if k not in parsed]
    if missing:
        problems.append("mutation kinds missing from the matrix: %s" % missing)
    # The specific contract the re-audit required.
    if "INSERT" in parsed:
        before, after = parsed["INSERT"]
        if "null" not in before or "not null" in before:
            problems.append("INSERT does not require a null record_version_before")
        if "not null" not in after:
            problems.append("INSERT does not require a non-null record_version_after")
    for kind in ("VERSION_APPEND", "UPDATE", "LIFECYCLE_STATE_CHANGE", "SUPERSEDE"):
        if kind in parsed and "not null" not in parsed[kind][0]:
            problems.append("%s does not require a before version" % kind)
    if "DESTROY" in parsed and "not null" in parsed["DESTROY"][1]:
        problems.append("DESTROY requires an after version, which cannot exist")
    if says("audit-provenance-observability.md", "the matrix is a constraint, not guidance"):
        problems.append("the matrix is not stated as a check constraint")
    if says("audit-provenance-observability.md", "BA-3 remains blocked"):
        problems.append("DESTROY is defined without restating that BA-3 is blocked")
    if says("audit-provenance-observability.md", "no audit event exists for a refused"):
        problems.append("refused transactions are not excluded from audit")
    return (not problems, str(problems)[:400] if problems
            else "%d mutation kinds, each with an explicit before/after nullability" % len(parsed))


check("crossdoc", "the audit version-nullability matrix is explicit and complete",
      the_audit_version_nullability_matrix_is_complete)


def blocked_commands_declare_zero_writes():
    inventory = {c: act for _n, c, _a, act in command_rows()}
    txn = transaction_rows()
    problems = []
    for name in ("PromoteToCanonical", "ReparentScopeNode", "DestroyGovernedContent",
                 "ApplyDestructiveMigration"):
        act = inventory.get(name)
        if act is None:
            problems.append("%s is not in the command inventory" % name)
            continue
        cells = txn_single(act)
        if cells is None:
            problems.append("%s has no single transaction contract" % act)
            continue
        if "0" not in cells[TXN["writes"]]:
            problems.append("%s does not declare zero governed writes" % act)
        if cells[TXN["audit"]].replace("*", "") != "0":
            problems.append("%s does not declare zero audit events" % act)
        if "1" not in cells[TXN["exec"]]:
            problems.append("%s does not declare its refusal execution event" % act)
    if says("api-command-contracts.md", "a refused transaction of any kind writes no audit"):
        problems.append("the general refusal rule is not stated in the API contract")
    return (not problems, str(problems)[:300] if problems
            else "four blocked acts: zero writes, zero audit events, one refusal event each")


check("crossdoc", "blocked commands declare zero writes and zero audit events",
      blocked_commands_declare_zero_writes)


# =========================================================== 15. canonical inventories


def assurance_inventories():
    """The five canonical assurance inventories, parsed from their owning tables.

    IDs are taken exactly - `A12a` and `A12b` are two IDs, and `A12` is not one. Prefix
    matching is never used, because a gate requiring "A12" would then silently be satisfied by
    a test that does not exist."""
    body = spec("test-and-assurance-strategy.md")
    def ids(pattern):
        return set(re.findall(pattern, body, re.MULTILINE))
    return {
        "A": ids(r"^\|\s*(A\d+[a-z]?)\s*\|"),
        "P-A": ids(r"^\|\s*(P-A\d+[a-z]?)\s*\|"),
        "I": ids(r"^\|\s*(I\d+)\s*\|"),
        "P": ids(r"^\|\s*(P\d+)\s*\|"),
        "S": ids(r"^\|\s*(S\d+)\s*\|"),
    }


#: Documents whose statements are normative gates rather than commentary. A stale count or a
#: stale range here is a defect; the same words inside a rule that explains why ranges are
#: forbidden are not.
NORMATIVE_DOCS = ("implementation-sequencing.md", "phase-14-self-check.md")


def the_assurance_inventories_are_declared_and_non_empty():
    inventories = assurance_inventories()
    problems = [k for k, v in inventories.items() if not v]
    if problems:
        return False, "empty inventories: %s" % problems
    body = spec("test-and-assurance-strategy.md")
    if says("test-and-assurance-strategy.md", "the inventory is the contract, never a range"):
        problems.append("the no-range rule is not stated")
    if says("test-and-assurance-strategy.md", "suffixed IDs are exact"):
        problems.append("exact-suffix matching is not required")
    if "## 2a." not in body:
        problems.append("the canonical inventory section is absent")
    # The suffixed IDs must actually be present, or the rule protects nothing.
    if not {i for i in inventories["A"] if i[-1].isalpha()}:
        problems.append("no suffixed adversarial IDs exist, so exactness is untested")
    return (not problems, str(problems)[:300] if problems
            else "A %d · P-A %d · I %d · P %d · S %d, suffixes exact"
                 % tuple(len(inventories[k]) for k in ("A", "P-A", "I", "P", "S")))


check("crossdoc", "the canonical assurance inventories are declared and parsable",
      the_assurance_inventories_are_declared_and_non_empty)


def normative_gates_require_the_whole_inventory():
    """M20 and G-R must require every current ID, not a prefix range."""
    inventories = assurance_inventories()
    sequencing = spec("implementation-sequencing.md")
    problems = []
    gates = [ln for ln in sequencing.splitlines()
             if ln.startswith("| **M20**") or ln.startswith("| **G-R**")]
    if len(gates) != 2:
        problems.append("M20 and G-R were not both found")
        return False, str(problems)
    for gate in gates:
        name = gate.split("|")[1].strip()
        # A range is the stale form and is forbidden outright in a normative gate.
        ranges = re.findall(r"\b([AIPS]\d+)\s*[–-]\s*([AIPS]?\d+)", gate)
        if ranges:
            problems.append("%s expresses a requirement as a range: %s" % (name, ranges[:2]))
        if "canonical assurance inventor" not in flat(gate) and \
                "every id in" not in flat(gate):
            problems.append("%s does not require the whole inventory" % name)
        # Any count it states must be a real inventory size.
        for stated in re.findall(r"\*\*(\d+)\*\*", gate):
            if int(stated) not in {len(v) for v in inventories.values()}:
                problems.append("%s states %s, which is no inventory's size" % (name, stated))
        # Any ID it names must exist exactly.
        for cited in re.findall(r"\b(P-A\d+[a-z]?|A\d+[a-z]?|I\d+|P\d+|S\d+)\b", gate):
            prefix = "P-A" if cited.startswith("P-A") else cited[0]
            if cited not in inventories.get(prefix, set()):
                problems.append("%s cites %s, which is not in the %s inventory"
                                % (name, cited, prefix))
    return (not problems, str(problems)[:400] if problems
            else "M20 and G-R require every ID in every inventory, with no range and no orphan")


check("crossdoc", "M20 and G-R require the whole assurance inventory, not a range",
      normative_gates_require_the_whole_inventory)


def no_normative_document_cites_an_orphan_assurance_id():
    inventories = assurance_inventories()
    known = set()
    for v in inventories.values():
        known |= v
    problems = []
    # A backticked RANGE is never a valid requirement - Rule T-15 forbids ranges outright, and
    # the gate check above rejects one in M20 or G-R. Stripping them here lets a document
    # describe the stale form it replaced without that description reading as a citation.
    quoted_range = re.compile(r"`[AIPS]\d+\s*[–-]\s*[AIPS]?\d+`")
    for name in NORMATIVE_DOCS:
        for i, line in enumerate(spec(name).splitlines(), 1):
            scanned = quoted_range.sub(" ", line)
            for cited in re.findall(r"\b(P-A\d+[a-z]?|A\d+[a-z]?|I\d+|P\d+|S\d+)\b", scanned):
                if cited not in known:
                    problems.append("%s:%d cites orphan %s" % (name, i, cited))
    return (not problems, str(problems)[:300] if problems
            else "no normative document cites an assurance ID that does not exist")


check("crossdoc", "no normative document cites an orphan assurance ID",
      no_normative_document_cites_an_orphan_assurance_id)


WORD_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "twenty-one": 21, "twenty-two": 22, "twenty-three": 23, "twenty-four": 24,
    "twenty-five": 25, "thirty": 30, "thirty-one": 31, "thirty-two": 32, "thirty-three": 33,
    "thirty-four": 34, "thirty-five": 35, "thirty-six": 36, "forty": 40,
}


def every_normative_count_matches_its_canonical_inventory():
    """All count-bearing locations, not "at least one correct occurrence" somewhere.

    The V3 audit mutated a localized milestone count and this harness passed, because a
    different correct count survived elsewhere. Every occurrence is checked, in digits and in
    word form, against the value derived from the owning table."""
    derived = {
        "uniqueness constraints": len(uniqueness_ids()),
        "governed commands": len(command_rows()),
        "adversarial tests": len(assurance_inventories()["A"]),
        "positive controls": len(assurance_inventories()["P-A"]),
        # The V4 miss was a stale count of the transaction table itself, restated in a
        # historical narrative row. Both of its sizes are derived here so that a document
        # cannot quote either one from memory.
        "transaction acts": len(transaction_rows()),
        "transaction branch rows": len(transaction_branch_rows()),
    }
    subjects = {
        "uniqueness constraints": r"(?:durable\s+)?uniqueness constraints",
        # Plural only: a total is always plural, while "one governed act" and "a class-4
        # governed act" are singular and are not claims about the size of the inventory.
        "governed commands": r"governed commands|governed acts",
        "adversarial tests": r"adversarial tests|adversarial cases",
        "positive controls": r"positive controls",
    }
    number = r"(\d+|[a-z]+(?:-[a-z]+)?)"
    problems = []

    def value_of(token):
        if token.isdigit():
            return int(token)
        return WORD_NUMBERS.get(token)

    def claims(line, raw):
        """Count claims in one line, as (stated, subject).

        Two forms are checked, and only these two, because a document legitimately says things
        like "the four blocked acts" or "one governed act" in passing. A claim about the SIZE
        OF AN INVENTORY is written either in bold - the convention this package uses for a
        derived total - or inside a milestone or gate row, where partial counts do not occur."""
        low = flat(line)
        bolded = set(re.findall(r"\*\*(\d+|[a-z]+(?:-[a-z]+)?)\*\*\s+[^|]{0,40}", raw))
        in_gate = bool(re.match(r"\|\s*\*\*(M\d+|G-[A-Z])\*\*\s*\|", raw))
        found = []
        for subject, expr in subjects.items():
            for m in re.finditer(number + r"\s+(?:named\s+|committed\s+|durable\s+)?(?:"
                                 + expr + r")", low):
                token = m.group(1)
                if value_of(token) is None:
                    continue                          # "every", "each", "the" - not a count
                bold_here = re.search(r"\*\*" + re.escape(token) + r"\*\*\s+[^|]{0,60}?"
                                      + expr, flat(raw.replace("*", "\x00"))) is not None
                marked = ("**%s**" % token) in raw or ("**%s**" % token.capitalize()) in raw
                if in_gate or marked or bold_here or token in bolded:
                    found.append((token, subject))
        return found

    #: A count can sit on either side of its subject. "**23** uniqueness constraints" is caught
    #: by `claims` above; "the canonical uniqueness inventory (currently **21**)" and a table
    #: row "| Governed commands | **seventeen** |" are not, and both are exactly the localized
    #: form the V3 audit mutated. Each subject therefore declares its trailing forms too.
    #: Patterns are matched against `flat(line)`, which has already stripped emphasis - so they
    #: must not require asterisks. That detail is why the first version of these patterns
    #: matched nothing, and the fixture said so.
    trailing = {
        "uniqueness constraints": (
            r"uniqueness inventory[^|]{0,60}?currently\s+([\w-]+)",
            r"u1[–-]u(\d+)",
        ),
        "governed commands": (
            r"\|\s*governed commands\s*\|\s*([\w-]+)",
        ),
        "adversarial tests": (
            r"adversarial\s*\(([\w-]+)\)",
        ),
        "positive controls": (
            r"positive controls\s*\(([\w-]+)\)",
        ),
    }

    #: Forms the two generic passes above cannot see, because the subject is not the phrase
    #: they key on. Each is a shape the specification actually uses, and the first three are
    #: exactly the V4 miss: a historical row restating "35 numbered commands" and
    #: "§7.2 has 35 rows" while every canonical inventory stayed correct.
    explicit = (
        (r"([\w-]+) numbered (?:governed )?commands", "governed commands"),
        (r"(?:§\s*)?7\.2 (?:now )?has ([\w-]+) rows", "transaction branch rows"),
        (r"transaction table (?:now )?has ([\w-]+) rows", "transaction branch rows"),
        (r"([\w-]+) branch rows", "transaction branch rows"),
        (r"([\w-]+) transaction acts", "transaction acts"),
        (r"([\w-]+) governed acts, keyed", "transaction acts"),
        (r"\|\s*adversarial tests\s*\|\s*([\w-]+)", "adversarial tests"),
        (r"\|\s*positive controls\s*\|\s*([\w-]+)", "positive controls"),
        (r"\|\s*durable uniqueness constraints\s*\|\s*([\w-]+)", "uniqueness constraints"),
    )

    for name in REQUIRED_DOCS:
        lines = spec(name).splitlines()
        for i, line in enumerate(lines, 1):
            for stated, subject in claims(line, line):
                expected = derived[subject]
                value = value_of(stated)
                if value != expected:
                    problems.append("%s:%d states %s %s, inventory has %d"
                                    % (name, i, stated, subject, expected))
            low = flat(line)
            for subject, patterns in trailing.items():
                expected = derived[subject]
                for pattern in patterns:
                    for stated in re.findall(pattern, low):
                        value = value_of(stated)
                        if value is None:
                            continue
                        if value != expected:
                            problems.append("%s:%d states %s for %s, inventory has %d"
                                            % (name, i, stated, subject, expected))
            for pattern, subject in explicit:
                expected = derived[subject]
                for stated in re.findall(pattern, low):
                    value = value_of(stated)
                    if value is None:
                        continue
                    if value != expected:
                        problems.append("%s:%d states %s for %s, inventory has %d"
                                        % (name, i, stated, subject, expected))
    return (not problems, str(problems)[:400] if problems
            else "every stated count agrees: " +
                 " · ".join("%s %d" % (k, v) for k, v in derived.items()))


check("crossdoc", "every normative count matches its canonical inventory, in digits and words",
      every_normative_count_matches_its_canonical_inventory)


def the_routing_lifecycle_is_one_contract_across_documents():
    api = spec("api-command-contracts.md")
    router = spec("model-router-runtime-contract.md")
    txn = transaction_rows()
    problems = []
    commands = {c for _n, c, _a, _act in command_rows()}
    if "RequestRouting" in commands:
        problems.append("RequestRouting still persists a Routing Request independently")
    if "request_routing" in txn:
        problems.append("a request_routing transaction contract still exists")
    branches = {cells[TXN["branch"]].split()[0] for cells in txn.get("route", [])}
    for expected in ("B1", "B1r", "B2", "B3", "B4s", "B4n"):
        if expected not in branches:
            problems.append("route branch %s is not specified" % expected)
    for cells in txn.get("route", []):
        if cells[TXN["branch"]].split()[0] in ("B1", "B1r"):
            if cells[TXN["audit"]].replace("*", "") != "0":
                problems.append("route B1 writes audit events for an invalid answer")
            if "0" not in cells[TXN["writes"]]:
                problems.append("route B1 does not declare zero governed writes")
    if says("api-command-contracts.md", "the Routing Request becomes durable only inside a "
                                        "validated routing act"):
        problems.append("the durability rule is not stated in the API contract")
    if says("model-router-runtime-contract.md", "one lifecycle, and every branch of it"):
        problems.append("the router contract does not encode the same lifecycle")
    if says("model-router-runtime-contract.md", "there is **no separate command that persists a "
                                                "Routing Request**"):
        problems.append("the router contract does not deny a separate persisting command")
    u6 = [ln for ln in table_rows("persistence-and-transaction-model.md") if "| U6 " in ln]
    if u6 and "submission_ordinal" not in u6[0]:
        problems.append("U6 still forbids a second decision for a re-submitted request")
    return (not problems, str(problems)[:400] if problems
            else "one lifecycle: prospective until validated, four branches, re-submission allowed")


check("crossdoc", "the Routing Request lifecycle is one contract across documents",
      the_routing_lifecycle_is_one_contract_across_documents)


def the_retry_branches_are_complete_and_none_writes_nothing():
    txn = transaction_rows()
    problems = []
    branches = {cells[TXN["branch"]].split()[0] for cells in txn.get("retry", [])}
    for expected in ("R1", "R2", "R2f", "R3", "R3a", "R4", "R6", "R7", "RX"):
        if expected not in branches:
            problems.append("retry branch %s is not specified" % expected)
    for cells in txn.get("retry", []):
        branch = cells[TXN["branch"]].split()[0]
        audit = cells[TXN["audit"]].replace("*", "")
        if not audit.isdigit() or int(audit) < 1:
            problems.append("retry %s writes no audit event" % branch)
        if branch in ("R4", "R6", "RX"):
            writes = flat(cells[TXN["writes"]])
            if "retry_refusal_record" not in writes:
                problems.append("retry %s does not write a refusal record" % branch)
            if "escalat" not in writes:
                problems.append("retry %s does not escalate" % branch)
    if says("orchestrator-runtime-contract.md", "a refused retry is a halt, and a halt is a write"):
        problems.append("O-20 does not state that refusing writes")
    if says("api-command-contracts.md",
            "every retry class has a defined branch, and none of them writes nothing"):
        problems.append("the branch-completeness rule is not stated")
    return (not problems, str(problems)[:400] if problems
            else "%d retry branches, each writing at least one audit event"
                 % len(txn.get("retry", [])))


check("crossdoc", "retry branches are complete and a refusal is a governed write",
      the_retry_branches_are_complete_and_none_writes_nothing)


def model_invocation_is_staged_not_transactional():
    txn = transaction_rows()
    commands = {c: act for _n, c, _a, act in command_rows()}
    problems = []
    for name in ("InvokeModel", "RecordProviderAttemptOutcome", "ReconcileExternalEffect"):
        if name not in commands:
            problems.append("%s is not a governed command" % name)
    intent = txn.get("invoke_model", [])
    if len(intent) != 1:
        problems.append("invoke_model does not have exactly one intent branch")
    else:
        writes = flat(intent[0][TXN["writes"]])
        if "model_result" in writes:
            problems.append("invoke_model writes a Model Result in the intent transaction")
        if "provider_attempt" not in writes or "outbox" not in writes:
            problems.append("invoke_model does not stage an attempt and an outbox row")
    outcome = txn.get("record_provider_attempt_outcome", [])
    if len(outcome) < 2:
        problems.append("the observed-outcome act does not distinguish result from no result")
    recon = txn.get("reconcile_external_effect", [])
    if len(recon) < 2:
        problems.append("reconciliation does not distinguish resolved from still-unknown")
    for phrase, doc in (("a timeout is not proof that nothing happened",
                         "api-command-contracts.md"),
                        ("a timeout is not proof that nothing happened",
                         "model-router-runtime-contract.md"),
                        ("an expired attempt lease reads as unknown, never as not-attempted",
                         "failure-recovery-race-model.md"),
                        ("model invocation is an external effect, staged",
                         "api-command-contracts.md"),
                        ("the invocation is staged, not transactional",
                         "model-router-runtime-contract.md")):
        if says(doc, phrase):
            problems.append("%s: missing %r" % (doc, phrase[:45]))
    if "ATTEMPTED_OUTCOME_UNKNOWN" not in spec("api-command-contracts.md"):
        problems.append("the uncertainty state is not used in the API contract")
    return (not problems, str(problems)[:400] if problems
            else "five stages, four identities, three commands, no local atomicity claimed")


check("crossdoc", "model invocation is staged across transactions, never one local commit",
      model_invocation_is_staged_not_transactional)


def the_audit_field_table_and_matrix_agree():
    body = spec("audit-provenance-observability.md")
    fields = body.split("## 4. The audit event")[1].split("### 4.1")[0]
    problems = []
    for field in ("record_version_before", "record_version_after"):
        row = [ln for ln in fields.splitlines() if field in ln]
        if not row:
            problems.append("%s is not a field of the audit event" % field)
            continue
        if "conditional" not in flat(row[0]):
            problems.append("%s states an unconditional nullability that the matrix contradicts"
                            % field)
        if "mutation_kind" not in flat(row[0]):
            problems.append("%s does not defer to the mutation-kind matrix" % field)
    if says("audit-provenance-observability.md",
            "the matrix in this section is the only statement of nullability"):
        problems.append("the matrix is not declared the single statement")
    return (not problems, str(problems)[:300] if problems
            else "the field table defers to the matrix for both version columns")


check("crossdoc", "the audit field table and the mutation-kind matrix agree",
      the_audit_field_table_and_matrix_agree)


def ba1_fails_closed_in_both_directions():
    """Promotion and governed downgrade are the same uncarded authority, seen from two sides."""
    blocked = spec("open-items-and-blocked-authorities.md")
    problems = []
    ba1 = blocked.split("### BA-1")[1].split("### BA-2")[0]
    if "also blocked: governed downgrade" not in flat(ba1):
        problems.append("BA-1 does not cover governed downgrade")
    if "creates and maps no right" not in flat(ba1):
        problems.append("the downgrade clarification does not deny creating a Right")
    for state in ("SUPERSEDED", "RETRACTED", "REJECTED"):
        if state not in ba1:
            problems.append("the downgrade clause does not name %s" % state)
    tests = spec("test-and-assurance-strategy.md")
    rows = [r for r in adversarial_rows()
            if "downgrade" in flat(r[3]) and "ApplyConsequentStatusChange" in r[1]]
    if not rows:
        problems.append("no adversarial test attacks a governed downgrade")
    elif "NO_APPLICABLE_DECISION_RIGHT" not in rows[0][4]:
        problems.append("the downgrade test does not expect a missing-Right refusal")
    if "both directions" not in flat(tests):
        problems.append("the test strategy does not state the two-directional rule")
    return (not problems, str(problems)[:300] if problems
            else "BA-1 blocks promotion and governed downgrade alike, creating no Right")


check("crossdoc", "BA-1 fails closed for governed downgrade as well as promotion",
      ba1_fails_closed_in_both_directions)



def retry_branch_rows():
    """The §5.6 retry branch table, as cell lists keyed by branch id."""
    body = spec("api-command-contracts.md").split("### 5.6")[1].split("## 6.")[0]
    rows = {}
    for line in body.splitlines():
        if not line.startswith("| **R"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows[cells[0].strip("*").split()[0]] = cells
    return rows


def routing_outcome_rows():
    """Rule Q-17b: non-selection outcome -> (run state written, s, posture, wait)."""
    body = spec("api-command-contracts.md").split("**Rule Q-17b")[1].split("**Rule Q-17c")[0]
    rows = {}
    for line in body.splitlines():
        m = re.match(r"^\|\s*`(\w+)`\s*\|(.+?)\|\s*\**(\d+)\**\s*\|(.+?)\|(.+?)\|\s*$", line)
        if m:
            rows[m.group(1)] = (m.group(2).strip(), int(m.group(3)),
                                m.group(4).strip(), m.group(5).strip())
    return rows


def the_routing_run_state_consequence_is_atomic_and_complete():
    """A durable non-selection decision never leaves the run eligible to continue.

    The V4 audit's first blocker: B3 and B4 committed a decision while the run-state
    consequence lived in prose, and nothing said what an invalid answer does once a request is
    already durable. This parses the outcome mapping, the branch table and the commit table and
    compares them to each other rather than looking for a sentence."""
    problems = []
    outcomes = routing_outcome_rows()
    expected_outcomes = {"NO_ELIGIBLE_MODEL": 1, "CANDIDATE_UNIVERSE_INCOMPLETE": 2,
                         "NO_APPLICABLE_DECISION_RIGHT": 2, "ACT_REQUIREMENT_OUTSTANDING": 1}
    for outcome, appends in expected_outcomes.items():
        if outcome not in outcomes:
            problems.append("Q-17b does not map %s to a run-state consequence" % outcome)
            continue
        state, s_value, posture, wait = outcomes[outcome]
        if s_value != appends:
            problems.append("Q-17b gives %s s=%d, not %d" % (outcome, s_value, appends))
        if not state.strip("* "):
            problems.append("Q-17b writes no run state for %s" % outcome)
        if outcome == "ACT_REQUIREMENT_OUTSTANDING":
            if "WAITING_FOR_" not in wait:
                problems.append("Q-17b does not name an approved wait reason for %s" % outcome)
            if "WAITING" not in state:
                problems.append("Q-17b does not put the run in WAITING for %s" % outcome)
        else:
            if "BLOCKED" not in state:
                problems.append("Q-17b does not block the run for %s" % outcome)
            if "GATE_UNSATISFIED" not in posture and "AUTHORITY_ABSENT" not in posture:
                problems.append("Q-17b carries no halted posture for %s" % outcome)
    # The approved wait-reason vocabulary is five values and Phase 14 creates no sixth.
    approved_waits = {"WAITING_FOR_DEPENDENCY", "WAITING_FOR_REVIEW", "WAITING_FOR_DECISION",
                      "WAITING_FOR_HUMAN", "WAITING_FOR_EXTERNAL_EVENT"}
    for doc in ("api-command-contracts.md", "orchestrator-runtime-contract.md",
                "model-router-runtime-contract.md", "persistence-and-transaction-model.md"):
        for found in set(re.findall(r"`(WAITING_FOR_\w+)`", spec(doc))):
            if found not in approved_waits:
                problems.append("%s invents the wait reason %s" % (doc, found))

    txn = transaction_rows().get("route", [])
    by_branch = {cells[TXN["branch"]].split()[0]: cells for cells in txn}
    for branch in ("B3", "B4n"):
        cells = by_branch.get(branch)
        if cells is None:
            problems.append("the transaction table has no %s branch" % branch)
            continue
        writes = flat(cells[TXN["writes"]])
        if "run state" not in writes:
            problems.append("%s commits a decision with no run-state write" % branch)
        if "s" not in cells[TXN["audit"]].replace("*", "").replace(" ", ""):
            problems.append("%s states a fixed audit count for a variable consequence" % branch)
    b1r = by_branch.get("B1r")
    if b1r is None:
        problems.append("there is no contract for an invalid answer after a durable request")
    else:
        writes = flat(b1r[TXN["writes"]])
        if "not advanced" not in writes and "not advance" not in writes:
            problems.append("B1r does not say the submission ordinal is not advanced")
        if "preserved" not in writes:
            problems.append("B1r does not preserve the durable Routing Request")
        if b1r[TXN["audit"]].replace("*", "") != "0":
            problems.append("B1r writes audit events")
    for phrase, doc in (
            ("an invalid answer never disturbs a durable request", "api-command-contracts.md"),
            ("a durable non-selection never leaves the run eligible to continue",
             "api-command-contracts.md"),
            ("b4 inherits b3's consequence, never a weaker one", "api-command-contracts.md"),
            ("an invalid answer leaves a durable request exactly as it found it",
             "model-router-runtime-contract.md"),
            ("the orchestrator effect is deterministic and commits with the decision",
             "model-router-runtime-contract.md")):
        if says(doc, phrase):
            problems.append("%s: missing %r" % (doc, phrase[:45]))
    router_outcomes = spec("model-router-runtime-contract.md").split("### 5.2")[1].split("### 5.3")[0]
    if "blocked` or `escalated" in flat(router_outcomes):
        problems.append("the router leaves the blocked/escalated choice to an implementation")
    router_branches = spec("model-router-runtime-contract.md").split("**Rule M-13 ")[1].split("**Rule M-13d")[0]
    for branch in ("B1r", "B4s", "B4n"):
        if "| " + branch + " |" not in router_branches:
            problems.append("the router branch table omits %s" % branch)
    return (not problems, str(problems)[:400] if problems
            else "B1r preserves the request and the ordinal; B3 and B4n commit their run state "
                 "with the decision; %d outcomes mapped" % len(outcomes))


check("crossdoc", "the routing run-state consequence is atomic and complete",
      the_routing_run_state_consequence_is_atomic_and_complete)


def the_retry_posture_is_a_committed_write():
    """A halted posture asserted only in prose is a posture an implementation may not set."""
    problems = []
    rows = retry_branch_rows()
    for branch in ("R1", "R2", "R2f", "R3", "R3a", "R4", "R6", "R7", "RX"):
        cells = rows.get(branch)
        if cells is None:
            problems.append("§5.6 has no %s row" % branch)
            continue
        if len(cells) < 12:
            problems.append("%s does not state the full branch contract (%d columns)"
                            % (branch, len(cells)))
            continue
        phase, posture, wait, writes = cells[3], cells[4], cells[5], cells[6]
        if "→" not in phase:
            problems.append("%s does not state phase before and after" % branch)
        if "→" not in posture:
            problems.append("%s does not state posture before and after" % branch)
        if not wait.strip("* "):
            problems.append("%s states no wait reason or escalation" % branch)
        if branch in ("R2f", "R4", "R6", "RX"):
            if "GATE_UNSATISFIED" not in posture:
                problems.append("%s does not halt with GATE_UNSATISFIED" % branch)
            if "GATE_UNSATISFIED" not in writes:
                problems.append("%s leaves its halted posture out of its exact writes" % branch)
        if branch == "R3" and "WAITING_FOR_HUMAN" not in wait:
            problems.append("R3 does not name its wait reason")
    txn = {cells[TXN["branch"]].split()[0]: cells
           for cells in transaction_rows().get("retry", [])}
    for branch in ("R2f", "R4", "R6", "RX"):
        cells = txn.get(branch)
        if cells is None:
            problems.append("the transaction table has no %s branch" % branch)
        elif "GATE_UNSATISFIED" not in cells[TXN["writes"]]:
            problems.append("%s commits a halt without its posture" % branch)
    if says("api-command-contracts.md", "the posture is a committed field, not a description"):
        problems.append("Q-28a is not stated")
    if says("api-command-contracts.md", "a dispatch occurs only where a dispatch record exists"):
        problems.append("Q-28b is not stated")
    if says("persistence-and-transaction-model.md",
            "a run-state transition is one version append, carrying every axis it"):
        problems.append("P-14g is not stated")
    return (not problems, str(problems)[:400] if problems
            else "%d retry branches, each stating phase, posture, wait and committed writes"
                 % len(rows))


check("crossdoc", "retry branch posture is a committed write, not prose",
      the_retry_posture_is_a_committed_write)


def the_outbox_protocol_is_implementable():
    """An outbox with no identity, no lease and no claim rule is a diagram, not a protocol."""
    body = spec("persistence-and-transaction-model.md")
    section = body.split("## 9. Outbox for external effects")[1].split("## 10.")[0]
    low = flat(section)
    problems = []
    for field in ("outbox_ref", "model_invocation_ref", "provider_attempt_ref",
                  "provider_idempotency_key", "claim_state", "lease_owner",
                  "lease_expires_at", "claim_token", "dispatch_ordinal"):
        if field not in section:
            problems.append("the dispatch item has no %s" % field)
    # The label is not the constraint. This probe came back REDUNDANT against an earlier
    # version of this check, which asked only whether the row existed - so a row reading
    # "O1 | (no constraint required)" passed. Each row's constraint cell is parsed and must
    # name a durable uniqueness on the column it exists to protect.
    declared = {}
    for line in section.splitlines():
        m = re.match(r"^\|\s*(O\d)\s*\|(.+?)\|", line)
        if m:
            declared[m.group(1)] = flat(m.group(2))
    required = {"O1": ("unique", "outbox_ref"),
                "O2": ("unique", "provider_attempt_ref"),
                "O3": ("unique", "provider_idempotency_key"),
                "O4": ("unique", "claim_state", "lease_expires_at")}
    for constraint, tokens in required.items():
        if constraint not in declared:
            problems.append("operational uniqueness constraint %s is not declared" % constraint)
            continue
        for token in tokens:
            if token not in declared[constraint]:
                problems.append("%s does not constrain %s" % (constraint, token))
    for state in ("PENDING", "CLAIMED", "DISPATCHED", "SETTLED", "ABANDONED"):
        if state not in section:
            problems.append("claim state %s is not in the vocabulary" % state)
    for rule in ("P-23", "P-24", "P-25", "P-26", "P-27", "P-28", "P-29", "P-30",
                 "P-31", "P-32"):
        if "Rule " + rule + " " not in section:
            problems.append("%s is not stated in the outbox protocol" % rule)
    for phrase in ("claiming is one atomic conditional update",
                   "at most one valid lease, enforced durably",
                   "the claimant is a named service identity",
                   "an expired lease is a redelivery condition, never a proof",
                   "lease expiry is never evidence that no external effect occurred",
                   "the provider idempotency key is stable and never regenerated",
                   "where the provider deduplicates, redelivery is at-least-once and safe",
                   "there is no safe redispatch after",
                   "no distributed transaction and no exactly-once",
                   "safe redispatch versus mandatory reconciliation, exactly"):
        if flat(phrase) not in low:
            problems.append("the protocol does not state %r" % phrase[:45])
    crashes = section.split("### 9.6")[1] if "### 9.6" in section else ""
    crash_rows = [ln for ln in crashes.splitlines() if ln.startswith("| **")]
    if len(crash_rows) != 4:
        problems.append("the protocol states %d crash points, not four" % len(crash_rows))
    if "compare-and-swap" not in low:
        problems.append("no compare-and-swap semantics are specified")
    for vendor in ("kafka", "rabbitmq", "sqs", "celery", "sidekiq", "pub/sub", "temporal"):
        if vendor in low:
            problems.append("the protocol names the vendor %s" % vendor)
    if says("failure-recovery-race-model.md",
            "the drain protocol is specified once, in persistence"):
        problems.append("the failure model does not defer to the one protocol")
    return (not problems, str(problems)[:400] if problems
            else "stable identity, O1-O4, five claim states, CAS lease, stable key, "
                 "four crash points, redispatch table")


check("crossdoc", "the provider-call outbox protocol is implementable and vendor-free",
      the_outbox_protocol_is_implementable)


def the_outbox_classification_is_one_classification():
    """Operational or governed - one answer, and every audit count derived from it."""
    problems = []
    persistence = spec("persistence-and-transaction-model.md")
    p14d = persistence.split("**Rule P-14d")[1].split("### 7.2")[0]
    outbox_row = [ln for ln in p14d.splitlines() if "outbox" in ln.lower()]
    if not outbox_row:
        problems.append("P-14d does not say whether an outbox row counts")
    elif "operational" not in flat(outbox_row[0]):
        problems.append("P-14d no longer classifies an outbox row as operational")
    for phrase, doc in (("an outbox row is an operational record, never a governed one",
                         "persistence-and-transaction-model.md"),
                        ("operational delivery records produce no audit event",
                         "audit-provenance-observability.md"),
                        ("the outbox row is operational and is not audited",
                         "api-command-contracts.md")):
        if says(doc, phrase):
            problems.append("%s: missing %r" % (doc, phrase[:45]))
    intent = transaction_rows().get("invoke_model", [])
    if len(intent) != 1:
        problems.append("invoke_model does not have exactly one intent branch")
    else:
        writes = intent[0][TXN["writes"]]
        audit = intent[0][TXN["audit"]].replace("*", "").strip()
        governed = [w for w in writes.split(",") if "outbox" not in w.lower()]
        if not audit.isdigit():
            problems.append("the intent branch states no exact audit count")
        elif int(audit) != len(governed):
            problems.append("the intent branch audits %s of %d governed writes"
                            % (audit, len(governed)))
        if "operational" not in flat(writes):
            problems.append("the intent branch does not mark the outbox row operational")
    stage1 = [ln for ln in spec("api-command-contracts.md").splitlines()
              if ln.startswith("| 1 | **Local intent commit**")]
    if not stage1:
        problems.append("the staging table has no stage 1 row")
    elif "| **2** |" not in stage1[0]:
        problems.append("stage 1 in the API contract does not audit two governed writes")
    control = [r for r in adversarial_rows() if r[0] == "P-A41"]
    if control and "3 audit" in control[0][4]:
        problems.append("the positive control still counts the outbox row")
    attack = [r for r in adversarial_rows() if r[0] == "A48"]
    if not attack:
        problems.append("no adversarial test attacks the outbox audit count")
    return (not problems, str(problems)[:400] if problems
            else "operational everywhere; stage 1 writes two governed records and two audits")


check("crossdoc", "the outbox is operational in every document that counts it",
      the_outbox_classification_is_one_classification)


def stages_three_and_four_are_one_transaction():
    """A recovery path for an unreachable state is how the state becomes reachable."""
    api = spec("api-command-contracts.md")
    problems = []
    if says("api-command-contracts.md",
            "stages 3 and 4 are one transaction, so there is no state between them"):
        problems.append("Q-22b is not stated")
    if says("failure-recovery-race-model.md",
            "stages 3 and 4 have no boundary between them"):
        problems.append("the failure model does not agree")
    crash = api.split("**Rule Q-24 ")[1].split("**Rule Q-25")[0]
    for line in crash.splitlines():
        if not line.startswith("|"):
            continue
        low = flat(line)
        if "after stage 3" in low and "before stage 4" in low:
            if "unreachable" not in low:
                problems.append("the crash table still describes a state between stages 3 and 4")
        if "between stages 3 and 4" in low and "unreachable" not in low:
            problems.append("the crash table still recovers from a state that cannot exist")
    stage4 = [ln for ln in api.splitlines() if ln.startswith("| 4 | **Result recording**")]
    if not stage4:
        problems.append("the staging table has no stage 4 row")
    elif "same transaction as stage 3" not in stage4[0]:
        problems.append("stage 4 does not declare the same transaction as stage 3")
    stage_map = spec("failure-recovery-race-model.md")
    row = [ln for ln in stage_map.splitlines() if ln.startswith("| 4 — result recording")]
    if row and "same transaction" not in flat(row[0]):
        problems.append("the stage map does not carry the transaction boundary")
    if not [r for r in adversarial_rows() if r[0] == "A52"]:
        problems.append("no adversarial test attacks the removed crash window")
    return (not problems, str(problems)[:400] if problems
            else "one transaction; the crash table declares the window unreachable")


check("crossdoc", "stages 3 and 4 are one transaction in every document",
      stages_three_and_four_are_one_transaction)


def refusal_events_do_not_break_observational_equality():
    """Equality over governed state, plus exactly the refusal event the contract names."""
    orch = spec("orchestrator-runtime-contract.md")
    problems = []
    o25 = orch.split("**Rule O-25 ")[1].split("**Rule O-25a")[0]
    if "execution-event history must remain" in o25:
        problems.append("O-25 still requires execution-event history to be identical")
    if "not stated over the total execution-event count" not in flat(o25):
        problems.append("O-25 does not exclude the execution-event count from equality")
    if "governed" not in flat(o25):
        problems.append("O-25 does not state equality over governed state")
    for phrase, doc in (
            ("a refusal execution event is permitted, and is never evidence",
             "orchestrator-runtime-contract.md"),
            ("how a test asserts this", "orchestrator-runtime-contract.md"),
            ("two assertions, never one conflated", "test-and-assurance-strategy.md")):
        if says(doc, phrase):
            problems.append("%s: missing %r" % (doc, phrase[:45]))
    o25a = orch.split("**Rule O-25a")[1].split("**Rule O-25b")[0]
    for denial in ("governance evidence", "authority"):
        if denial not in flat(o25a):
            problems.append("O-25a does not deny a refusal event %s" % denial)
    tests = spec("test-and-assurance-strategy.md")
    preamble = tests.split("## 3. Adversarial tests")[1].split("| Column |")[0]
    if "event count" in flat(preamble) and "governed" not in flat(preamble):
        problems.append("the adversarial preamble still demands total event-count equality")
    for row in adversarial_rows():
        expected = flat(row[4])
        if "execution-event count" in expected and "identical" in expected:
            problems.append("%s requires execution-event-count equality" % row[0])
        if "execution event count" in expected and "equal" in expected:
            problems.append("%s requires execution-event-count equality" % row[0])
    return (not problems, str(problems)[:400] if problems
            else "equality is governed state and governed history; the refusal event is "
                 "asserted separately and is never evidence")


check("crossdoc", "a required refusal event never contradicts observational equality",
      refusal_events_do_not_break_observational_equality)


#: Commands this package once had and deliberately removed. A document may say a removed
#: command is gone; none may present it as a member of a current inventory.
OBSOLETE_COMMANDS = ("RequestRouting", "RecordApprovalState")

#: Phrases that deny present membership. A line carrying one is recording the removal, which
#: is exactly what these documents are supposed to do.
REMOVAL_DENIALS = (
    "no longer exists", "was removed", "is removed", "not a member of any current inventory",
    "removed in revision", "no longer a governed command", "there is no separate command",
    "was, and why it is now two commands",
)

#: Phrases that turn a mention into a claim of present membership.
CURRENCY_CLAIMS = (
    "now has a full contract", "has a full contract", "is now the canonical",
    "now the canonical governed-command inventory", "numbered commands",
    "current inventory", "the inventory holds", "each with exactly one transaction contract",
)


def no_obsolete_command_is_claimed_as_current():
    """The exact V4 miss: a stale narrative row restating a removed command and old totals.

    The canonical inventories were correct; a historical row was not; and nothing compared the
    two. This derives the current command set from §5.1 and fails any line that both names a
    removed command and makes a claim of present membership."""
    current = {c for _n, c, _a, _act in command_rows()}
    problems = []
    for obsolete in OBSOLETE_COMMANDS:
        if obsolete in current:
            problems.append("%s is back in the canonical inventory" % obsolete)
    for name in REQUIRED_DOCS:
        for i, line in enumerate(spec(name).splitlines(), 1):
            low = flat(line)
            if any(d in low for d in REMOVAL_DENIALS):
                continue
            for obsolete in OBSOLETE_COMMANDS:
                if obsolete.lower() not in low:
                    continue
                claimed = [c for c in CURRENCY_CLAIMS if c in low]
                if claimed:
                    problems.append("%s:%d presents %s as current (%r)"
                                    % (name, i, obsolete, claimed[0][:34]))
    if says("api-command-contracts.md", "`RequestRouting` no longer exists"):
        problems.append("the API contract does not record that RequestRouting was removed")
    return (not problems, str(problems)[:400] if problems
            else "%d removed commands, none presented as a member of the %d-command inventory"
                 % (len(OBSOLETE_COMMANDS), len(current)))


check("crossdoc", "no removed command is presented as a current inventory member",
      no_obsolete_command_is_claimed_as_current)


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
