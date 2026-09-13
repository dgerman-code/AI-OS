#!/usr/bin/env python3
"""Phase 11 Orchestrator architecture validation.

Architecture-validation tooling. Reads the repository's markdown and asserts properties of
it. Implements no part of AI-OS: no orchestrator, queue, worker, scheduler, event bus, state
machine service, schema, client, credential or runtime.

Usage:
    python3 validation/phase_11_validation.py [--verbose] [--json]

Exit code 0 if every check passes, 1 otherwise.
"""

import html
import itertools
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The Phase 10 human-approval record. Everything at or before it is upstream and immutable.
PHASE10_BASELINE = "eb789263b4dcc7c4a966a19359522173c57ac8ec"

UPSTREAM_PATHS = {
    "Phase 3 Roles": ["roles/"],
    "Phase 4 Skills": ["skills/", "architecture/skill-registry-design.md",
                       "architecture/role-to-skill-mapping-rules.md"],
    "Phase 5 Workflows": ["workflows/", "architecture/workflow-registry-design.md"],
    "Phase 6 Handoff/Review": ["handoffs/", "architecture/handoff-review-registry-design.md",
                               "reviews/_standards/", "reviews/_templates/",
                               "reviews/master-review-profile-universe.md", "reviews/exemplars/"],
    "Phase 7 Decisions": ["decisions/", "architecture/decision-rights-registry-design.md"],
    "Phase 8 Knowledge": ["knowledge/", "architecture/memory-canonical-governance.md"],
    "Phase 9 Models/Routing": ["models/", "architecture/model-registry-router.md"],
    "Phase 10 Storage": ["storage/", "architecture/storage-persistence-architecture.md"],
    "Phase 9/10 approval records": ["reviews/phase-9-final-approval.md",
                                    "reviews/phase-10-final-approval.md"],
    "Phase 8/9/10 validators": ["validation/phase_8_validation.py",
                                "validation/phase_9_validation.py",
                                "validation/phase_10_validation.py"],
    "Inherited Phase 2/3 architecture": ["architecture/context-hierarchy.md",
                                         "architecture/project-criticality-policy.md",
                                         "architecture/registry-separation.md",
                                         "architecture/system-principles.md"],
}


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def plain(text):
    """Strip markdown emphasis: checks test what a sentence says, not how it is styled."""
    return text.replace("**", "").replace("`", "")


def discover(subdir, suffix=".md"):
    """Walk the tree. Never enumerate: a new artifact is covered automatically and cannot
    pass by being absent from a hand-written list."""
    out = []
    for root, _dirs, files in os.walk(os.path.join(REPO, subdir)):
        for name in sorted(files):
            if name.endswith(suffix):
                out.append(os.path.relpath(os.path.join(root, name), REPO))
    return sorted(out)


def git_unchanged(paths):
    diff = subprocess.run(["git", "diff", "--name-only", PHASE10_BASELINE, "HEAD", "--"] + paths,
                          cwd=REPO, capture_output=True, text=True)
    status = subprocess.run(["git", "status", "--porcelain", "--"] + paths,
                            cwd=REPO, capture_output=True, text=True)
    changed = [ln for ln in (diff.stdout + status.stdout).splitlines() if ln.strip()]
    return (not changed), changed


ARCH = "architecture/orchestrator-architecture.md"
ORCH_FILES = discover("orchestration")
EXEMPLARS = [f for f in ORCH_FILES if "/exemplars/" in f]
TEMPLATES = [f for f in ORCH_FILES if "/_templates/" in f]
STANDARD = "orchestration/_standards/common-orchestrator-governance-constraints.md"
PHASE11_FILES = ([ARCH] + ORCH_FILES
                 + [f for f in discover("reviews") if "phase-11" in f])

DOCS = {rel: read(rel) for rel in PHASE11_FILES}
NORMATIVE = {rel: doc for rel, doc in DOCS.items() if not rel.startswith("reviews/")}

# A denial marker suppresses a scan hit ONLY on the hit's own line. Phase 10's audit proved a
# wide context window is no filter at all: prose about what an architecture refuses is dense
# with denial words, so anything injected nearby inherits their cover.
DENIAL_MARKER = re.compile(
    r"\bnever\b|\bno\b|\bnot\b|\bcannot\b|must not|prohibit|refus|forbid|"
    r"would have|rejected|instead of|rather than|defect|denie|denial", re.I)


def line_of(text, index):
    """The single line containing `index` - the only context a denial marker may reach."""
    start = text.rfind("\n", 0, index) + 1
    end = text.find("\n", index)
    return text[start:end if end != -1 else len(text)]


A = DOCS[ARCH]
RUN = DOCS["orchestration/execution-run-model.md"]
STATE = DOCS["orchestration/state-machine-and-transitions.md"]
SCHED = DOCS["orchestration/scheduling-and-dependency-model.md"]
GATE = DOCS["orchestration/human-gate-and-decision-invocation.md"]
ROUTE = DOCS["orchestration/model-router-invocation-boundary.md"]
RETRY = DOCS["orchestration/retry-replay-idempotency.md"]
RACE = DOCS["orchestration/concurrency-and-race-governance.md"]
FAILD = DOCS["orchestration/failure-escalation-recovery.md"]
MANUAL = DOCS["orchestration/manual-intervention-boundary.md"]
AUDIT = DOCS["orchestration/execution-audit-and-provenance.md"]
INDEP = DOCS["orchestration/provider-runtime-independence.md"]
STD = DOCS[STANDARD]
TMPL = {os.path.basename(t): DOCS[t] for t in TEMPLATES}

RESULTS = []


def check(group, name, fn):
    try:
        outcome = fn()
    except Exception as exc:
        outcome = (False, "ERROR: %s: %s" % (type(exc).__name__, exc))
    if isinstance(outcome, tuple):
        ok, evidence = outcome
    else:
        ok, evidence = bool(outcome), ""
    RESULTS.append({"group": group, "name": name, "pass": bool(ok), "evidence": str(evidence)})


# =========================================================== identity separation

SEPARATED = ["ROLE", "AGENT INSTANCE", "MODEL", "MODEL PROFILE", "ROUTER", "ORCHESTRATOR",
             "WORKFLOW", "WORKFLOW RUN", "TASK", "HANDOFF", "REVIEW PROFILE", "REVIEW INSTANCE",
             "DECISION RIGHT", "DECISION RECORD", "KNOWLEDGE", "CANONICAL RECORD", "ARTIFACT",
             "STORAGE RECORD", "RUNTIME EVENT", "CREDENTIAL", "HUMAN AUTHORITY"]

check("identity", "full twenty-one-object separation chain stated verbatim",
      lambda: (" != ".join(SEPARATED) in plain(A), "%d objects" % len(SEPARATED)))


def denial_table_has_consequences():
    """Each listed collapse must be denied with what collapsing it would destroy."""
    body = A.split("The collapses Phase 11 is most exposed to")[1].split("## 3.")[0]
    rows = [ln for ln in body.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)][1:]
    empty = [r for r in rows if len(plain(r.split("|")[2]).strip()) < 20]
    return (len(rows) >= 9 and not empty,
            "%d denials, %d without a stated consequence" % (len(rows), len(empty)))


check("identity", "each named collapse is denied with its consequence", denial_table_has_consequences)

CORE_DENIALS = ["ROLE != AGENT INSTANCE", "ROUTER != ORCHESTRATOR", "WORKFLOW != WORKFLOW RUN",
                "REVIEW PROFILE != REVIEW INSTANCE", "DECISION RIGHT != DECISION RECORD",
                "RUNTIME EVENT != AUDIT EVENT", "ORCHESTRATOR != HUMAN AUTHORITY",
                "CREDENTIAL != HUMAN AUTHORITY"]
check("identity", "the eight load-bearing collapses are each denied individually",
      lambda: (lambda missing: (not missing, str(missing) if missing else "8 denials"))(
          [d for d in CORE_DENIALS if d not in plain(A)]))

check("identity", "a Role is activated, never instantiated as an agent",
      lambda: ("An assignment is not an agent" in plain(STD)
               and "No execution creates a persistent persona" in plain(STD)
               and "not a persona created" in plain(RUN), ""))

check("identity", "no seniority variants of a Role are created",
      lambda: ("No seniority variants" in plain(RUN)
               and "junior, middle or senior" in plain(RUN), ""))

check("identity", "a runtime identifier is never a governance identity",
      lambda: ("A runtime identifier is not a governance identity" in plain(STD)
               and "A runtime identifier is never a governance identity" in plain(RUN), ""))


def orchestrator_is_not_router():
    return ("ROUTER != ORCHESTRATOR" in plain(A)
            and "The orchestrator is not the Router" in plain(STD)
            and "Two questions, two components" in plain(ROUTE), "")


check("identity", "orchestrator and router remain two components", orchestrator_is_not_router)

# =========================================================== authority boundary


def may_may_not_table():
    body = A.split("| It may | It may never |")[1].split("## 2.")[0]
    return [ln for ln in body.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)]


check("authority", "the may / may-never table is populated on both sides",
      lambda: (lambda rows: (len(rows) >= 12 and all(len(r.strip().strip("|").split("|")) == 2
                                                     for r in rows),
                             "%d rows" % len(rows)))(may_may_not_table()))

FORBIDDEN_POWERS = {
    "approve": r"(?i)orchestrator [^.\n]{0,40}\bmay approve\b",
    "review": r"(?i)orchestrator [^.\n]{0,40}\bmay (satisfy|perform) (a )?review",
    "canonicalize": r"(?i)orchestrator [^.\n]{0,40}\bmay (promote|canonicali)",
    "accept risk": r"(?i)orchestrator [^.\n]{0,40}\bmay accept (a )?risk",
    "exercise a Right": r"(?i)orchestrator [^.\n]{0,40}\bmay exercise\b",
    "sign": r"(?i)orchestrator [^.\n]{0,40}\bmay sign\b",
}


def orchestrator_claims_no_authority():
    bad = []
    for rel, doc in DOCS.items():
        flat = plain(doc)
        for label, pat in FORBIDDEN_POWERS.items():
            for m in re.finditer(pat, flat):
                if DENIAL_MARKER.search(line_of(flat, m.start())):
                    continue
                bad.append("%s: %s (%s)" % (rel, m.group(0)[:60], label))
    return (not bad, str(bad) if bad
            else "0 statements granting the orchestrator a governed power")


check("authority", "no artifact grants the orchestrator a governed power",
      orchestrator_claims_no_authority)

check("authority", "completion is not approval, stated normatively",
      lambda: ("Completion is not approval" in plain(STD)
               and "Completion is not approval" in plain(STATE)
               and "no quantity of finished work becomes one" in plain(STD), ""))

check("authority", "absence of a Decision Right is never permission",
      lambda: ("Absence of a Decision Right is not permission" in plain(STD)
               and "block and escalate" in plain(STD).lower()
               and "Carding a Right is a Phase 7 act" in plain(GATE), ""))

check("authority", "a timeout is never an approval",
      lambda: ("A timeout is never an approval" in plain(STD)
               and "Silence is not assent" in plain(STD)
               and "Never an approval" in plain(GATE), ""))

check("authority", "DEFER and ESCALATE never collapse into APPROVE",
      lambda: ("never collapse into" in plain(STD)
               and "are not approvals" in plain(GATE)
               and "no configuration, criticality band, urgency level or policy setting"
               in plain(GATE), ""))

check("authority", "the orchestrator never self-satisfies a gate",
      lambda: ("The orchestrator never self-satisfies a gate" in plain(STD)
               and "It may not be the reviewer, the decider, the signatory or the promoter"
               in plain(STD), ""))

check("authority", "confidence is never authority",
      lambda: ("Confidence is not authority" in plain(STD)
               and "Phase 9 denies this for routing" in plain(STD), ""))

check("authority", "a model result is AI_SUGGESTION and nothing more",
      lambda: ("AI_SUGGESTION" in STD and "ORIGIN: AI_GENERATED" in STD
               and "A model result is a model result" in plain(STD)
               and "A model result is not a completed review" in plain(ROUTE), ""))

check("authority", "possession of a credential grants nothing",
      lambda: ("CREDENTIAL != HUMAN AUTHORITY" in plain(A)
               and "ability to perform an action is not authority to authorise one"
               in plain(MANUAL), ""))

# =========================================================== state model

PHASES = ["CREATED", "VALIDATING", "READY", "RUNNING", "WAITING", "PAUSED", "RETRY_PENDING",
          "REWORK_REQUIRED", "BLOCKED", "ESCALATED"]
TERMINALS = ["COMPLETED", "COMPLETED_WITH_OPEN_ITEMS", "CANCELLED", "TERMINATED", "FAILED",
             "SUPERSEDED"]
WAITS = ["WAITING_FOR_DEPENDENCY", "WAITING_FOR_REVIEW", "WAITING_FOR_DECISION",
         "WAITING_FOR_HUMAN", "WAITING_FOR_EXTERNAL_EVENT"]
POSTURES = ["GOVERNANCE_CLEAR", "OPEN_ITEMS_CARRIED", "GATE_UNSATISFIED", "AUTHORITY_ABSENT"]


def axis_rows(heading, stop):
    body = STATE.split(heading)[1].split(stop)[0]
    return [ln for ln in body.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)][1:]


check("state", "four orthogonal axes are declared, not one status enum",
      lambda: ("Four orthogonal axes, not one enum" in plain(STATE)
               and "A single status field would force unrelated facts into one value"
               in plain(STATE), ""))

check("state", "ten run phases parse from the axis table",
      lambda: (lambda rows: (len(rows) == 10 and all(p in STATE for p in PHASES),
                             "%d phases" % len(rows)))(
          axis_rows("## 2. Axis A", "## 3. Axis B")))

check("state", "six terminal outcomes parse, each with a requirement",
      lambda: (lambda rows: (len(rows) == 6 and all(t in STATE for t in TERMINALS)
                             and all(len(r.strip().strip("|").split("|")) == 3 for r in rows),
                             "%d terminals" % len(rows)))(
          axis_rows("## 3. Axis B", "## 4. Axis C")))

check("state", "five wait reasons, each required to name its subject",
      lambda: (all(w in STATE for w in WAITS)
               and "A wait with no named subject is a defect" in plain(STATE),
               "%d wait reasons" % len(WAITS)))

check("state", "four governance postures parse, with their permitted terminals",
      lambda: (lambda rows: (len(rows) == 4 and all(p in STATE for p in POSTURES),
                             "%d postures" % len(rows)))(
          axis_rows("## 5. Axis D", "## 6. Transitions")))


def completion_requires_clear_posture():
    """COMPLETED must require GOVERNANCE_CLEAR; open items must require an upstream rule."""
    rows = axis_rows("## 3. Axis B", "## 4. Axis C")
    problems = []
    for r in rows:
        cells = [plain(c).strip() for c in r.strip().strip("|").split("|")]
        if cells[0] == "COMPLETED" and "GOVERNANCE_CLEAR" not in cells[2]:
            problems.append("COMPLETED does not require GOVERNANCE_CLEAR")
        if cells[0] == "COMPLETED_WITH_OPEN_ITEMS":
            if "OPEN_ITEMS_CARRIED" not in cells[2] or "upstream rule" not in cells[2]:
                problems.append("open-items completion lacks an upstream-rule requirement")
    if "No completion" not in plain(STATE):
        problems.append("unsatisfied postures do not forbid completion")
    return (not problems, str(problems) if problems
            else "completion is gated on posture, not on stages finishing")


check("state", "completion requires a clear posture, never merely finished stages",
      completion_requires_clear_posture)


def no_timeout_to_completion_edge():
    """There must be no transition from waiting to a terminal success on expiry."""
    body = STATE.split("## 6. Transitions")[1].split("### 6.1")[0]
    bad = []
    for ln in body.splitlines():
        if not ln.startswith("| "):
            continue
        cells = [plain(c).strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[0] in ("WAITING", "PAUSED", "BLOCKED", "ESCALATED"):
            if re.search(r"\bCOMPLETED\b", cells[1]):
                bad.append("%s may reach COMPLETED directly" % cells[0])
    if "WAITING` → `COMPLETED` on timeout" not in STATE:
        bad.append("the non-existent timeout edge is not stated as absent")
    if "There is no such edge" not in plain(STATE):
        bad.append("the timeout edge is not explicitly denied")
    return (not bad, str(bad) if bad else "no waiting-or-blocked state reaches completion")


check("state", "no waiting, paused or blocked state may reach completion",
      no_timeout_to_completion_edge)

check("state", "terminal outcomes have no outgoing transitions",
      lambda: ("Terminal outcomes have no outgoing transitions" in plain(STATE)
               and "never by reopening it" in plain(STATE), ""))

check("state", "a blocked run is not resumed by retry",
      lambda: ("Retry re-executes a step" in plain(STATE)
               and "it does not satisfy a constraint" in plain(STATE), ""))

check("state", "stage and run postures compose strictly",
      lambda: ("The run's posture is the strictest posture of its open parts" in plain(STATE),
               ""))

# =========================================================== scope isolation

SCOPES = ["organisation", "programme", "portfolio", "project", "product", "workstream",
          "PERSONAL"]
check("scope", "every scope boundary the orchestrator may not cross is named",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d boundaries" % len(SCOPES)))(
          [s for s in SCOPES if s not in plain(STD)]))

check("scope", "each execution binds to exactly one governed scope",
      lambda: ("Every execution binds to exactly one governed scope" in plain(STD)
               and "Bound at intake, before any work" in plain(STD)
               and "A change is a new run" in plain(RUN), ""))

check("scope", "cross-scope movement requires an approved mechanism",
      lambda: ("A cross-scope movement uses an approved mechanism or does not happen"
               in plain(STD)
               and "There is no orchestrator-level shortcut" in plain(STD), ""))

check("scope", "a sub-run may narrow but never widen scope",
      lambda: ("It may not widen it" in plain(RUN)
               and "a scope crossing wearing a different name" in plain(RUN), ""))

check("scope", "scope mismatch is a stop condition",
      lambda: ("Scope mismatch" in FAILD and "never a silent transfer" in plain(FAILD), ""))


# A sentence about crossing a scope is read by its PREDICATE, not by the words it happens to
# contain. The previous check exempted any line containing `approved mechanism`, so
# "a stage may cross a project boundary without an approved mechanism" passed on the strength
# of the very phrase it was dispensing with - the same substring-coincidence failure that this
# suite has now hit in three different invariants.
CROSSING = re.compile(r"cross(?:es|ing|ed)?\b[^.;\n]{0,40}?\b(?:scope|boundar(?:y|ies))", re.I)
# Scope crossing is validated by a CONTROLLED NORMATIVE GRAMMAR, not by understanding English.
# Three earlier readings tried to classify open-ended modality, qualification and connective
# vocabulary, and each was bypassed by wording nobody had enumerated ("pending operator
# approval", "consequently", "whereby"). Normative Phase 11 prose is controlled input, so the
# validator now accepts only constructions it can consume ENTIRELY, and rejects everything
# else. A false rejection of non-canonical wording is a cost the corpus can pay; a silent
# authorisation is not.
#
# A crossing SPAN is bounded by sentence punctuation, table cell walls, and a coordinated
# NEGATIVE continuation - a coordinate that begins with a negation cannot grant permission,
# which is what lets "Never cross a scope boundary, and never widen where material may go"
# and "A cross-scope movement uses an approved mechanism or does not happen" stand as written.
SPAN_BREAK = re.compile(
    r"[.;|\n]|(?:,\s*)?\b(?:and|or|nor)\s+"
    r"(?:(?:does|do|did|is|are|was|were|can|will|shall|would|could|may|must|has|have|had)\s+)?"
    r"(?:never|not|no|neither|nothing)\b", re.I)

SCOPE_WORD = (r"(?:scope|project|programme|program|portfolio|product|workstream|organisation|"
              r"organization|team|tenant|personal)")
CROSS_OBJECT = r"(?:a|an|the|any|each|every|that|this)?\s*(?:%s\s+)?boundar(?:y|ies)" % SCOPE_WORD
CROSS_SUBJECT = (r"(?:a|an|the|any|each|every|no)?\s*"
                 r"(?:sub-run|run|stage|orchestrator|workflow\s+run|workflow|execution|task|"
                 r"work\s+item|movement|coordinator|router)")
CANON_PROHIBITIVE = (
    r"(?:must\s+not|must\s+never|may\s+not|may\s+never|cannot|can\s*not|can't|can\s+never|"
    r"shall\s+not|shall\s+never|will\s+not|will\s+never|would\s+not|does\s+not|do\s+not|"
    r"is\s+not\s+permitted\s+to|are\s+not\s+permitted\s+to|is\s+not\s+allowed\s+to|"
    r"are\s+not\s+allowed\s+to|is\s+forbidden\s+to|are\s+forbidden\s+to|never)")
CANON_PERMISSIVE = (
    r"(?:may|can|could|might|shall|will|must|is\s+permitted\s+to|are\s+permitted\s+to|"
    r"is\s+allowed\s+to|are\s+allowed\s+to)")
# The mechanism must be BOUND to the crossing by one of these local relations. A mechanism
# reached any other way - a neighbouring proposition, a trailing remark - is not a binding.
MECHANISM_BINDER = r"(?:only\s+)?(?:through|via|using|under|by\s+means\s+of|by)"
CANON_MECHANISM_NP = (
    r"(?:a|an|the)?\s*(?:approved\s+)?(?:phase\s+\d+\s+)?"
    r"(?:scope\s+transfer|handoff|approved\s+mechanism)")
CANON_NOMINAL_CROSSING = r"(?:a|an|the)?\s*cross-scope\s+(?:movement|transfer)"
CANON_NOMINAL_BINDER = (r"(?:uses|happens\s+through|occurs\s+through|is\s+made\s+through|"
                        r"takes\s+place\s+through)")

CANON_PROHIBITION = re.compile(
    r"\s*(?:%s\s+)?%s\s+cross(?:es)?\s+%s\s*"
    % (CROSS_SUBJECT, CANON_PROHIBITIVE, CROSS_OBJECT), re.I)
CANON_PROHIBITION_FROM = re.compile(
    r"\s*%s\s+(?:is|are)\s+(?:prohibited|barred|precluded)\s+from\s+crossing\s+%s\s*"
    % (CROSS_SUBJECT, CROSS_OBJECT), re.I)
CANON_MECHANISM_BOUND = re.compile(
    r"\s*%s\s+(?:%s\s+)?cross(?:es)?\s+%s\s+%s\s+%s\s*"
    % (CROSS_SUBJECT, CANON_PERMISSIVE, CROSS_OBJECT, MECHANISM_BINDER, CANON_MECHANISM_NP), re.I)
CANON_NOMINAL_MECHANISM = re.compile(
    r"\s*%s\s+%s\s+%s\s*"
    % (CANON_NOMINAL_CROSSING, CANON_NOMINAL_BINDER, CANON_MECHANISM_NP), re.I)
CANON_GERUND_MECHANISM = re.compile(
    r"\s*crossing\s+%s\s+(?:happens|occurs|takes\s+place)\s+%s\s+%s\s*"
    % (CROSS_OBJECT, MECHANISM_BINDER, CANON_MECHANISM_NP), re.I)


def classify_crossing(span):
    """PROHIBITION_CANONICAL, MECHANISM_BOUND_CANONICAL or UNCLASSIFIED for one crossing span.

    A form counts only when the grammar consumes the WHOLE span. Text left over inside the
    span - a condition, an exception, a purpose, a consequence, a trailing remark - is not
    interpreted, it simply means the construction was not proven safe."""
    text = " ".join(span.split())
    if CANON_PROHIBITION.fullmatch(text) or CANON_PROHIBITION_FROM.fullmatch(text):
        return "PROHIBITION_CANONICAL"
    if (CANON_MECHANISM_BOUND.fullmatch(text) or CANON_NOMINAL_MECHANISM.fullmatch(text)
            or CANON_GERUND_MECHANISM.fullmatch(text)):
        return "MECHANISM_BOUND_CANONICAL"
    return "UNCLASSIFIED"


def crossing_spans(text):
    """(span, classification) for every span of `text` that mentions crossing a scope.

    Discovery reads the SAME rendered-text path the identity invariants use. Reading `plain()`
    let syntax the normaliser already supports hide the predicate: `cr*oss*` and
    `c<!--x-->ross` both render as `cross` to a reader, and were invisible to the scan. There
    is one semantic reader in this file, and every invariant that reads visible text uses it.
    `semantic_text` is defined further down, so the two scope checks that depend on this are
    registered after it rather than here."""
    return [(span, classify_crossing(span))
            for span in SPAN_BREAK.split(semantic_text(text)) if span and CROSSING.search(span)]


def scope_crossing_offences(text):
    """Spans in `text` whose crossing the controlled grammar cannot prove governed.

    Named and shared so the guard can drive the SCAN, not only the classifier: a weakening
    that bypasses the classifier inside the scan is invisible to a guard that calls the
    classifier directly, which is exactly how a reverted exemption once survived."""
    return [" ".join(span.split())[:100]
            for span, verdict in crossing_spans(text) if verdict == "UNCLASSIFIED"]


def no_implicit_scope_crossing():
    """Every scope crossing in normative content parses as a canonical governed construction.

    ALLOW for a canonical unconditional prohibition and for a canonical mechanism-bound
    crossing. REJECT for everything else, unknown wording included."""
    bad = ["%s: %s" % (rel, offence)
           for rel, doc in NORMATIVE.items() for offence in scope_crossing_offences(doc)]
    return (not bad, str(bad) if bad
            else "every scope-crossing span parses as a canonical governed construction")




def controlled_crossing_grammar():
    """The controlled crossing grammar, executed rather than described.

    Every case runs against the real classifier AND the real document scan. The negatives are
    deliberately drawn from vocabulary the grammar does not enumerate anywhere: that is the
    point of a fail-closed parser - it does not need to have seen the words."""
    unclassified = {
        # The v10 bypasses.
        "prohibition with a pending condition":
            "The run must not cross a project boundary pending operator approval.",
        "prohibition with an authorised-case exception":
            "The run is forbidden to cross a project boundary in cases authorised by the "
            "operator.",
        "prohibition with an outside-conditions carve-out":
            "The run never crosses a project boundary outside emergency conditions.",
        "prohibition with a `should` conditional":
            "The run would not cross a scope boundary should the operator request it.",
        "prohibition with an `as long as` condition":
            "The run must not cross a scope boundary as long as the operator remains silent.",
        "permission with a `consequently` consequence":
            "The run may cross a scope boundary consequently a Phase 6 handoff is recorded.",
        "mechanism in an `accordingly` antecedent":
            "A Phase 6 handoff exists accordingly the run may cross a project boundary.",
        "permission with a `whereby` result":
            "The run may cross a scope boundary whereby a Phase 6 handoff is recorded "
            "afterwards.",
        # Independent paraphrases, none of them substitutions from a synonym list.
        "prohibition with a `barring` carve-out":
            "The stage must not cross a scope boundary barring an operator instruction.",
        "prohibition with a `save in` carve-out":
            "The run cannot cross a project boundary save in emergencies.",
        "permission with a promised later handoff":
            "The orchestrator may cross a scope boundary and a handoff will follow eventually.",
        "prohibition with an `until told otherwise` limit":
            "The run is not permitted to cross a scope boundary until told otherwise.",
        "permission justified by a `because` clause":
            "The run may cross a project boundary because a Phase 6 handoff exists.",
        "mechanism in a `therefore` antecedent":
            "A Phase 6 handoff is on file therefore the stage may cross a scope boundary.",
        "prohibition with an `absent` condition":
            "The run never crosses a project boundary absent operator instruction.",
        "permission with a `given ... somewhere` mechanism":
            "The stage may cross a scope boundary given an approved mechanism somewhere.",
        "permission waiving the mechanism outright":
            "The run may cross a scope boundary without an approved mechanism.",
        "unclassifiable permission paraphrase":
            "It falls to the run to cross a project boundary.",
        "mechanism in a neighbouring proposition":
            "An approved mechanism exists, and the orchestrator may cross a scope boundary.",
        "prohibition on another predicate, then a permission":
            "The orchestrator never waits and may cross a scope boundary.",
        # Bare permissions: nothing binds the crossing to a mechanism at all.
        "bare permission": "The run may cross a project boundary.",
        "bare permission, passive": "The stage is permitted to cross a scope boundary.",
        "bare assertion": "The stage crosses a project boundary.",
    }
    prohibition_canonical = {
        "must not cross": "The orchestrator must not cross a scope boundary.",
        "cannot cross": "The run cannot cross a project boundary.",
        "may not cross": "The stage may not cross a scope boundary.",
        "is not permitted to cross": "The run is not permitted to cross a scope boundary.",
        "never crosses": "The run never crosses a project boundary.",
        "is prohibited from crossing": "The run is prohibited from crossing a project boundary.",
        "imperative never cross": "Never cross a scope boundary.",
    }
    mechanism_canonical = {
        "may cross through an approved scope transfer":
            "The run may cross a project boundary through an approved scope transfer.",
        "may cross via a Phase 6 handoff":
            "The stage may cross the scope boundary via a Phase 6 handoff.",
        "may cross only through an approved scope transfer":
            "The run may cross a scope boundary only through an approved scope transfer.",
        "crosses using an approved mechanism":
            "The stage crosses a project boundary using an approved mechanism.",
        "nominal crossing uses an approved mechanism":
            "A cross-scope movement uses an approved mechanism or does not happen.",
        "gerund crossing happens through a handoff":
            "Crossing a project boundary happens through a Phase 6 handoff.",
    }
    problems = []

    def parses(sentence):
        """The classifications the real scan assigns to `sentence`, span by span."""
        return [verdict for _span, verdict in crossing_spans(sentence)]

    for label, sentence in unclassified.items():
        got = parses(sentence)
        if got != ["UNCLASSIFIED"]:
            problems.append("%s: %s, expected UNCLASSIFIED" % (label, got))
    for label, sentence in prohibition_canonical.items():
        if parses(sentence) != ["PROHIBITION_CANONICAL"]:
            problems.append("%s: %s, expected PROHIBITION_CANONICAL" % (label,
                                                                       parses(sentence)))
    for label, sentence in mechanism_canonical.items():
        if parses(sentence) != ["MECHANISM_BOUND_CANONICAL"]:
            problems.append("%s: %s, expected MECHANISM_BOUND_CANONICAL" % (label,
                                                                           parses(sentence)))
    # Two crossings in one sentence, classified independently, in both orders.
    for order, sentence, expected in (
            ("prohibition then bare permission",
             "The run must not cross a scope boundary; the stage may cross a project "
             "boundary.", ["PROHIBITION_CANONICAL", "UNCLASSIFIED"]),
            ("governed crossing then prohibition",
             "The stage may cross a project boundary through a Phase 6 handoff; the run must "
             "not cross a scope boundary.",
             ["MECHANISM_BOUND_CANONICAL", "PROHIBITION_CANONICAL"])):
        if parses(sentence) != expected:
            problems.append("%s: %s, expected %s" % (order, parses(sentence), expected))
    # A prohibition followed by a separate recording statement stays a prohibition.
    separate = ("The run must not cross a project boundary. The refusal is recorded in the "
                "run record.")
    if parses(separate) != ["PROHIBITION_CANONICAL"]:
        problems.append("a separate recording sentence changed a prohibition: %s"
                        % parses(separate))

    # Rendering may change presentation; it may not hide the predicate. Each raw form below
    # must discover exactly what its rendered equivalent discovers, and reverting discovery to
    # `plain()` leaves every one of them undiscovered.
    rendered = {
        "emphasis splitting the verb": "The run may cr*oss* a project boundary.",
        "strong emphasis splitting the verb": "The run may cr**oss** a project boundary.",
        "an HTML comment splitting the verb":
            "The run may c<!--x-->ross a project boundary.",
        "a code span around the verb": "The run may `cross` a project boundary.",
        "an inline HTML tag around the verb":
            "The run may <em>cross</em> a project boundary.",
        "a numeric entity inside the verb": "The run may cr&#111;ss a project boundary.",
        "a Markdown link around the verb":
            "The run may [cross](#anchor-target) a project boundary.",
    }
    plain_form = "The run may cross a project boundary."
    expected_spans = crossing_spans(plain_form)
    for label, raw in rendered.items():
        if crossing_spans(raw) != expected_spans:
            problems.append("%s: discovery differs from the rendered text: %s"
                            % (label, crossing_spans(raw)))
        if not scope_crossing_offences(raw):
            problems.append("%s: formatting hid the crossing from the scan" % label)
    # Rendering must not turn a governed construction into an offence either.
    for label, raw in {
            "prohibition with emphasis":
                "The orchestrator must not cr*oss* a scope boundary.",
            "mechanism-bound crossing with emphasis":
                "The run may cr*oss* a project boundary through an approved scope transfer."
    }.items():
        if scope_crossing_offences(raw):
            problems.append("%s: rendering broke a governed construction" % label)

    # Drive the document SCAN, not only the classifier.
    for label, doc in {
            "bare permission": "## Sub-runs\n\nThe run may cross a project boundary.\n",
            "pending condition":
                "## Sub-runs\n\nThe run must not cross a project boundary pending operator "
                "approval.\n",
            "whereby result":
                "## Sub-runs\n\nThe run may cross a scope boundary whereby a Phase 6 handoff "
                "is recorded afterwards.\n",
            "accordingly antecedent":
                "## Sub-runs\n\nA Phase 6 handoff exists accordingly the run may cross a "
                "project boundary.\n"}.items():
        if not scope_crossing_offences(doc):
            problems.append("the document scan did not reject: %s" % label)
    for label, doc in {
            "canonical prohibition":
                "## Sub-runs\n\nThe orchestrator must not cross a scope boundary.\n",
            "mechanism-bound crossing":
                "## Sub-runs\n\nThe run may cross a scope boundary only through an approved "
                "scope transfer.\n",
            "committed nominal form":
                "## Sub-runs\n\nA cross-scope movement uses an approved mechanism or does not "
                "happen.\n"}.items():
        if scope_crossing_offences(doc):
            problems.append("the document scan rejected governed wording: %s" % label)
    return (not problems, str(problems)[:400] if problems
            else "%d spans classified as specified, and the scan agrees"
                 % (len(unclassified) + len(prohibition_canonical) + len(mechanism_canonical)))


check("scope", "sensitivity and residency are carried and never widened",
      lambda: ("Sensitivity and residency are carried, never relaxed" in plain(STD)
               and "it may never widen where material may go" in plain(STD), ""))


def no_scalar_sensitivity():
    """Phase 8 defines no order over sensitivity classes and Phase 11 introduces none."""
    patterns = [r"MAX_DATA_SENSITIVITY", r"maximum (approved )?(data )?sensitivity",
                r"sensitivity[^.]{0,40}at or above", r"highest[^.]{0,30}sensitivity",
                r"sensitivity (level|ceiling|score|rank)"]
    hits = []
    for rel, doc in DOCS.items():
        flat = plain(doc)
        for pat in patterns:
            for m in re.finditer(pat, flat, re.I):
                if DENIAL_MARKER.search(line_of(flat, m.start())):
                    continue
                hits.append("%s: %s" % (rel, m.group(0)))
    return (not hits, str(sorted(set(hits))) if hits else "0 ordinal sensitivity constructs")


check("scope", "no scalar sensitivity ceiling is introduced", no_scalar_sensitivity)

# =========================================================== scheduling and dependencies


def dispatch_rows():
    body = SCHED.split("## 1. Six dispatch kinds")[1].split("## 2.")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


def dependency_rows():
    body = SCHED.split("## 2. Eight dependency kinds")[1].split("## 3.")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("scheduling", "six dispatch kinds, each classified scheduled or requested",
      lambda: (lambda rows: (len(rows) == 6 and all(
          re.search(r"(?i)scheduled|requested|awaited",
                    plain(r.strip().strip("|").split("|")[2])) for r in rows),
          "%d dispatch kinds" % len(rows)))(dispatch_rows()))


def human_work_is_requested_not_scheduled():
    bad = []
    for r in dispatch_rows():
        cells = [plain(c).strip() for c in r.strip().strip("|").split("|")]
        if re.search(r"(?i)human work|review|decision right", cells[1]):
            if not cells[2].startswith("Requested"):
                bad.append("%s is %r" % (cells[1], cells[2]))
    return (not bad and "Human authority is not a worker queue" in plain(SCHED),
            str(bad) if bad else "human, review and decision dispatches are requested")


check("scheduling", "human authority is requested, never scheduled as a queue",
      human_work_is_requested_not_scheduled)

check("scheduling", "eight dependency kinds with satisfaction and failure outcomes",
      lambda: (lambda rows: (len(rows) == 8 and all(len(r.strip().strip("|").split("|")) == 4
                                                    for r in rows), "%d kinds" % len(rows)))(
          dependency_rows()))

check("scheduling", "a branch condition may not read a model's opinion",
      lambda: ("It may not read a model" in plain(SCHED)
               and "has let confidence choose the path" in plain(SCHED), ""))

check("scheduling", "the dependency graph is acyclic and rework is a bounded loop",
      lambda: ("A dependency graph is acyclic" in plain(STD)
               and "The graph is acyclic; rework is a declared loop" in plain(SCHED)
               and "declared maximum iteration count" in plain(SCHED)
               and "A hidden cycle is a defect" in plain(STD), ""))

check("scheduling", "loop exhaustion escalates rather than continuing or failing silently",
      lambda: ("never `FAILED` and never silent continuation" in SCHED
               and "the loop is not converging" in plain(SCHED), ""))

check("scheduling", "sequencing belongs to the definition; timing to the orchestrator",
      lambda: ("Sequencing is the workflow definition's; timing is the orchestrator's"
               in plain(SCHED)
               and "would be editing the workflow" in plain(SCHED), ""))

check("scheduling", "orchestrator policy may not change what a stage means",
      lambda: ("may never change what a stage" in plain(RUN)
               and "second, unreviewed workflow definition" in plain(RUN)
               and "may never change what a stage means"
               in plain(TMPL["orchestrator-policy-template.md"]), ""))

check("scheduling", "long-running runs re-evaluate freshness at the point of use",
      lambda: ("re-evaluated at the point of use" in plain(SCHED)
               and "Phase 8's verdicts are use-specific and Phase 11 does not cache them"
               in plain(SCHED), ""))

check("scheduling", "a lapsed assignment is invalidated, never honoured as once-valid",
      lambda: ("invalidated and re-attempted" in plain(SCHED)
               and "never honoured on the grounds that it was valid when made"
               in plain(SCHED), ""))

# =========================================================== role / skill activation


def envelope_rows():
    body = RUN.split("## 5. The Assignment Envelope")[1].split("**No seniority variants.**")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("assignment", "the assignment envelope carries twelve fields",
      lambda: (lambda n: (n == 12, "%d fields" % n))(len(envelope_rows())))

ENVELOPE_FIELDS = ["Role ID", "Required skills", "Scope", "Task / activity reference",
                   "Criticality", "Required independence", "Executor eligibility",
                   "Review restrictions", "Decision restrictions",
                   "Sensitivity and residency", "Provenance", "Assignment reason"]
check("assignment", "every required envelope field is present",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d fields" % len(ENVELOPE_FIELDS)))(
          [f for f in ENVELOPE_FIELDS if f not in plain(RUN)]))

check("assignment", "activation confers nothing the profile did not carry",
      lambda: ("Coordination is not competence" in plain(STD)
               and "confers nothing the Role, the Skill and the scope" in plain(RUN)
               .replace("It confers nothing not already carried by the Role, the Skill and "
                        "the scope.", "confers nothing the Role, the Skill and the scope"),
               ""))

check("assignment", "executor eligibility is declared, never inferred",
      lambda: ("declared by the definition, never inferred" in plain(RUN), ""))

check("assignment", "review and decision exclusions are recorded at assignment time",
      lambda: ("Recording the exclusion at assignment time is what makes the later "
               "independence check checkable" in plain(RUN), ""))

check("assignment", "task, work item and assignment attempt stay three objects",
      lambda: ("Three objects that are routinely collapsed into one" in plain(RUN)
               and "It does not edit the Work Item" in plain(RUN)
               and "rewriting the workflow definition from inside a run" in plain(RUN), ""))

# =========================================================== router invocation

check("router", "the orchestrator submits a request; the router decides",
      lambda: ("The orchestrator submits a Model Invocation Request" in plain(ROUTE)
               and "these are two objects" in plain(ROUTE).lower(), ""))

check("router", "the request may not carry a chosen model or a relaxed constraint",
      lambda: ("does not choose an endpoint where a Routing Policy applies" in plain(ROUTE)
               and "would be choosing the model with extra steps" in plain(ROUTE), ""))

check("router", "a routing block is a block, not a prompt to re-ask",
      lambda: ("A block from the Router is a block" in plain(ROUTE)
               and "BLOCKED_FOR_ROUTING" in ROUTE
               and "NO_APPLICABLE_DECISION_RIGHT" in ROUTE, ""))

check("router", "routing decisions are recorded by value, not re-resolved",
      lambda: ("as a recorded value" in plain(ROUTE)
               and "does not re-resolve the model profile at read time" in plain(ROUTE), ""))


def retry_never_switches_to_evade_independence():
    return ("A retry" in plain(ROUTE)
            and "never" in plain(ROUTE).lower()
            and "alters the request's constraints, independence class or named prior selection"
            in plain(ROUTE)
            and "Repeated routing blocks are" in plain(ROUTE), "")


check("router", "retry may not switch models to evade an independence constraint",
      retry_never_switches_to_evade_independence)

check("router", "a model producing output completes an activity, not a gate",
      lambda: ("completes an activity, not a gate" in plain(ROUTE)
               and "agreement between two models" in plain(ROUTE), ""))

# =========================================================== gates


def gate_outcome_rows():
    body = GATE.split("## 3. Seven gate outcomes")[1].split("## 4.")[0]
    return [ln for ln in body.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)][1:]


GATE_OUTCOMES = ["SATISFIED", "SATISFIED_WITH_OPEN_ITEMS", "NOT_SATISFIED", "DEFER", "ESCALATE",
                 "EXPIRED", "NO_APPLICABLE_DECISION_RIGHT"]
check("gates", "seven gate outcomes parse, each with a run effect",
      lambda: (lambda rows: (len(rows) == 7 and all(o in GATE for o in GATE_OUTCOMES),
                             "%d outcomes" % len(rows)))(gate_outcome_rows()))


def non_satisfied_outcomes_never_continue():
    """Every non-satisfying outcome must forbid continuation in its own row."""
    bad = []
    for r in gate_outcome_rows():
        cells = [plain(c).strip() for c in r.strip().strip("|").split("|")]
        name, effect = cells[0], cells[2]
        if name in ("NOT_SATISFIED", "DEFER", "ESCALATE", "EXPIRED",
                    "NO_APPLICABLE_DECISION_RIGHT"):
            if re.search(r"(?i)^continue", effect) or not re.search(
                    r"(?i)BLOCK|ESCALAT|REWORK|WAITING|Never", effect):
                bad.append("%s effect is %r" % (name, effect[:50]))
    return (not bad, str(bad) if bad
            else "no non-satisfying outcome permits continuation")


check("gates", "no non-satisfying gate outcome permits continuation",
      non_satisfied_outcomes_never_continue)

check("gates", "four gate kinds are kept apart",
      lambda: ("Review and decision gates never merge" in plain(GATE)
               and "A satisfied review is not authority to act" in plain(GATE), ""))

check("gates", "re-requesting a gate requires a recorded change to the work",
      lambda: ("only after a recorded change to the work" in plain(GATE)
               and "reviewer shopping" in plain(GATE), ""))

check("gates", "a missing Decision Right blocks and escalates, with four refusals named",
      lambda: (all(t in plain(GATE) for t in ["pick the nearest Right",
                                              "treat the absence as permission",
                                              "approve it anyway",
                                              "continue and record the gap as an open item"]),
               ""))

check("gates", "independence is enforced mechanically at review request time",
      lambda: ("cannot" in plain(GATE)
               and "Reviewer independence and model diversity remain two controls" in plain(GATE)
               and "no eligible reviewer exists" in plain(GATE), ""))

check("gates", "a waiting window governs escalation, never proceeding",
      lambda: ("Human gates are not deadlines" in plain(GATE)
               and "never about when to proceed" in plain(GATE)
               and "auto-approve after" in plain(GATE), ""))

check("gates", "the policy template forbids an auto-approve setting",
      lambda: ("There is no auto-approve setting, and none may be added"
               in plain(TMPL["orchestrator-policy-template.md"]), ""))

# =========================================================== retry / replay / idempotency

RETRY_CLASSES = ["SAFE_AUTOMATIC_RETRY", "RETRY_REQUIRING_REVALIDATION",
                 "RETRY_REQUIRING_HUMAN_ACKNOWLEDGEMENT", "NON_RETRYABLE_GOVERNED_ACT",
                 "REPLAYABLE_READ_ONLY", "NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT",
                 "IDEMPOTENT_AT_LEAST_ONCE"]


def retry_rows():
    body = RETRY.split("## 1. Seven retry classes")[1].split("## 2.")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("retry", "seven retry classes parse, each with an automatic-retry answer",
      lambda: (lambda rows: (len(rows) == 7 and all(c in RETRY for c in RETRY_CLASSES),
                             "%d classes" % len(rows)))(retry_rows()))

check("retry", "an unclassified step is non-retryable by default",
      lambda: ("non-retryable by default" in plain(RETRY)
               and "the strict reading" in plain(RETRY), ""))


def authority_bearing_acts_never_replayed():
    bad = []
    for r in retry_rows():
        cells = [plain(c).strip() for c in r.strip().strip("|").split("|")]
        if cells[1] in ("NON_RETRYABLE_GOVERNED_ACT", "NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT"):
            if not re.search(r"(?i)never", cells[2]):
                bad.append("%s answers %r" % (cells[1], cells[2]))
    needles = ["Retry is not repetition of an authority-bearing act",
               "An external side effect is not replayable"]
    missing = [n for n in needles if n not in plain(STD)]
    return (not bad and not missing, str(bad + missing) if (bad or missing)
            else "authority-bearing and external acts are never automatically retried")


check("retry", "authority-bearing acts and external effects are never blindly replayed",
      authority_bearing_acts_never_replayed)

AUTHORITY_ACTS = ["Decision Record", "approval", "signature", "external publication",
                  "contract commitment", "risk acceptance", "purge", "destructive migration"]
check("retry", "every authority-bearing act class is enumerated as non-retryable",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d act classes" % len(AUTHORITY_ACTS)))(
          [a for a in AUTHORITY_ACTS if a.lower() not in plain(RETRY).lower()]))


def exactly_once_not_claimed():
    """An exactly-once claim anywhere, without being denied on its own line, is the defect."""
    bad = []
    for rel, doc in DOCS.items():
        flat = plain(doc)
        for m in re.finditer(r"(?i)exactly[- ]once", flat):
            line = line_of(flat, m.start())
            if DENIAL_MARKER.search(line):
                continue
            bad.append("%s: %s" % (rel, line.strip()[:80]))
    stated = ("Exactly-once is not claimed" in plain(STD)
              and "Exactly-once" in RETRY and "Nowhere" in RETRY)
    return (not bad and stated, str(bad) if bad
            else "exactly-once is denied, and the two real guarantees are stated instead")


check("retry", "exactly-once is never asserted, and the real guarantees are named",
      exactly_once_not_claimed)

check("retry", "the at-most-once guarantee is grounded in the governed record",
      lambda: ("At-most-once by governed record" in plain(RETRY)
               and "not achieved by the orchestrator being careful" in plain(RETRY)
               and "uniqueness constraint" in plain(RETRY), ""))

check("retry", "replay after recovery walks the classes rather than re-running everything",
      lambda: ("Replay after recovery" in plain(RETRY)
               and "Resolve the existing governed record by reference" in plain(RETRY)
               and "external side-effect uncertainty stops the run" in plain(RETRY).lower(), ""))

check("retry", "retry never widens a constraint or unblocks a block",
      lambda: ("never widens a constraint" in plain(RETRY)
               and "never converts a" in plain(RETRY)
               and "only a governed act resolves one" in plain(RETRY), ""))

check("retry", "compensation is distinguished from rollback",
      lambda: ("Rollback is not compensation" in plain(STD)
               and "Compensation vs rollback" in plain(FAILD)
               and "is not available for anything that left the system" in plain(FAILD), ""))

# =========================================================== concurrency / races

RACE_OUTCOMES = ["BLOCK", "IGNORE_AS_STALE", "SUPERSEDE", "RECONCILE", "ESCALATE"]


def race_rows():
    body = RACE.split("## 2. Ten races")[1].split("## 3.")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("concurrency", "five race outcomes are declared as a fixed vocabulary",
      lambda: (lambda rows: (len(rows) == 5, "%d outcomes" % len(rows)))(
          [ln for ln in RACE.split("## 1. Five outcomes")[1].split("## 2.")[0].splitlines()
           if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)][1:]))

check("concurrency", "ten races parse, each with an outcome from the vocabulary",
      lambda: (lambda rows: (len(rows) == 10 and all(
          any(o in plain(r.strip().strip("|").split("|")[2]) for o in RACE_OUTCOMES)
          for r in rows), "%d races" % len(rows)))(race_rows()))

REQUIRED_RACES = ["Duplicate trigger", "Double stage start", "Concurrent edits",
                  "Stale assignment result", "Review result after supersession",
                  "Decision result after cancellation", "Two workers claim one Work Item",
                  "Model result after run reclassification",
                  "Resumed run versus late retry", "Human intervention versus automated"]
check("concurrency", "every required race case is modelled",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d races" % len(REQUIRED_RACES)))(
          [r for r in REQUIRED_RACES if r.lower() not in plain(RACE).lower()]))


def late_results_are_never_applied():
    return ("Stale results are recorded, never applied" in plain(STD)
            and "does not" in plain(STD)
            and "Why case 6 is not" in plain(RACE), "")


check("concurrency", "late results are recorded and never applied", late_results_are_never_applied)


# A late Decision Record may require RECONCILE and/or ESCALATE for current-state handling.
# It may never be characterised as stale ITSELF: staleness is a property a coordinator would
# be assigning to a governed act that occurred, which is the one move this race case exists to
# refuse.
#
# Two earlier versions of this rule were bypassed. The first was a forbidden-word list, which
# only knows the words someone thought of. The second replaced it with predications plus a
# PROXIMITY-based negation suppressor - any negator within 40 characters cancelled the match -
# and the re-audit wrote "The Decision Record stands and is not optional but is stale", where
# the negation belongs to `optional` and the staleness is asserted anyway.
#
# The rule now is grammatical rather than positional: a negation suppresses a stale match ONLY
# when it is attached to the stale predicate itself. There is no lookback window, and there is
# no line-wide denial exemption: both were ways for a negation somewhere else in the sentence
# to speak for a predicate it does not govern.
NEGATOR = r"(?:not|never|no\s+longer|neither|nor)"
ADVERB = r"(?:now|then|already|merely|simply|yet|still)"
COPULA = r"(?:is|was|were|becomes?|became|remains?|stays?|gets?|turns?|counts?|reads?)"
SUBJECT = r"(?:record|records|decision|act|it|which|that|this)"
ASSESSED = r"(?:deemed|considered|marked|regarded|classified|counted|treated|held|taken)"

# The negator slot sits INSIDE each pattern, immediately before `stale`, so only a negation in
# that slot suppresses. Fixed-width lookbehinds cover the adjectival and participle forms.
STALE_PREDICATION = re.compile(
    r"(?<!not )(?<!never )(?<!not a )(?<!never a )\bstale\s+(?:decision\s+)?record\b"
    r"|\b%(subj)s\s+%(cop)s\s+(?!%(neg)s\b)(?:%(adv)s\s+)*stale\b"
    r"|(?<!not )(?<!never )\b%(ass)s\s+(?:as\s+|to\s+be\s+)?stale\b"
    r"|\b%(cop)s\s+(?!%(neg)s\b)(?:%(adv)s\s+)*stale\b"
    % {"subj": SUBJECT, "cop": COPULA, "neg": NEGATOR, "adv": ADVERB, "ass": ASSESSED},
    re.I)

# The row-scoped matcher above is deliberately broad, because it is only ever applied to the
# two cells of the late-Decision race row, where a sentence about anything being stale does not
# belong. The Phase-11-wide matcher below is narrow by necessity: it must name a Decision
# Record, so that stale *evidence* - a real and blocking condition in this architecture - is
# never touched by it. Two scopes, two widths, and the difference is the point.
NAMED_STALE_RECORD = re.compile(
    r"(?<!not )(?<!never )(?<!not a )(?<!never a )\bstale\s+decision\s+record\b"
    r"|\bdecision\s+record\b[^.;|]{0,60}?\b%(cop2)s\s+(?!%(neg)s\b)"
    r"(?:%(adv)s\s+)*stale\b"
    r"|\bdecision\s+record\b[^.;|]{0,60}?(?<!not )(?<!never )\b%(ass)s\s+"
    r"(?:as\s+|to\s+be\s+)?stale\b"
    % {"cop2": COPULA, "neg": NEGATOR, "adv": ADVERB, "ass": ASSESSED},
    re.I)

# Formatting is not semantics.
#
# The previous pass exempted anything inside a code span, on the theory that a quoted wording
# is a specimen rather than an assertion. The re-audit showed what that buys an author who
# does not want to be caught: backticks around one word, or around half the subject, delete
# exactly the text the invariant needs to read. `The Decision Record is ``stale``.` and
# `The Decision ``Record`` is stale.` both passed, and neither is a quotation of anything.
#
# So markup is now NORMALISED rather than deleted - every formatting marker is removed while
# the semantic text it wrapped is preserved - and an exemption has to be claimed EXPLICITLY,
# in a fence that says what it is. A fence is a statement by the author; a backtick is a
# typographic choice, and the two are not interchangeable.
SPECIMEN_FENCE = re.compile(
    r"<!--\s*stale-specimen\s*-->.*?<!--\s*/stale-specimen\s*-->", re.S)


# `plain()` is the suite's general normaliser and strips only `**` and backticks, which is all
# the other 150 checks need. It is deliberately NOT widened here: it is used in roughly a
# hundred places, and stripping underscores broadly would destroy the vocabulary this
# architecture is written in - IGNORE_AS_STALE, NON_RETRYABLE_GOVERNED_ACT, GOVERNANCE_CLEAR.
#
# So this invariant gets its own normaliser. The re-audit showed why: emphasis and
# strikethrough markers split the governed subject, and `The Decision *Record* is stale.`
# passed because nothing removed the asterisks.
#
# Every supported marker is removed; NO enclosed text ever is. An underscore between two
# alphanumerics is an identifier character and is kept, which is what protects the declared
# vocabulary while `_Record_` is still normalised away.
INTRAWORD_SAFE_UNDERSCORE = re.compile(r"(?<![A-Za-z0-9])_|_(?![A-Za-z0-9])")


class _VisibleText(HTMLParser):
    """Collects what an HTML fragment renders: text in, tags and comments out.

    `convert_charrefs=True` decodes character references inside text, so an entity that
    reconstructs part of a word is resolved rather than left as a splitter. Comments have no
    handler, so they disappear while the text on either side of them joins up."""

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append(html.unescape("&%s;" % name))

    def handle_charref(self, name):
        self.parts.append(html.unescape("&#%s;" % name))


# A real parser reads quoted attributes, comments and character references correctly, and
# there is exactly one shape it handles WORSE than a crude strip: an opener that never closes,
# where it buffers the rest as an incomplete tag and the words are lost. Losing visible content
# is the single thing this path may never do - it is precisely how an assertion gets hidden.
#
# The fix is not a second reading to compare against; a crude strip leaks presentation as
# content and would win the comparison on well-formed input. Instead, unterminated openers are
# located with a quote-aware scan - the one thing a regex cannot do here - and reduced to
# nothing, leaving the words they prefixed for the parser to read normally.


def _tag_closes(text, index):
    """Whether the `<` at `index` has a `>` terminating it OUTSIDE any quoted attribute.

    Two bounds make this a local decision rather than an open-ended search, and both matter:

    * quotes are tracked, because `<span title="a>b">` does not end at the first `>` it
      contains - the distinction a regex cannot draw;
    * the scan stops at the end of the LINE. An inline tag is inline. Without that bound, a
      stray `<em` could find a `>` arbitrarily far below - a blockquote marker at the start of
      some later line will do - be judged well-formed, and hand the parser everything in
      between to swallow. That is how malformed presentation consumed visible content in the
      full-document path while the single-cell row path, which has no later `>`, read the
      same text correctly. Bounding to the line makes the two agree by construction, and errs
      towards treating an opener as malformed, which neutralises the marker and keeps the
      words."""
    quote, i, limit = None, index + 1, len(text)
    while i < limit:
        ch = text[i]
        if ch == "\n":
            return False
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == ">":
            return True
        elif ch == "<":
            return False
        i += 1
    return False


def neutralise_unterminated(text):
    """Remove markers that open a construct they never close, keeping every word after them."""
    out, i, limit = [], 0, len(text)
    while i < limit:
        if text.startswith("<!--", i):
            # A comment may span lines, but not the whole document: bounded to the paragraph,
            # so an unterminated marker cannot reach a `-->` belonging to something else.
            paragraph = text[i:].split("\n\n", 1)[0]
            closer = paragraph.find("-->")
            if closer != -1:
                end = i + closer + 3
                out.append(text[i:end])              # a real comment, left for the parser
                i = end
                continue
            i += 4                                   # an unclosed comment marker, dropped
            continue
        if text.startswith("-->", i):
            i += 3                                   # an orphaned terminator, dropped
            continue
        if text[i] == "<" and not _tag_closes(text, i):
            match = re.match(r"</?[A-Za-z][A-Za-z0-9-]*", text[i:])
            if match:
                i += match.end()                     # an unclosed opener, dropped
                continue
        out.append(text[i])
        i += 1
    return "".join(out)


def strip_inline_html(text):
    """Visible text of `text`, parsed rather than pattern-matched.

    A parser is used because a regex cannot see a quoted attribute containing a tag
    terminator, a comment between two visible words, or a character reference inside a word.
    Unterminated markers are neutralised first, so no construct the parser would abandon can
    take a sentence with it. If the parser raises at all, the fallback strips angle-bracket
    runs - failing towards MORE normalisation, never less, because less is what hides."""
    pre = neutralise_unterminated(text)
    parser = _VisibleText()
    try:
        parser.feed(pre)
        parser.close()
    except Exception:
        return html.unescape(re.sub(r"<[^>]*>", "", pre))
    return "".join(parser.parts)


def _consume_balanced(text, index, opener, closer):
    """Index just past the balanced group starting at `index`, or None if it does not close.

    Nesting is counted rather than matched with a regex, which is what lets a link
    destination containing balanced parentheses be consumed completely instead of leaving
    its tail in the visible text."""
    depth, i, limit = 0, index, len(text)
    while i < limit:
        ch = text[i]
        if ch == "\n":
            return None
        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return None


def strip_markdown_links(text):
    """Markdown inline and reference links reduced to their visible label.

    A link renders as its label; the destination is syntax nobody reads. Labels are processed
    recursively so a link nested inside a label cannot smuggle syntax back in."""
    out, i, limit = [], 0, len(text)
    while i < limit:
        ch = text[i]
        if ch != "[":
            out.append(ch)
            i += 1
            continue
        label_end = _consume_balanced(text, i, "[", "]")
        if label_end is None:
            out.append(ch)
            i += 1
            continue
        label = text[i + 1:label_end - 1]
        after = label_end
        if after < limit and text[after] in "([":
            opener = text[after]
            closer = ")" if opener == "(" else "]"
            target_end = _consume_balanced(text, after, opener, closer)
            if target_end is not None:
                out.append(strip_markdown_links(label))
                i = target_end
                continue
        # A bare [label] renders with its brackets. They are punctuation, not content, and
        # dropping them can only join tokens - never hide one.
        out.append(strip_markdown_links(label))
        i = label_end
    return "".join(out)


def semantic_text(text):
    """The text as it renders: presentation removed, visible content preserved exactly.

    The reading order matters and is fixed:

    1. Markdown links first, so a destination containing angle brackets never reaches the
       HTML parser as if it were markup.
    2. Inline HTML next, through a real parser, which also decodes character references -
       so an entity that decodes to a formatting marker is stripped by step 3 rather than
       surviving as one.
    3. Markdown emphasis markers last.

    Every step removes presentation and keeps visible text. None removes content, so this
    can only join tokens that presentation split; it can hide nothing."""
    out = strip_markdown_links(text)
    out = strip_inline_html(out)
    out = out.replace("`", "")
    for marker in ("~~", "**", "__"):
        out = out.replace(marker, "")
    out = out.replace("*", "")
    return INTRAWORD_SAFE_UNDERSCORE.sub("", out)


# The row-scoped matcher above is deliberately broad, because it is only ever applied to the
# two cells of the late-Decision race row, where a sentence about anything being stale does not
# belong. The Phase-11-wide matcher below is narrow by necessity: it must name a Decision
# Record, so that stale *evidence* - a real and blocking condition in this architecture - is
# never touched by it. Two scopes, two widths, and the difference is the point.
NAMED_STALE_RECORD = re.compile(
    r"(?<!not )(?<!never )(?<!not a )(?<!never a )\bstale\s+decision\s+record\b"
    r"|\bdecision\s+record\b[^.;|]{0,60}?\b%(cop2)s\s+(?!%(neg)s\b)"
    r"(?:%(adv)s\s+)*stale\b"
    r"|\bdecision\s+record\b[^.;|]{0,60}?(?<!not )(?<!never )\b%(ass)s\s+"
    r"(?:as\s+|to\s+be\s+)?stale\b"
    % {"cop2": COPULA, "neg": NEGATOR, "adv": ADVERB, "ass": ASSESSED},
    re.I)

def assertive_text(doc):
    """The document's assertions: markup normalised, explicitly fenced specimens removed.

    Markers are removed while their contents are kept, so a wrapped or split word reads
    exactly as the sentence means it. Only an explicit specimen fence is dropped, and only a
    review record quoting rejected wordings has any reason to open one."""
    return semantic_text(SPECIMEN_FENCE.sub(" ", doc))


# =========================================================== identity contradiction

# A required denial being present says nothing about whether the corpus also asserts the
# collapse it denies. The pairs are DERIVED from the denials themselves rather than listed, so
# a denial added to the architecture is guarded the moment it is written.
def denied_identity_pairs(docs):
    """Every pair of objects Phase 11 asserts to be distinct, read out of its `!=` denials."""
    pairs = set()
    for doc in docs.values():
        for line in plain(doc).splitlines():
            for seq in re.findall(r"[A-Z][A-Z ]*(?:!=\s*[A-Z][A-Z ]*)+",
                                  line.replace(" !=", "!=")):
                terms = [t.strip() for t in seq.split("!=") if 2 <= len(t.strip()) <= 30]
                for i, first in enumerate(terms):
                    for second in terms[i + 1:]:
                        if first != second:
                            pairs.add((first, second))
    return sorted(pairs)


# Identity contradictions are read by GUARDED-PAIR CO-OCCURRENCE, not by enumerating
# equivalence verbs. A v10 audit walked past four enumerated forms with `constitutes`,
# `doubles as`, `denote` and `collapses into`. The rule is inverted: two guarded objects
# appearing in one predication are not presumed harmless - the span must PROVE it is a
# separation or one of the narrow relations the committed corpus actually uses.
IDENTITY_PAIRS = denied_identity_pairs(NORMATIVE)
GUARDED_PAIRS = set(IDENTITY_PAIRS) | set((b, a) for a, b in IDENTITY_PAIRS)
GUARDED_TERMS = sorted({t for pair in IDENTITY_PAIRS for t in pair}, key=len, reverse=True)
GUARDED_TERM = re.compile(
    r"\b(%s)\b" % "|".join(t.replace(" ", r"\s+") for t in GUARDED_TERMS), re.I)

# A closed function-word vocabulary. Anything outside it is a content word, and a predication
# linking two guarded objects must have every one of its content words in the corpus's own
# safe-relation vocabulary. There is no silent skip any more: a co-occurrence the grammar
# cannot prove benign is an offence, however long, parenthetical or pronoun-bearing it is.
FUNCTION_WORDS = set("""a an the its their his her this these those each every any no some all
one of to in on at by for from with within under over as into onto per via through between
among about than is are was were be been being remain remains remained become becomes became
has have had do does did will would shall should may might can could must not never only also
still now just simply merely really actually effectively same other another it they them which
that who whose what he she we you""".split())
SEPARATION = re.compile(r"\b(?:not|never|neither|nor|no)\b|!=", re.I)
PROPOSITION_BREAK = re.compile("[,;:]|\u2014|\u2013|--|" + r"\b(?:and|or|nor|but)\b", re.I)
# A predication puts the second term in predicate position, so the link ends where a noun
# phrase begins: on a determiner, on a bare copula, or on an equals sign. A link ending on a
# preposition ("artifacts in", "authorised by which") is a list or a different proposition -
# it never asserts that the two objects are the same thing.
PREDICATE_TAIL = re.compile(
    r"\b(?:a|an|the|its|their|this|that|these|those|one|both)\s*$"
    r"|\b(?:is|are|was|were|be|been|being|remains?|remained|becomes?|became)\s*$"
    r"|=+\s*$", re.I)
# An aside may be removed because it interrupts a predication; a LIST may not, because its
# commas are the structure. An aside is lowercase-led, and a comma-aside is only recognised
# where the link carries exactly the two commas that delimit it.
BRACKET_ASIDE = [re.compile(r"\([^()]{0,80}\)"),
                 re.compile(r"—\s*[a-z][^—]{0,60}—")]
COMMA_ASIDE = re.compile(r",\s*[a-z][^,]{0,60},")
# Named only so a controlled weakening can reinstate the silent skip this remediation
# removed: a pronoun or an aside used to make a co-occurrence invisible.
PRONOUN_OR_ASIDE = re.compile(r"\b(?:it|they|them|which|that|who|whose)\b|[(),\u2014]", re.I)
LIST_SEPARATOR = re.compile(r"^[\s,]*(?:and|or|nor)?[\s,]*$", re.I)
COORDINATED_SUBJECT = re.compile(r"\s*(?:,\s*|\s+(?:and|or)\s+)(?:a|an|the)?\s*")
# A predication of a coordinated pair: a copula, or a verb taking a determiner. A preposition
# is not a predication, which is what keeps "Review Profile or Decision Right from the
# definition" a list rather than an assertion about the pair.
COPULA_HEAD = re.compile(
    r"^(?:is|are|was|were|be|been|being|remains?|remained|becomes?|became)\b", re.I)
VERB_WITH_OBJECT = re.compile(r"^([A-Za-z][A-Za-z'-]*)\s+(?:one|a|an|the|both|two|each)\b", re.I)
SEPARATION_PREDICATE = re.compile(
    r"^(?:is|are|was|were|remains?|becomes?)\s+"
    r"(?:not|never|two|three|distinct|separate|different|independent)\b", re.I)
# The relations the committed corpus asserts between two guarded objects, measured from it,
# plus the non-identity forms Phase 11 names explicitly. Anything else is unproven.
SAFE_RELATIONS = {"records", "recorded", "references", "activates", "requests", "binds",
                  "execution", "submits", "rewriting", "produced", "reaching", "satisfied",
                  "exercise"}


def strip_asides(text):
    """Remove interrupting asides so the predication underneath can be read.

    Brackets and em-dash asides are removed whenever they are lowercase-led. A comma aside is
    removed only where the text carries exactly the two commas that delimit it: in a list the
    commas ARE the structure, and eating them would turn an enumeration into a predication."""
    previous = None
    while previous != text:
        previous = text
        for pattern in BRACKET_ASIDE:
            text = pattern.sub(" ", text)
    if text.count(",") == 2:
        text = COMMA_ASIDE.sub(" ", text, count=1)
    return text


def _content_words(text):
    return [w for w in re.findall(r"[A-Za-z][A-Za-z'-]*", text)
            if w.lower() not in FUNCTION_WORDS]


def _coordinated_predication(raw_tail):
    """The predicate made of a coordinated guarded pair, or None if none is made."""
    tail = strip_asides(raw_tail).strip()
    if re.match(r"(?:and|or|nor)\b", tail, re.I):
        return None                                  # the enumeration simply continues
    if COPULA_HEAD.match(tail):
        return tail
    verb = VERB_WITH_OBJECT.match(tail)
    if verb and verb.group(1).lower() not in FUNCTION_WORDS:
        return tail
    return None                                      # not a predication of the pair at all


def identity_collapses(text):
    """Guarded-pair co-occurrences the grammar cannot prove benign.

    Every co-occurrence of a guarded pair inside one proposition is an offence unless the span
    proves an explicit separation, a possessive or compound reference, an enumeration, a
    different proposition on each side, or a relation drawn entirely from the corpus's own safe
    vocabulary. Length, parentheses, pronouns and relative clauses are no longer reasons to
    skip - the aside is removed and the predication underneath is read."""
    found = []
    for span in re.split(r"[.;|\n]", text):
        marks = [(re.sub(r"\s+", " ", hit.group(0).upper()), hit.start(), hit.end())
                 for hit in GUARDED_TERM.finditer(span)]
        for index, (first, _start, first_end) in enumerate(marks):
            for second, second_start, second_end in marks[index + 1:]:
                if (first, second) not in GUARDED_PAIRS:
                    continue
                gap = span[first_end:second_start]
                if SEPARATION.search(gap):
                    continue                          # an explicit denial
                if gap.strip() in ("", "'s"):
                    continue                          # a compound name or a possessive
                if COORDINATED_SUBJECT.fullmatch(gap):
                    predicate = _coordinated_predication(span[second_end:])
                    if predicate is None:
                        continue
                    if SEPARATION_PREDICATE.match(predicate) or SEPARATION.search(
                            predicate[:60]):
                        continue
                    found.append("%s + %s: %s" % (first, second, predicate[:60]))
                    continue
                if LIST_SEPARATOR.fullmatch(gap):
                    continue                          # a bare list separator
                link = strip_asides(gap)
                if SEPARATION.search(link):
                    continue
                if PROPOSITION_BREAK.search(link):
                    continue                          # the terms sit in different propositions
                if GUARDED_TERM.search(link):
                    continue                          # a third guarded term: this is a list
                if not PREDICATE_TAIL.search(link):
                    continue                          # the second term is not in predicate position
                words = _content_words(link)
                if words and all(w.lower() in SAFE_RELATIONS for w in words):
                    continue
                found.append("%s / %s: %s" % (first, second, link.strip()[:60]))
    return found


def identity_collapse_offences(docs):
    """Collapse assertions in a corpus, named so the guard can drive the SCAN, not the helper.

    Read through `semantic_text` rather than `assertive_text`: the specimen fence is a
    review-record device, and letting it silence this scan would hand normative content a way
    to assert a collapse inside a fence. Normative artifacts may not open one at all."""
    return ["%s: %s" % (rel, hit)
            for rel, doc in docs.items() for hit in identity_collapses(semantic_text(doc))]


def no_identity_collapse_asserted():
    """A denial elsewhere does not cancel a collapse asserted here."""
    bad = identity_collapse_offences(NORMATIVE)
    return (not bad, str(bad)[:300] if bad
            else "%d denied pairs, no positive collapse asserted" % len(IDENTITY_PAIRS))


check("identity", "no normative artifact asserts a denied identity collapse",
      no_identity_collapse_asserted)


def identity_collapse_scan_is_driven():
    """The contradiction grammar, executed rather than described.

    The committed corpus asserts no collapse, so the corpus scan passes whether or not the
    grammar works. These probes are what make weakening it fail. The negatives deliberately use
    verbs the harness enumerates nowhere - that is the point of reading co-occurrence rather
    than vocabulary."""
    collapses = [
        # The v11 bypasses: long, parenthetical, pronoun-bearing or multi-content-word
        # relations that the previous heuristics skipped in silence.
        "A Role has exactly the same governance identity as an Agent Instance.",
        "A Role should be treated in all respects as an Agent Instance.",
        "A Role, for every operational purpose, constitutes an Agent Instance.",
        "A Role is functionally indistinguishable from an Agent Instance.",
        "A Role, which the runtime creates, is an Agent Instance.",
        "The Router and the Orchestrator, taken together, are one component.",
        # Other aside shapes: brackets, an em-dash aside, a very long interruption.
        "A Role (as the runtime sees it) is an Agent Instance.",
        "A Role \u2014 in every respect that matters \u2014 is an Agent Instance.",
        "A Role, in the view of every operator who has ever looked at one, is an Agent "
        "Instance.",
        # The v10 bypasses.
        "A Role is effectively an Agent Instance.",
        "A Role constitutes an Agent Instance.",
        "The Router is indistinguishable from the Orchestrator.",
        "The Router and Orchestrator denote one component.",
        "A Decision Right collapses into a Decision Record.",
        "ROLE == AGENT INSTANCE",
        "The Router doubles as the Orchestrator.",
        "Role functions as an Agent Instance.",
        "Orchestrator serves as the Router.",
        "A Review Profile and Review Instance are effectively one object.",
        # Independent forms, no shared equivalence-verb family.
        "A Workflow amounts to a Workflow Run.",
        "The Credential subsumes the Human Authority.",
        "A Runtime Event qualifies as an Audit Event.",
        "The Task coincides with the Work Item.",
        "A Decision Right reduces to a Decision Record.",
        # The plain forms the earliest enumeration already caught, kept as regression.
        "ROLE = AGENT INSTANCE",
        "A Role is an Agent Instance.",
        "ROUTER = ORCHESTRATOR",
        "The Router is the Orchestrator.",
        "Router and Orchestrator are the same component.",
        # Formatting is not semantics: emphasis, code spans and a comment splitting a term.
        "**ROLE** = **AGENT INSTANCE**",
        "The `Router` is *indistinguishable* from the Orchestrator.",
        "A Ro<!--x-->le is an Agent Instance.",
    ]
    benign = [
        "ROLE != AGENT INSTANCE",
        "ROUTER != ORCHESTRATOR",
        "The orchestrator is not the Router.",
        "A Role is never an Agent Instance.",
        "A Router and an Orchestrator are two components, not one.",
        "The `Router` is *not* the Orchestrator.",
        "A Workflow Run is an execution of a Workflow.",
        "The Decision Record records the exercise of a Decision Right.",
        "A Decision Record records a Decision Right.",
        "An Agent Instance carries no Role of its own.",
        "Review Profile or Decision Right from the definition",
        "Task, Work Item and Assignment",
        "The orchestrator's role",
        "The orchestrator submits a Model Invocation Request",
        "Reviews stay in review, decisions in decision, knowledge in knowledge, routing in "
        "routing, artifacts in artifact",
    ]
    problems = []
    for text in collapses:
        if not identity_collapses(semantic_text(text)):
            problems.append("collapse not detected: %s" % text)
    for text in benign:
        hits = identity_collapses(semantic_text(text))
        if hits:
            problems.append("denial or description read as a collapse: %s -> %s" % (text, hits))
    # Drive the corpus scan itself, on synthetic documents shaped like normative artifacts.
    offending = "# Roles\n\nA Role constitutes an Agent Instance.\n\nThe stage activates it.\n"
    fenced = ("# Roles\n\n<!-- stale-specimen -->\nThe Router doubles as the Orchestrator.\n"
              "<!-- /stale-specimen -->\n")
    clean = "# Roles\n\nROLE != AGENT INSTANCE, and a Role is never an Agent Instance.\n"
    if not identity_collapse_offences({"orchestration/synthetic.md": offending}):
        problems.append("the document scan missed an asserted collapse")
    if not identity_collapse_offences({"orchestration/synthetic.md": fenced}):
        problems.append("a specimen fence hid a collapse from the normative scan")
    if identity_collapse_offences({"orchestration/synthetic.md": clean}):
        problems.append("the document scan rejected canonical denial prose")
    return (not problems, str(problems)[:300] if problems
            else "%d collapses detected, %d denials and descriptions left alone"
                 % (len(collapses), len(benign)))


def denial_chains(docs):
    """Independent parse of every `A != B != C` chain into its term list.

    Deliberately NOT the production builder and deliberately not its regex: this walks the
    line, splits on the operator, and reads the capitalised run on each side. The production
    pair set is then checked against `itertools.combinations` over these chains, so a builder
    that silently drops to adjacent pairs cannot be validated by its own implementation."""
    def leading_caps(text):
        out = []
        for char in text.lstrip():
            if char.isupper() or char == " ":
                out.append(char)
            else:
                break
        return " ".join("".join(out).split())

    def trailing_caps(text):
        out = []
        for char in reversed(text.rstrip()):
            if char.isupper() or char == " ":
                out.append(char)
            else:
                break
        return " ".join("".join(reversed(out)).split())

    chains = []
    for doc in docs.values():
        for line in plain(doc).splitlines():
            if "!=" not in line:
                continue
            parts = line.split("!=")
            terms = [trailing_caps(parts[0])]
            for middle in parts[1:-1]:
                stripped = " ".join(middle.split())
                terms.append(stripped if re.fullmatch(r"[A-Z][A-Z ]*", stripped)
                             else leading_caps(middle))
            terms.append(leading_caps(parts[-1]))
            terms = [t for t in terms if 2 <= len(t) <= 30]
            if len(terms) >= 2:
                chains.append(terms)
    return chains


def denied_pair_closure():
    """The guarded-pair set must be the FULL closure of every denial chain.

    A v10 weakening dropped the production builder from all combinations to adjacent pairs -
    212 pairs down to 23 - and the suite still reported PASS, because nothing asserted the
    closure. The closure is now computed independently and compared, pair by pair."""
    chains = denial_chains(NORMATIVE)
    produced = set(frozenset(pair) for pair in IDENTITY_PAIRS)
    expected, arithmetic = set(), 0
    for terms in chains:
        unique = list(dict.fromkeys(terms))
        arithmetic += len(unique) * (len(unique) - 1) // 2
        expected |= set(frozenset(c) for c in itertools.combinations(unique, 2))
    problems = []
    missing = expected - produced
    extra = produced - expected
    if missing:
        problems.append("%d pairs missing, e.g. %s"
                        % (len(missing), sorted(tuple(sorted(p)) for p in missing)[:3]))
    if extra:
        problems.append("%d pairs not derived from any denial chain, e.g. %s"
                        % (len(extra), sorted(tuple(sorted(p)) for p in extra)[:3]))
    if len(IDENTITY_PAIRS) != len(produced):
        problems.append("the production set contains a duplicated or reversed pair")
    # The longest chain alone must contribute its whole n*(n-1)/2 closure to the PRODUCTION
    # set. Asserted against `itertools.combinations` directly rather than against `expected`,
    # so the comparison cannot be satisfied by aliasing the oracle to the production output.
    if chains:
        longest = list(dict.fromkeys(max(chains, key=len)))
        closure = set(frozenset(c) for c in itertools.combinations(longest, 2))
        if not closure <= produced:
            problems.append("the longest chain of %d terms contributes only %d of its %d pairs"
                            % (len(longest), len(closure & produced), len(closure)))
        if len(closure) != len(longest) * (len(longest) - 1) // 2:
            problems.append("closure arithmetic is wrong for the longest chain")
    # The independent chain parser itself, on synthetic input with a hand-computed answer.
    synthetic = {"orchestration/synthetic.md": "ALPHA != BETA != GAMMA != DELTA\n"}
    parsed = denial_chains(synthetic)
    if parsed != [["ALPHA", "BETA", "GAMMA", "DELTA"]]:
        problems.append("the independent chain parser misread a synthetic chain: %s" % parsed)
    elif len(set(frozenset(c) for c in itertools.combinations(parsed[0], 2))) != 6:
        problems.append("closure of a 4-term chain is not 6 pairs")
    return (not problems, str(problems)[:300] if problems
            else "%d chains, %d pair slots, %d distinct pairs, production agrees exactly"
                 % (len(chains), arithmetic, len(expected)))


check("identity", "the guarded-pair set is the full closure of every denial chain",
      denied_pair_closure)


def chain_closure_independently_verified():
    """Closure proved again, by a third path that touches neither of the other two.

    This check calls neither `denied_pair_closure()` nor `denial_chains()`. It finds the
    longest denial line itself, splits it on the operator with `re.split`, and builds the
    closure with `itertools.combinations`. Two checks that shared a helper would fail together
    and prove nothing about each other."""
    lines = [ln for doc in NORMATIVE.values() for ln in plain(doc).splitlines() if "!=" in ln]
    if not lines:
        return (False, "no denial line found at all")
    problems = []
    universe = set()
    for line in lines:
        terms = [" ".join(part.split()) for part in re.split(r"\s*!=\s*", line)]
        terms[0] = " ".join(re.findall(r"[A-Z][A-Z ]*$", terms[0].rstrip()) or [""]).strip()
        terms[-1] = " ".join(re.findall(r"^[A-Z][A-Z ]*", terms[-1].lstrip()) or [""]).strip()
        terms = [t for t in terms if 2 <= len(t) <= 30]
        universe |= set(frozenset(c) for c in itertools.combinations(dict.fromkeys(terms), 2))
    produced = set(frozenset(pair) for pair in IDENTITY_PAIRS)
    if universe != produced:
        problems.append("independent closure differs: %d expected, %d produced, %d missing"
                        % (len(universe), len(produced), len(universe - produced)))
    # The separation chain itself: every one of its pairs, not only the adjacent ones.
    chain = max((re.split(r"\s*!=\s*", ln) for ln in lines), key=len)
    chain = [" ".join(p.split()) for p in chain]
    chain[0] = " ".join(re.findall(r"[A-Z][A-Z ]*$", chain[0].rstrip()) or [""]).strip()
    chain = [t for t in chain if re.fullmatch(r"[A-Z][A-Z ]*", t)]
    if len(chain) != len(SEPARATED):
        problems.append("the separation chain parsed as %d terms, not %d"
                        % (len(chain), len(SEPARATED)))
    expected_pairs = len(chain) * (len(chain) - 1) // 2
    chain_closure = set(frozenset(c) for c in itertools.combinations(chain, 2))
    if len(chain_closure) != expected_pairs:
        problems.append("chain closure arithmetic is wrong")
    if not chain_closure <= produced:
        problems.append("%d of the chain's %d pairs are missing from the production set"
                        % (len(chain_closure - produced), expected_pairs))
    # A pair from the two ends of the chain is the one an adjacent-only derivation loses first.
    for distant in (("ROLE", "HUMAN AUTHORITY"), ("ROLE", "CREDENTIAL"),
                    ("AGENT INSTANCE", "DECISION RECORD")):
        if frozenset(distant) not in produced:
            problems.append("a distant pair is absent: %s" % (distant,))
    # The arithmetic, on a synthetic chain with a hand-computed answer.
    synthetic = [" ".join(p.split()) for p in re.split(r"\s*!=\s*", "ALPHA != BETA != GAMMA != DELTA")]
    if len(set(frozenset(c) for c in itertools.combinations(synthetic, 2))) != 6:
        problems.append("closure of a 4-term chain is not 6 pairs")
    return (not problems, str(problems)[:300] if problems
            else "%d pairs proved by a third independent path, %d in the chain's own closure"
                 % (len(universe), expected_pairs))


check("identity", "the closure is proved again by an independent path",
      chain_closure_independently_verified)


def closure_checks_reject_a_weakened_pair_set():
    """Negative control: both closure checks must FAIL when the pair set is weakened.

    The committed set is correct, so a closure check that simply returned success would pass
    unnoticed. Here the guarded-pair set is deliberately corrupted three ways and each closure
    check is required to reject it. A check replaced by an unconditional success fails here,
    and so does an oracle aliased to the production output it is meant to audit."""
    global IDENTITY_PAIRS
    original = IDENTITY_PAIRS
    chains = denial_chains(NORMATIVE)
    adjacent = []
    for terms in chains:
        unique = list(dict.fromkeys(terms))
        adjacent += list(zip(unique, unique[1:]))
    weakenings = {
        "adjacent pairs only": sorted(set(adjacent)),
        "one pair removed": original[:-1],
        "an undenied pair added": original + [("ALPHA", "OMEGA")],
        "the set emptied": [],
    }
    problems = []
    try:
        for label, weakened in weakenings.items():
            IDENTITY_PAIRS = weakened
            for name, closure_check in (("denied_pair_closure", denied_pair_closure),
                                        ("chain_closure_independently_verified",
                                         chain_closure_independently_verified)):
                accepted, _evidence = closure_check()
                if accepted:
                    problems.append("%s accepted a pair set with %s" % (name, label))
    finally:
        IDENTITY_PAIRS = original
    if len(IDENTITY_PAIRS) != len(original):
        problems.append("the negative control did not restore the guarded-pair set")
    return (not problems, str(problems)[:300] if problems
            else "%d weakened pair sets, each rejected by both closure checks"
                 % len(weakenings))


check("identity", "a weakened guarded-pair set is rejected by both closure checks",
      closure_checks_reject_a_weakened_pair_set)



check("identity", "an identity collapse is detected even where the denial also stands",
      identity_collapse_scan_is_driven)


# Registered here rather than beside their definitions: both read `semantic_text`, which is
# defined above this point and not above the scope grammar. `main()` groups results by label,
# so they still print under [scope].
check("scope", "no scope crossing is implicit", no_implicit_scope_crossing)
check("scope", "every scope crossing parses as a canonical governed construction",
      controlled_crossing_grammar)


def named_stale_record(text):
    """Predications of staleness that name a Decision Record, anywhere in Phase 11."""
    scrubbed = text.replace("IGNORE_AS_STALE", "<declared-outcome-token>")
    return [" ".join(m.group(0).split()) for m in NAMED_STALE_RECORD.finditer(scrubbed)]


def stale_characterisations(text):
    """Predications of staleness in `text`, with declared vocabulary tokens scrubbed first."""
    scrubbed = text.replace("IGNORE_AS_STALE", "<declared-outcome-token>")
    return [m.group(0).strip() for m in STALE_PREDICATION.finditer(scrubbed)]


def race_row_cells(row):
    """A race row's cells, read the way the invariant must read them.

    Named rather than inlined so the guard can assert this path normalises formatting too: a
    controlled weakening showed that reverting just this call to `plain()` was invisible,
    because the committed row happens to contain no formatted stale text. A guard that only
    watches the helpers and not the reading path is watching half the rule."""
    return [semantic_text(c).strip() for c in row.strip().strip("|").split("|")]


def late_decision_record_stands():
    """Inspect the authoritative race rows, not positive prose elsewhere.

    A late review result may be IGNORE_AS_STALE while remaining recorded against its Review
    Instance. A late Decision Record is an authority-bearing governed act: the record stands,
    and current-state handling must reconcile and/or escalate. The asymmetry is intentional.
    """
    rows = race_rows()
    decision_rows = [r for r in rows if "Decision result after cancellation" in plain(r)]
    review_rows = [r for r in rows if "Review result after supersession" in plain(r)]
    problems = []

    if len(decision_rows) != 1:
        problems.append("expected exactly one late-Decision race row, found %d"
                        % len(decision_rows))
    else:
        # Same normalisation as the Phase-11-wide scan: formatting may not split the subject
        # in the authoritative row either.
        cells = race_row_cells(decision_rows[0])
        if len(cells) != 4:
            problems.append("late-Decision race row does not have four cells")
        else:
            outcome, reason = cells[2], cells[3]
            if "IGNORE_AS_STALE" in outcome:
                problems.append("late Decision Record uses IGNORE_AS_STALE")
            if not any(required in outcome for required in ("RECONCILE", "ESCALATE")):
                problems.append("late Decision Record lacks RECONCILE/ESCALATE handling")
            if not re.search(r"(?i)\b(stands?|retain(?:ed|s|ing)?)\b", reason):
                problems.append("late Decision Record is not explicitly retained / standing")
            forbidden = re.search(
                r"(?i)\b(discard(?:ed|s|ing)?|ignor(?:e|ed|es|ing)|drop(?:ped|s|ping)?|"
                r"eras(?:e|ed|es|ing)|void(?:ed|s|ing)?)\b",
                outcome + " " + reason)
            if forbidden:
                problems.append("late Decision Record is described as discarded: %r"
                                % forbidden.group(0))
            stale = stale_characterisations(outcome + " " + reason)
            if stale:
                problems.append("late Decision Record is itself characterised as stale: %s"
                                % stale)

    if len(review_rows) != 1:
        problems.append("expected exactly one late-review race row, found %d" % len(review_rows))
    else:
        cells = race_row_cells(review_rows[0])
        if len(cells) != 4:
            problems.append("late-review race row does not have four cells")
        else:
            outcome, reason = cells[2], cells[3]
            if "IGNORE_AS_STALE" not in outcome:
                problems.append("late review no longer uses IGNORE_AS_STALE")
            if "record" not in reason.lower() or "Review Instance" not in reason:
                problems.append("late review is not retained against its Review Instance")

    return (not problems, str(problems) if problems
            else "late Decision Record stands with RECONCILE/ESCALATE, never characterised as "
                 "stale; late review keeps IGNORE_AS_STALE, recorded against its Review Instance")


check("concurrency", "late Decision Record stands and remains asymmetric with late review",
      late_decision_record_stands)


def no_decision_record_is_called_stale():
    """Nowhere in Phase 11 may a Decision Record itself be called stale.

    Narrower than the row check and applied everywhere: it fires only where the predication
    names a Decision Record, so stale *evidence* - which is a real and blocking condition in
    this architecture - is untouched."""
    bad = []
    for rel, doc in DOCS.items():
        # Markup normalised, not deleted, and NO line-wide denial exemption: neither a
        # backtick nor a denial elsewhere on the line may speak for a positive stale
        # predicate. Only an explicit specimen fence exempts anything.
        for hit in named_stale_record(assertive_text(doc)):
            bad.append("%s: %s" % (rel, hit[:80]))
    return (not bad, str(bad) if bad
            else "no artifact characterises a Decision Record as stale")


check("concurrency", "no artifact characterises a Decision Record as stale",
      no_decision_record_is_called_stale)


def stale_predication_grammar():
    """The rule, executed rather than described.

    A check is only as good as the cases it was written for, so the cases run here: the
    harness feeds its own matcher the audit's bypass and the wordings the remediation must
    reject, and requires each verdict. Relaxing the patterns fails this without any document
    being edited."""
    # (text, flagged by the row-scoped matcher, flagged by the Phase-11-wide matcher)
    #
    # The contrastive block is the point of this table. Each of those sentences contains a
    # negation, and in each the negation belongs to a DIFFERENT predicate while staleness is
    # asserted anyway. Proximity-based suppression passes every one of them; predicate-attached
    # suppression fails every one of them. Reverting the logic therefore fails this check with
    # no document edited, which is the property the previous two versions of the rule lacked.
    cases = {
        # --- direct negation of the stale predicate: correct wording, must not be flagged
        "is not stale": ("The Decision Record is not stale.", False, False),
        "was not stale": ("The Decision Record was not stale.", False, False),
        "is never stale": ("The Decision Record is never stale.", False, False),
        "not a stale record": ("This is not a stale Decision Record.", False, False),
        # --- unrelated earlier negation, later positive stale predicate: must be flagged
        "not optional but is stale":
            ("The Decision Record stands and is not optional but is stale.", True, True),
        "not optional and is stale":
            ("The Decision Record is not optional and is stale.", True, True),
        "not ignored but is stale":
            ("The Decision Record is not ignored but is stale.", True, True),
        "neither optional nor revocable but is stale":
            ("The Decision Record is neither optional nor revocable but is stale.", True, True),
        "no longer pending but is stale":
            ("The Decision Record is no longer pending but is stale.", True, True),
        "never discarded, but is stale":
            ("The Decision Record is never discarded, but is stale.", True, True),
        # --- the earlier bypasses, still rejected
        "the first audit bypass": ("The Decision Record stands but is stale", True, True),
        "deemed stale": ("The Decision Record was deemed stale", True, True),
        "considered stale": ("The record is considered stale", True, False),
        "marked stale": ("The record is marked stale", True, False),
        "becomes stale": ("The Decision Record becomes stale on cancellation", True, True),
        "treated as stale": ("The Decision Record is treated as stale", True, True),
        "stale Decision Record": ("A stale Decision Record needs no handling", True, True),
        # Sentence-bounded: the phase-wide matcher deliberately does not reach across `;`,
        # which is why the authoritative row - not this net - is the rule that governs.
        "was stale, across a clause boundary":
            ("The Decision Record stands; it was stale by then", True, False),
        # --- Emphasis and strikethrough must not split the governed subject or predicate.
        # Each marker class appears at least once, so dropping any one of them from the
        # normaliser fails this table with no document edited.
        "subject emphasised with asterisks": ("The Decision *Record* is stale.", True, True),
        "subject emphasised with underscores": ("The Decision _Record_ is stale.", True, True),
        "subject strong with asterisks": ("The Decision **Record** is stale.", True, True),
        "subject strong with underscores": ("The Decision __Record__ is stale.", True, True),
        "subject struck through": ("The Decision ~~Record~~ is stale.", True, True),
        "whole subject emphasised": ("The *Decision Record* is stale.", True, True),
        "whole subject underscored": ("The _Decision Record_ is stale.", True, True),
        "whole subject struck through": ("The ~~Decision Record~~ is stale.", True, True),
        "predicate emphasised": ("The Decision Record is *stale*.", True, True),
        "predicate underscored": ("The Decision Record is _stale_.", True, True),
        "predicate struck through": ("The Decision Record is ~~stale~~.", True, True),
        "mixed across subject and predicate":
            ("The *Decision* _Record_ is ~~stale~~.", True, True),
        "mixed with inline code":
            ("The **Decision** `Record` is _stale_.", True, True),
        "formatted attached negation":
            ("The *Decision Record* is not _stale_.", False, False),
        "declared vocabulary survives normalisation":
            ("IGNORE_AS_STALE and NON_RETRYABLE_GOVERNED_ACT are unaffected", False, False),
        # --- Rendering mechanisms a regex cannot see. Each is a class, not an example: a
        # quoted attribute holding a tag terminator, a comment between two visible words, a
        # character reference inside a word, and a link destination with nested parentheses.
        "quoted > inside an attribute":
            ('The Decision <span title="a>b">Record</span> is stale.', True, True),
        "quoted < inside an attribute":
            ('The Decision <span title="a<b">Record</span> is stale.', True, True),
        "comment between the two subject words":
            ("The Decision <!-- aside -->Record is stale.", True, True),
        "comment inside a subject word":
            ("The Decision Rec<!-- x -->ord is stale.", True, True),
        "decimal character reference in the subject":
            ("The Decision Reco&#114;d is stale.", True, True),
        "hexadecimal character reference in the subject":
            ("The Decision Reco&#x72;d is stale.", True, True),
        "named entity inside the predicate":
            ("The Decision Record is st&auml;le.", False, False),
        "nested parentheses in a link destination":
            ("The Decision [Record](#a(b(c))d) is stale.", True, True),
        "nested parentheses and a label link":
            ("The [Decision Record](#see(the(row))) is stale.", True, True),
        "everything at once":
            ("The <em>Decision</em> <!-- x -->[Reco&#114;d](#a(b)) is `~~stale~~`.", True, True),
        "malformed wrapper cannot split the subject":
            ("The Decision <em Record is stale.", True, True),
        # --- A link or an inline HTML tag renders away; it must not split the subject either.
        "subject in a link": ("The Decision [Record](#term) is stale.", True, True),
        "whole subject in a link": ("The [Decision Record](#term) is stale.", True, True),
        "predicate in a link": ("The Decision Record is [stale](#status).", True, True),
        "subject in <em>": ("The Decision <em>Record</em> is stale.", True, True),
        "subject in <strong>": ("The Decision <strong>Record</strong> is stale.", True, True),
        "subject in <code>": ("The Decision <code>Record</code> is stale.", True, True),
        "subject in <span>": ("The Decision <span>Record</span> is stale.", True, True),
        "html across subject and predicate":
            ("The <em>Decision</em> <code>Record</code> is <strong>stale</strong>.", True, True),
        "markdown, html and inline code mixed":
            ("The *Decision* <code>Record</code> is `stale`.", True, True),
        "link, html and emphasis mixed":
            ("The [Decision](#a) <em>Record</em> is ~~stale~~.", True, True),
        "html attached negation":
            ("The <em>Decision Record</em> is not <code>stale</code>.", False, False),
        "benign link making no assertion":
            ("See [the race table](#races) for the outcome vocabulary.", False, False),
        # --- Markdown inline code must not hide an assertion. These are written exactly as
        # they would appear in a document, and are read through the same normalisation the
        # Phase-11-wide scan applies. Deleting code spans - the behaviour this remediation
        # removed - makes every one of them stop being flagged, so reintroducing it fails here
        # with no document edited.
        "stale wrapped in code": ("The Decision Record is `stale`.", True, True),
        "subject half in code": ("The Decision `Record` is stale.", True, True),
        "subject wholly in code": ("The `Decision Record` is stale.", True, True),
        "every token in code": ("The `Decision` `Record` is `stale`.", True, True),
        "deemed, stale in code": ("The Decision Record was deemed `stale`.", True, True),
        "adjectival, subject in code": ("This is a stale `Decision Record`.", True, True),
        "negation survives normalisation": ("The `Decision Record` is not stale.", False, False),
        # --- correct content and unrelated staleness: must stay unflagged
        "the correct wording": ("The Decision Record stands - a human exercised a Right "
                                "and that happened", False, False),
        "the declared token alone": ("IGNORE_AS_STALE - recorded against its request",
                                     False, False),
        "late review, recorded against its Instance":
            ("IGNORE_AS_STALE - recorded against the Review Instance, which remains a true "
             "record of that review", False, False),
        "stale evidence, unrelated to a Decision Record":
            ("Evidence that was current in week one is stale in week six", True, False),
    }
    wrong = []
    for label, (text, row_scoped, phase_wide) in cases.items():
        # Both scopes read normalised text, which is how a real document reaches them: the
        # row cells are normalised by the row check, documents by assertive_text().
        read_as = assertive_text(text)
        if bool(stale_characterisations(read_as)) != row_scoped:
            wrong.append("%s: row-scoped verdict wrong (expected %s)" % (label, row_scoped))
        if bool(named_stale_record(read_as)) != phase_wide:
            wrong.append("%s: phase-wide verdict wrong (expected %s)" % (label, phase_wide))
    return (not wrong, str(wrong) if wrong
            else "%d cases behave as specified in both scopes, the audit bypass rejected" % len(cases))


check("concurrency", "the stale-characterisation matcher rejects every named wording",
      stale_predication_grammar)


def formatting_is_not_an_exemption():
    """Only an explicit fence exempts a specimen; markup never does.

    Asserted against the real reading path, so that reinstating code-span deletion - or
    widening the fence to accept a typographic marker - fails here directly."""
    fenced = ("<!-- stale-specimen -->The Decision Record is `stale`."
              "<!-- /stale-specimen -->")
    problems = []
    # Every supported marker class, asserted twice: the marker must go, the text must stay,
    # and an assertion wearing it must still be caught.
    markers = {
        "inline code": ("`", "`"),
        "emphasis (*)": ("*", "*"),
        "emphasis (_)": ("_", "_"),
        "strong (**)": ("**", "**"),
        "strong (__)": ("__", "__"),
        "strikethrough": ("~~", "~~"),
    }
    for label, (opener, closer) in markers.items():
        wrapped = "a %sformatted span%s here" % (opener, closer)
        normalised = semantic_text(wrapped)
        if any(ch in normalised for ch in "`*_~"):
            problems.append("%s: marker survived normalisation" % label)
        if "formatted span" not in normalised:
            problems.append("%s: normalisation dropped the enclosed text" % label)
        assertion = "The Decision %sRecord%s is stale." % (opener, closer)
        if not named_stale_record(assertive_text(assertion)):
            problems.append("%s: formatting hid an assertion" % label)
    if named_stale_record(assertive_text(fenced)):
        problems.append("an explicitly fenced specimen was read as an assertion")
    # Declared vocabulary must survive: an underscore between alphanumerics is an identifier
    # character, not an emphasis delimiter.
    if semantic_text("IGNORE_AS_STALE") != "IGNORE_AS_STALE":
        problems.append("normalisation damaged the declared vocabulary")
    # The authoritative row's own reading path must normalise too. Asserted through the real
    # helper, so reverting it to a weaker normaliser fails here rather than passing unnoticed
    # because the committed row happens to carry no formatted stale text.
    for label, wrapped in {
        "emphasis": "The Decision *Record* is ~~stale~~",
        "link": "The Decision [Record](#term) is stale",
        "inline HTML": "The Decision <em>Record</em> is stale",
    }.items():
        synthetic = "| 6 | Decision result after cancellation | RECONCILE | %s |" % wrapped
        if not stale_characterisations(" ".join(race_row_cells(synthetic))):
            problems.append("the row's reading path does not normalise %s" % label)
    # The reading ALGORITHM, asserted class by class rather than through phrase examples.
    rendering = {
        "inline link renders to its label":
            ("see [the visible text](#anchor-target)", "see the visible text"),
        "reference link renders to its label":
            ("see [the visible text][ref]", "see the visible text"),
        "nested parentheses in a destination are consumed whole":
            ("see [the label](#a(b(c))d) now", "see the label now"),
        "tag removed, inner text kept":
            ('a <span class="x">wrapped phrase</span> here', "a wrapped phrase here"),
        "a quoted > does not terminate the tag early":
            ('a <span title="a>b">wrapped phrase</span> here', "a wrapped phrase here"),
        "a quoted < does not terminate the tag early":
            ('a <span title="a<b">wrapped phrase</span> here', "a wrapped phrase here"),
        "a comment disappears and its neighbours join":
            ("Reco<!-- hidden -->rd", "Record"),
        "a decimal character reference decodes":
            ("Reco&#114;d", "Record"),
        "a hexadecimal character reference decodes":
            ("Reco&#x72;d", "Record"),
        "a named entity decodes":
            ("caf&eacute;", "caf\u00e9"),
        "an entity that decodes to a marker is then stripped":
            ("a &#96;quoted&#96; word", "a quoted word"),
        "an unbalanced tag does not survive as a splitter":
            ("an <em>unclosed wrapper", "an unclosed wrapper"),
        "declared vocabulary is untouched":
            ("IGNORE_AS_STALE NON_RETRYABLE_GOVERNED_ACT GOVERNANCE_CLEAR",
             "IGNORE_AS_STALE NON_RETRYABLE_GOVERNED_ACT GOVERNANCE_CLEAR"),
        "an unterminated opener does not swallow the rest of the line":
            ("an <em unclosed wrapper here", "an unclosed wrapper here"),
        "an unterminated comment does not swallow the words after it":
            ("Reco<!--rd is stale", "Record is stale"),
        "an unterminated comment cannot reach a terminator in a later paragraph":
            ("The Decision <!--Record is stale.\n\nA later line ends a comment -->here.",
             "The Decision Record is stale. A later line ends a comment here."),
    }
    for label, (raw, expected) in rendering.items():
        # Whitespace is not content: removing a marker can leave a doubled space, and the
        # rule is about what words survive, not about spacing.
        got = " ".join(semantic_text(raw).split())
        if got != " ".join(expected.split()):
            problems.append("%s: read as %r" % (label, got))
    # The invariant the whole path rests on, asserted rather than assumed: presentation may be
    # removed, content may not. Checked over the malformed shapes that tempt a parser to drop
    # a buffer, because that is where the rule is actually at risk.
    for raw in ("The Decision <em Record is stale.",
                "The Decision </em Record is stale.",
                "The Decision <!--Record is stale.",
                "The Decision [Record](#a(b is stale."):
        kept = re.sub(r"[^A-Za-z0-9]", "", semantic_text(raw))
        if "DecisionRecord" not in kept or "stale" not in kept:
            problems.append("content was lost reading %r: %r" % (raw[:44], semantic_text(raw)))
    # Both scopes must consume the same path: the same input must read identically whether it
    # arrives as a document or as a row cell.
    # A malformed opener must be neutralised LOCALLY. In a whole document a later `>` - a
    # blockquote marker will do - used to make a stray `<em` look well-formed, and the parser
    # then swallowed everything between them. Asserted on a document-shaped sample, because
    # that is the only shape in which the bug existed.
    document_shaped = ("Intro line.\n\nThe Decision <em Record is stale.\n\n"
                       "> A later blockquote marker.\n\nA closing line.\n")
    read = assertive_text(document_shaped)
    for word in ("Decision", "Record", "stale", "later blockquote", "closing line"):
        if word not in read:
            problems.append("a malformed opener consumed %r in a full document" % word)
    if not named_stale_record(read):
        problems.append("a malformed opener hid a stale assertion in a full document")
    # The same malformed sample must read identically through both paths.
    malformed = "The Decision <em Record is stale."
    if assertive_text(malformed) != " ".join(race_row_cells("| %s |" % malformed)):
        problems.append("document and row paths differ on a malformed opener")
    for sample in ("The Decision <code>Record</code> is [stale](#s).",
                   'The Decision <span title="a>b">Record</span> is stale.',
                   "The Decision <!-- x -->Reco&#114;d is [stale](#a(b))."):
        if assertive_text(sample) != " ".join(race_row_cells("| %s |" % sample)):
            problems.append("document scan and row path differ on %r" % sample[:40])
    # No architecture document may claim the exemption; it is for review records only.
    misuse = [rel for rel in NORMATIVE if SPECIMEN_FENCE.search(DOCS[rel])]
    if misuse:
        problems.append("architecture documents claiming a specimen fence: %s" % misuse)
    return (not problems, str(problems) if problems
            else "markup is normalised, only an explicit fence exempts, and no architecture "
                 "document claims one")


check("concurrency", "Markdown formatting cannot exempt a stale assertion",
      formatting_is_not_an_exemption)

check("concurrency", "a human intervention wins against automated continuation",
      lambda: (lambda row: (row and "Human wins" in plain(row[0]) and "BLOCK" in row[0], ""))(
          [r for r in race_rows() if "Human intervention" in r]))

check("concurrency", "last-write-wins is absent from the vocabulary",
      lambda: ("Last-write-wins is absent from this vocabulary" in plain(RACE)
               and "Two claimants on one Work Item is a block" in plain(STD), ""))

check("concurrency", "a concurrency limit may delay a dispatch but never skip one",
      lambda: ("may never" in plain(RACE)
               and "a skipped stage is a workflow change" in plain(RACE), ""))

check("concurrency", "ordering rests on causation identifiers, not timestamps",
      lambda: ("Causation identifiers, not timestamps" in plain(RACE)
               and "an audit that can be wrong" in plain(RACE), ""))

# =========================================================== failure / recovery / manual


def distinction_rows():
    body = FAILD.split("## 1. Seven distinctions")[1].split("## 2.")[0]
    return [ln for ln in body.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)][1:]


check("failure", "seven distinctions parse, each with a harm from collapsing it",
      lambda: (lambda rows: (len(rows) == 7 and all(len(r.strip().strip("|").split("|")) == 3
                                                    for r in rows),
                             "%d distinctions" % len(rows)))(distinction_rows()))

REQUIRED_PAIRS = ["PAUSE vs BLOCK", "CANCEL vs TERMINATE", "RETRY vs REWORK",
                  "ESCALATE vs HUMAN REVIEW", "FAIL vs BLOCKED", "SUPERSEDE vs CANCEL",
                  "Compensation vs rollback"]
check("failure", "every required distinction is stated",
      lambda: (lambda missing: (not missing, str(missing) if missing else "7 pairs"))(
          [p for p in REQUIRED_PAIRS if p not in plain(FAILD)]))


def stop_condition_rows():
    body = FAILD.split("## 4. Twelve stop conditions")[1].split("## 5.")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("failure", "twelve stop conditions parse, each with an outcome",
      lambda: (lambda rows: (len(rows) == 12 and all(
          re.search(r"BLOCK|ESCALAT|REWORK|TERMINAT|RECONCILE", r) for r in rows),
          "%d stop conditions" % len(rows)))(stop_condition_rows()))

REQUIRED_STOPS = ["No applicable Decision Right", "unresolved conflict", "NOT_SATISFIED",
                  "Stale or expired blocking evidence", "Scope mismatch",
                  "residency constraint", "destructive action without a named authority",
                  "Ambiguous identity or version", "Failed integrity check",
                  "Unknown model eligibility", "termination race",
                  "External side-effect uncertainty"]
check("failure", "every required stop condition is present",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d conditions" % len(REQUIRED_STOPS)))(
          [s for s in REQUIRED_STOPS if s.lower() not in plain(FAILD).lower()]))

check("failure", "no distributed transaction is claimed across the systems",
      lambda: ("has no distributed transaction, and none is claimed" in plain(FAILD)
               and "declared commit order" in plain(FAILD).lower()
               and "reconciliation owner" in plain(FAILD), ""))

check("failure", "external side-effect uncertainty stops the run",
      lambda: ("Never assumed in either direction" in plain(FAILD), ""))

check("failure", "no failure path weakens a constraint",
      lambda: ("No failure path weakens a constraint" in plain(STD)
               and "No failure path weakens a constraint" in plain(FAILD)
               and "where the pressure to break it is highest" in plain(FAILD), ""))

check("failure", "a resume compares rather than assumes, and re-enters current constraints",
      lambda: ("A resume is a governed event" in plain(FAILD)
               and "resumes into the new constraints" in plain(FAILD), ""))


def intervention_rows():
    body = MANUAL.split("## 2. Six permitted acts")[1].split("## 3.")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("manual", "six intervention acts parse, each stating whether a Right is required",
      lambda: (lambda rows: (len(rows) == 6 and all(
          re.search(r"(?i)\byes\b|\bno\b", plain(r.strip().strip("|").split("|")[3]))
          for r in rows), "%d acts" % len(rows)))(intervention_rows()))

check("manual", "an intervention record names the human and the system identity separately",
      lambda: ("Not the account, and not the service identity" in plain(MANUAL)
               and "two identities are always recorded and never merged"
               in plain(MANUAL).lower(), ""))

check("manual", "an operational exception requires a named Right and touches no requirement",
      lambda: ("There is no intervention that adjusts a governed requirement" in plain(MANUAL)
               and "that adjustment is a Phase 7 governed exception" in plain(MANUAL), ""))

check("manual", "intervention cannot convert a refusal into a continuation",
      lambda: (all(t in MANUAL for t in ["NOT_SATISFIED", "DEFER", "ESCALATE", "EXPIRED",
                                         "NO_APPLICABLE_DECISION_RIGHT"])
               and "into a continuation" in plain(MANUAL), ""))

check("manual", "intervention cannot edit or delete governed history",
      lambda: ("edits or deletes an execution event" in plain(MANUAL)
               and "Interventions are append-only" in plain(MANUAL), ""))

check("manual", "seniority is not authority where no Right exists",
      lambda: ("no amount of seniority substitutes" in plain(MANUAL), ""))

# =========================================================== audit / provenance

HISTORIES = ["Operational runtime event", "Execution event", "Audit event", "Decision Record",
             "Review result", "Routing Decision", "Knowledge provenance",
             "Git architecture history"]
check("audit", "eight histories are kept apart, none substituting for another",
      lambda: (all(h in plain(AUDIT) for h in HISTORIES)
               and "An execution event is not an audit event" in plain(AUDIT),
               "%d histories" % len(HISTORIES)))


def execution_event_fields():
    body = AUDIT.split("## 2. The execution event")[1].split("## 3.")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("audit", "the execution event carries thirteen fields",
      lambda: (lambda n: (n == 13, "%d fields" % n))(len(execution_event_fields())))

check("audit", "an operational log is never governance evidence",
      lambda: ("An operational log is never governance evidence" in plain(STD)
               and "Never governance evidence" in plain(AUDIT), ""))


def logs_never_cited_as_evidence():
    bad = []
    for rel, doc in DOCS.items():
        flat = plain(doc)
        for m in re.finditer(r"(?i)(operational )?log[^.\n]{0,40}\b(evidence|proof|proves)\b",
                             flat):
            if DENIAL_MARKER.search(line_of(flat, m.start())):
                continue
            bad.append("%s: %s" % (rel, m.group(0)[:70]))
    return (not bad, str(bad) if bad else "no artifact treats a log as evidence")


check("audit", "no artifact turns an operational log into evidence", logs_never_cited_as_evidence)

check("audit", "the execution event stream is append-only",
      lambda: ("no update and no delete operation to grant" in plain(AUDIT)
               and "Governed history is never rewritten" in plain(STD), ""))

check("audit", "an unenforceable immutability claim is recorded as a gap",
      lambda: ("the limitation is recorded rather than assumed away" in plain(AUDIT), ""))

check("audit", "an authority reference is required for the event classes that need one",
      lambda: ("Absent is a failure for those classes" in plain(AUDIT), ""))

check("audit", "a historical execution reconstructs its definitions and versions",
      lambda: ("Reconstructing a historical execution" in plain(AUDIT)
               and "recorded value in the event stream" in plain(AUDIT)
               and "Reproducibility is by recorded reference" in plain(STD), ""))

check("audit", "Phase 11 relocates no governed object",
      lambda: ("Nothing in Phase 11 relocates a governed object" in plain(AUDIT)
               and "The orchestrator references them; it does not hold them" in plain(AUDIT), ""))

# =========================================================== provider independence


def adapter_rows():
    body = INDEP.split("## 2. Five adapter boundaries")[1].split("## 3.")[0]
    return [ln for ln in body.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)][1:]


check("independence", "five adapter boundaries split portable from engine-specific",
      lambda: (lambda rows: (len(rows) == 5 and all(len(r.strip().strip("|").split("|")) == 3
                                                    for r in rows),
                             "%d boundaries" % len(rows)))(adapter_rows()))

check("independence", "an adapter isolates a mechanism, never a meaning",
      lambda: ("It never isolates a meaning" in plain(INDEP)
               and "no queue decides whether a retry is safe" in plain(INDEP), ""))

check("independence", "the replacement test is stated so it can be applied",
      lambda: ("if the execution engine were replaced tomorrow" in plain(INDEP), ""))

check("independence", "determinism is bounded honestly",
      lambda: ("Determinism is bounded and stated" in plain(A)
               and "Not deterministic, and not claimed to be" in plain(INDEP), ""))

# =========================================================== trigger intake


def intake_rows():
    body = A.split("## 5. Trigger intake and validation")[1].split("## 6.")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("intake", "intake validates before anything is scheduled",
      lambda: (lambda rows: (len(rows) == 7 and "a trigger is a request, not a start"
                             in plain(A), "%d intake checks" % len(rows)))(intake_rows()))

check("intake", "unassessed sensitivity is restricted, never permissive",
      lambda: ("unassessed is restricted, never permissive" in plain(A), ""))

check("intake", "a failing trigger is refused rather than started and blocked later",
      lambda: ("recorded refusal" in plain(A)
               and "has already consumed assignments" in plain(A), ""))

# =========================================================== templates and exemplars

check("templates", "three templates are present and remain PROPOSED",
      lambda: (len(TEMPLATES) == 3 and all("Status: PROPOSED" in DOCS[t] for t in TEMPLATES),
               "%d: %s" % (len(TEMPLATES), [os.path.basename(t) for t in TEMPLATES])))

check("templates", "every template inherits the standard",
      lambda: (all("standard.orchestration.common_constraints" in DOCS[t] for t in TEMPLATES),
               ""))

check("templates", "the standard's numbering is contiguous from 1",
      lambda: (lambda nums: (nums == list(range(1, len(nums) + 1)),
                             "%d contiguous rules" % len(nums)))(
          [int(n) for n in re.findall(r"^## (\d+)\. ", STD, re.M)]))

check("templates", "the policy template enumerates what it cannot declare",
      lambda: ("What this policy cannot declare" in plain(TMPL["orchestrator-policy-template.md"])
               and "exactly-once is guaranteed"
               in plain(TMPL["orchestrator-policy-template.md"]), ""))

check("exemplars", "six exemplars on disk, each PROPOSED and synthetic",
      lambda: (len(EXEMPLARS) == 6
               and all("Status: PROPOSED" in DOCS[e] for e in EXEMPLARS)
               and all("synthetic" in plain(DOCS[e]).lower() for e in EXEMPLARS),
               "%d: %s" % (len(EXEMPLARS), [os.path.basename(e) for e in EXEMPLARS])))

EXEMPLAR_PROOFS = {
    "normal-multi-stage-with-gates.md": "through",
    "critical-independence-enforced.md": "two controls",
    "partial-failure-before-metadata.md": "neither half is ever completed by inventing the other",
    "cancellation-racing-late-results.md": "recorded rather than applied",
    "missing-decision-right-blocks.md": "never an inference",
    "long-running-resume-stale-evidence.md": "compares rather than assumes",
}
for _fname, _needle in EXEMPLAR_PROOFS.items():
    check("exemplars", "exemplar %s states what it proves" % _fname.replace(".md", ""),
          (lambda f=_fname, n=_needle: ("orchestration/exemplars/" + f in DOCS
                                        and n in plain(DOCS["orchestration/exemplars/" + f]),
                                        "")))

check("exemplars", "the missing-Right exemplar blocks and names what did not happen",
      lambda: (lambda d: ("NO_APPLICABLE_DECISION_RIGHT" in d and "AUTHORITY_ABSENT" in d
                          and "Five things that did not happen" in plain(d)
                          and "a Phase 7 governance extension" in plain(d), ""))(
          DOCS["orchestration/exemplars/missing-decision-right-blocks.md"]))

check("exemplars", "the cancellation exemplar keeps the late Decision Record",
      lambda: (lambda d: ("The Decision Record stands" in plain(d)
                          and "IGNORE_AS_STALE" in d and "RECONCILE" in d, ""))(
          DOCS["orchestration/exemplars/cancellation-racing-late-results.md"]))

check("exemplars", "the independence exemplar blocks rather than relaxing a class",
      lambda: (lambda d: ("BLOCKED" in d and "there is no partial independence" in plain(d)
                          and "Seeing a conflict and being allowed to resolve it are different"
                          in plain(d), ""))(
          DOCS["orchestration/exemplars/critical-independence-enforced.md"]))

# =========================================================== regression / hygiene

for _label, _paths in UPSTREAM_PATHS.items():
    check("regression", "%s unchanged since the Phase 10 approval baseline" % _label,
          (lambda p=_paths: (lambda r: (r[0], ", ".join(r[1]) or "clean"))(git_unchanged(p))))

APPROVAL_RECORD = re.compile(r"(?:^|/)phase-\d+-final-approval\.md$")


def architecture_artifacts_only(docs):
    """A human approval record is a different kind of object from an architecture artifact:
    it is *supposed* to say APPROVED, and it is not a Phase 11 proposal. Running the Phase 10
    harness during this pass showed what happens without this exemption - it reports its own
    phase's approval record as a defect. Exempted here, and required to be a real approval."""
    out, malformed = {}, []
    for rel, doc in docs.items():
        if APPROVAL_RECORD.search(rel):
            if "HUMAN DECISION" not in doc:
                malformed.append(rel)
            continue
        out[rel] = doc
    return out, malformed


def artifacts_remain_proposed():
    docs, malformed = architecture_artifacts_only(DOCS)
    bad = [rel for rel, doc in docs.items()
           if not re.search(r"^Status: (\*\*)?PROPOSED", doc, re.M)]
    return (not bad and not malformed, str(bad + malformed) if (bad or malformed)
            else "%d architecture artifacts, all PROPOSED" % len(docs))


check("regression", "every Phase 11 architecture artifact remains PROPOSED",
      artifacts_remain_proposed)


def no_approval_claimed():
    docs, _ = architecture_artifacts_only(DOCS)
    bad = [rel for rel, doc in docs.items()
           if re.search(r"Status:[^\n]*\b(APPROVED|CANONICAL)\b", doc)]
    return (not bad, str(bad) if bad else "0 approval claims")


check("regression", "no Phase 11 architecture artifact claims APPROVED or CANONICAL status",
      no_approval_claimed)

check("regression", "Phase 11 states that it changes no approved semantics",
      lambda: ("Phase 11 changes no approved semantics" in plain(STD)
               and "It adds no governance semantics" in plain(A), ""))

# --- self-inspection region (excluded from its own scans) ---
RUNTIME = re.compile(  # self-literal
    r"\b(import celery|import kombu|import temporalio|from airflow|"  # self-literal
    r"CREATE TABLE|ALTER TABLE|DROP TABLE|INSERT INTO|SELECT \*|CREATE POLICY|"  # self-literal
    r"api[_-]?key|bearer token|POST /|https?://|"  # self-literal
    r"@app\.task|BEGIN;|pip install|npm install|docker run)\b", re.I)  # self-literal
SECRET_SHAPES = re.compile(  # self-literal
    r"(?:BEGIN [A-Z ]*PRIVATE KEY|"  # self-literal
    r"postgres(?:ql)?://[^\s]+:[^\s]+@|"  # self-literal
    r"\b(?:password|passwd|secret|token)\s*[:=]\s*['\"][^'\"\s]{8,})", re.I)  # self-literal
SELF_START = "# --- self-inspection region (excluded from its own scans) ---"
SELF_END = "# --- end self-inspection region ---"
# --- end self-inspection region ---


def harness_body():
    """This file minus the region holding the patterns, so a scan cannot match its own text."""
    kept, skipping = [], False
    for line in read("validation/phase_11_validation.py").splitlines():
        if line.strip() == SELF_START:
            skipping = True
            continue
        if line.strip() == SELF_END:
            skipping = False
            continue
        if skipping or line.rstrip().endswith("# self-literal"):
            continue
        kept.append(line)
    return "\n".join(kept)


def no_runtime_implementation():
    # No suppression: these are executable constructs, not vocabulary. An architecture
    # document has no legitimate reason to contain one, denied or otherwise.  # self-literal
    hits = []
    for rel, doc in DOCS.items():
        for m in RUNTIME.finditer(doc):
            hits.append("%s: %s" % (rel, m.group(0)))
    for m in RUNTIME.finditer(harness_body()):
        hits.append("harness: %s" % m.group(0))
    return (not hits, str(sorted(set(hits))) if hits else "0 runtime constructs")


check("regression", "no orchestrator, queue, engine, schema or client is implemented",
      no_runtime_implementation)


def no_committed_secret():
    hits = []
    for rel, doc in DOCS.items():
        for m in SECRET_SHAPES.finditer(doc):
            hits.append("%s: %s" % (rel, m.group(0)[:40]))
    for m in SECRET_SHAPES.finditer(harness_body()):
        hits.append("harness: %s" % m.group(0)[:40])
    return (not hits, str(hits) if hits else "0 secret-shaped strings in any Phase 11 artifact")


check("regression", "no secret, key or credential shape appears in any artifact",
      no_committed_secret)


def no_vacuous_checks():
    """A check that cannot fail is worse than a missing one: it reports confidence."""
    t = "Tr" + "ue"
    patterns = {"or-true": r"\bor %s\b" % t,
                "or-not-false": r"\bor not Fa" + r"lse\b",
                "lambda-true": r"lambda:\s*\(?%s\)?\s*[,)]" % t,
                "assert-true": r"\bassert %s\b" % t,
                "hard-coded pass count": r"passed\s*=\s*\d+"}
    body = harness_body()
    found = [label for label, pat in patterns.items() if re.search(pat, body)]
    return (not found, str(found) if found
            else "0 vacuous constructs across %d patterns" % len(patterns))


check("regression", "harness contains no vacuous or unconditional-pass checks", no_vacuous_checks)


def harness_is_read_only():
    body = harness_body()
    writes = re.findall(r"open\([^)]*['\"][wa]['\"]", body) + re.findall(r"\bos\.remove\b", body)
    gitcmds = set(re.findall(r'"git", "(\w+)"', body))
    return (not writes and gitcmds <= {"diff", "status", "log", "rev-parse"},
            "writes=%d, git verbs=%s" % (len(writes), sorted(gitcmds)))


check("regression", "harness writes nothing and runs only read-only git", harness_is_read_only)


def no_local_pr_action():
    """Honest scope: a local script cannot prove a remote open-PR count and does not claim to."""
    claims_remote = re.search(r"(?i)no open (pull request|pr)s? (exist|remain)", harness_body())
    return (claims_remote is None,
            "LOCAL ONLY - remote open-PR state is NOT provable offline and is not claimed")


check("regression", "the harness makes no claim about remote pull-request state",
      no_local_pr_action)

# =========================================================== derived inventory


def inventory_rows():
    body = A.split("| Vocabulary | Members | Owner document |")[1]
    rows = {}
    for line in body.splitlines():
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [plain(c).strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        m = re.match(r"(\d+)", cells[1])
        if m:
            rows[cells[0]] = int(m.group(1))
    return rows


AUTHORITATIVE = {
    "Identity chain objects": len(SEPARATED),
    "Runtime identity kinds": len([ln for ln in RUN.split("## 2. Fifteen runtime identity kinds")[1]
                                   .split("## 3.")[0].splitlines()
                                   if re.match(r"^\| \d+ \|", ln)]),
    "Run phases (non-terminal)": len(axis_rows("## 2. Axis A", "## 3. Axis B")),
    "Terminal outcomes": len(axis_rows("## 3. Axis B", "## 4. Axis C")),
    "Wait reasons": len(WAITS),
    "Governance postures": len(axis_rows("## 5. Axis D", "## 6. Transitions")),
    "Dependency kinds": len(dependency_rows()),
    "Dispatch kinds": len(dispatch_rows()),
    "Assignment envelope fields": len(envelope_rows()),
    "Gate outcomes": len(gate_outcome_rows()),
    "Retry classes": len(retry_rows()),
    "Race cases": len(race_rows()),
    "Race outcomes": len(RACE_OUTCOMES),
    "Failure distinctions": len(distinction_rows()),
    "Stop conditions": len(stop_condition_rows()),
    "Intervention acts": len(intervention_rows()),
    "Execution event fields": len(execution_event_fields()),
    "History kinds": len(HISTORIES),
    "Adapter boundaries": len(adapter_rows()),
    "Common orchestrator constraints": len(re.findall(r"^## (\d+)\. ", STD, re.M)),
    "Templates": len(TEMPLATES),
    "Exemplars": len(EXEMPLARS),
}

check("inventory", "every authoritative count is derived from a parsed source",
      lambda: (all(isinstance(v, int) and v > 0 for v in AUTHORITATIVE.values()),
               ", ".join("%s=%d" % kv for kv in sorted(AUTHORITATIVE.items()))))


def inventory_reconciled():
    rows = inventory_rows()
    missing = [k for k in AUTHORITATIVE if k not in rows]
    if missing:
        return (False, "inventory rows not found, so nothing was compared: %s" % missing)
    wrong = ["%s states %d, authoritative %d" % (k, rows[k], AUTHORITATIVE[k])
             for k in AUTHORITATIVE if rows[k] != AUTHORITATIVE[k]]
    return (not wrong, str(wrong) if wrong
            else "%d inventory rows reconciled against parsed sources" % len(AUTHORITATIVE))


check("inventory", "the master inventory table reconciles with every parsed source",
      inventory_reconciled)

NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
                "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
                "nineteen": 19, "twenty": 20, "twenty-one": 21, "twenty-two": 22, "thirty": 30}


def as_number(token):
    token = token.strip().lower()
    return int(token) if token.isdigit() else NUMBER_WORDS.get(token)


PROSE_CLAIMS = [
    (r"(\S+)[- ]object separation chain", "Identity chain objects"),
    (r"(\S+) runtime identity kinds", "Runtime identity kinds"),
    (r"(\S+) dependency kinds", "Dependency kinds"),
    (r"(\S+) dispatch kinds", "Dispatch kinds"),
    (r"(\S+) gate outcomes", "Gate outcomes"),
    (r"(\S+) retry classes", "Retry classes"),
    (r"(\S+) races\b", "Race cases"),
    (r"(\S+) distinctions that are routinely collapsed", "Failure distinctions"),
    (r"(\S+) stop conditions", "Stop conditions"),
    (r"(\S+) permitted acts", "Intervention acts"),
    (r"(\S+) histories", "History kinds"),
    (r"(\S+) adapter boundaries", "Adapter boundaries"),
    (r"(\S+) exemplars", "Exemplars"),
    (r"(\S+) templates", "Templates"),
]


def prose_counts_reconciled():
    bad = []
    for rel, doc in DOCS.items():
        flat = plain(doc)
        for pattern, key in PROSE_CLAIMS:
            for m in re.finditer(pattern, flat, re.I):
                stated = as_number(m.group(1))
                if stated is None or stated == AUTHORITATIVE[key]:
                    continue
                bad.append("%s: '%s' (%s is %d)"
                           % (rel, m.group(0).strip(), key, AUTHORITATIVE[key]))
    return (not bad, str(sorted(set(bad))) if bad
            else "%d quantities reconciled across %d documents" % (len(AUTHORITATIVE), len(DOCS)))


check("inventory", "every prose count reconciles with its parsed source", prose_counts_reconciled)


def heading_list_cardinality():
    words = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
             "Eight": 8, "Nine": 9, "Ten": 10, "Eleven": 11, "Twelve": 12, "Thirteen": 13,
             "Fifteen": 15}
    bad = []
    for rel, doc in DOCS.items():
        for m in re.finditer(r"^#{2,3} (?:\d+\.?\w?\. )?(%s) ([a-z][^\n]*)$"
                             % "|".join(words), doc, re.M):
            claimed = words[m.group(1)]
            body = doc[m.end():].split("\n## ")[0].split("\n### ")[0]
            numbered = len(re.findall(r"^\d+\. ", body, re.M))
            rows = [ln for ln in body.splitlines()
                    if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)]
            table_items = max(0, len(rows) - 1) if rows else 0
            items = numbered or table_items
            if items and items != claimed:
                bad.append("%s: '%s %s' governs %d" % (rel, m.group(1), m.group(2)[:40], items))
    return (not bad, str(bad) if bad else "headings match their lists")


check("inventory", "a heading claiming N items governs a list of N", heading_list_cardinality)


# --- this check must stay last: it counts the suite, itself included ---
_PENDING_FINAL_CHECKS = 1                                              # self-literal


def _freeze_final_counts():
    groups = {}
    for r in RESULTS:
        groups[r["group"]] = groups.get(r["group"], 0) + 1
    groups["inventory"] = groups.get("inventory", 0) + _PENDING_FINAL_CHECKS
    return groups, sum(groups.values())


FINAL_GROUPS, FINAL_TOTAL = _freeze_final_counts()
SELF_CHECK = "reviews/phase-11-foundation-self-check.md"


def self_check_is_current():
    """The producer self-check may not state a total or group count the suite does not produce."""
    if len(RESULTS) + 1 != FINAL_TOTAL:
        return (False, "the frozen suite shape has drifted: registry holds %d, frozen %d"
                % (len(RESULTS) + 1, FINAL_TOTAL))
    if SELF_CHECK not in DOCS:
        return (False, "no producer self-check found, so nothing was compared")
    doc = DOCS[SELF_CHECK]
    problems = []
    totals = [(int(a), int(b)) for a, b in re.findall(r"\b(\d{2,4})/(\d{2,4})\b", doc)]
    if not totals:
        problems.append("the self-check states no total")
    problems += ["stale total %d/%d" % f for f in totals if f != (FINAL_TOTAL, FINAL_TOTAL)]
    stated = {m.group(1): int(m.group(2))
              for m in re.finditer(r"^\| `([a-z-]+)` \| (\d+) \|", doc, re.M)}
    if not stated:
        problems.append("the self-check states no per-group counts")
    problems += ["%s states %d, suite emits %d" % (g, n, FINAL_GROUPS[g])
                 for g, n in sorted(stated.items())
                 if g in FINAL_GROUPS and n != FINAL_GROUPS[g]]
    problems += ["no such group: %s" % g for g in sorted(stated) if g not in FINAL_GROUPS]
    problems += ["group not stated: %s" % g for g in sorted(FINAL_GROUPS) if g not in stated]
    return (not problems, str(problems) if problems
            else "%d/%d and all %d group counts reconcile with the result registry"
            % (FINAL_TOTAL, FINAL_TOTAL, len(FINAL_GROUPS)))


check("inventory", "the producer self-check states the suite's actual totals",
      self_check_is_current)


def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv
    passed = sum(1 for r in RESULTS if r["pass"])
    if as_json:
        print(json.dumps({"total": len(RESULTS), "passed": passed, "results": RESULTS}, indent=2))
    else:
        # Grouped by label in order of first appearance, so a check registered later in the
        # file - the identity-contradiction scan needs the rendered-text helpers - still
        # prints under its own group once rather than reopening it.
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
