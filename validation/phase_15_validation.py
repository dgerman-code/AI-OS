"""Phase 15 — intent and work planning architecture validator.

Status: PROPOSED. Standard library only, deterministic, no network, no third-party imports.

    python3 validation/phase_15_validation.py [--verbose] [--json]

This harness is an ASSURANCE TOOL AND NEVER GOVERNANCE AUTHORITY. A passing check is evidence
that a check passed. It approves nothing, satisfies no review, creates no Decision Right, and
does not make the Phase 15 architecture correct.

It tests substantive cross-document consistency: that the planning layer never acquires authority
it is forbidden, that a Work Plan never becomes a Workflow, that confidence never substitutes for
governance, and that every identifier the package cites resolves against approved architecture.
It cannot test that the architecture is *right*; that is what the independent review is for.

It modifies no approved validator and reads no Phase 14 artifact.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PLANNING = os.path.join(REPO, "planning")

RESULTS = []

#: The architecture document lives under planning/ with the rest of the package. It is NOT
#: placed under architecture/: the approved Phase 12 validator treats every path under
#: architecture/ as inherited and counts an added file there as a change to approved material,
#: which took Phase 12 from 55/55 to 54/55. See planning/phase-15-self-check.md §2a.
ARCHITECTURE_DOC = os.path.join("planning", "intent-work-planning-architecture.md")

PLANNING_DOCS = (
    "request-intent-model.md",
    "context-scope-resolution.md",
    "work-classification-and-criticality.md",
    "role-skill-requirement-inference.md",
    "workflow-matching-and-composition.md",
    "work-plan-object-model.md",
    "clarification-policy.md",
    "governance-preflight.md",
    "orchestrator-handoff-contract.md",
    "failure-and-escalation-model.md",
    "workflow-candidate-learning-boundary.md",
    "user-experience-contract.md",
    "exemplars.md",
    "open-items.md",
    "phase-15-self-check.md",
)


def read(relative):
    with open(os.path.join(REPO, relative), encoding="utf-8") as handle:
        return handle.read()


def doc(name):
    """A Phase 15 document, by its short name."""
    if name.endswith("intent-work-planning-architecture.md"):
        return read(ARCHITECTURE_DOC)
    return read(os.path.join("planning", name))


def all_docs():
    return (ARCHITECTURE_DOC.split(os.sep)[-1],) + PLANNING_DOCS


def flat(text):
    """Markdown-insensitive form: emphasis stripped, whitespace collapsed, lowercased."""
    text = text.replace("*", "").replace("`", "").replace("—", " ")
    text = re.sub(r"(?m)^\s*>+\s?", " ", text)
    text = re.sub(r"(?m)^\s*[-*+]\s+", " ", text)
    return " ".join(text.split()).lower()


def says(name, *phrases):
    body = flat(doc(name))
    return [p for p in phrases if flat(p) not in body]


#: A statement that DESCRIBES a prohibited thing in order to forbid it. A scan over every
#: sentence has to be able to tell "the planner may not select a model" from "the planner
#: selects a model", and the marker is the denial or the corrective frame.
CORRECTIVE = re.compile(
    r"\b(never|not|no|none|cannot|must not|may not|prohibit\w*|forbid\w*|refus\w*|"
    r"excluded|instead|rather|would be|would have|is prohibited|is excluded|"
    r"deliberately|wrong|failure mode|defect|violat\w*|tempt\w*|nothing|"
    r"inert|only|never means|is not)\b", re.IGNORECASE)


def statements(name):
    """(line, statement): a table ROW is one statement, a bullet is one, prose splits by sentence.

    A row's columns answer each other - an exemplar row's scenario cell is answered by its
    outcome cell - so splitting a row reads the scenario as a claim. A bullet merged into the
    paragraph around it would acquire every qualifier its neighbours carry."""
    fenced = False
    buffer, start = [], None
    units = []
    for i, line in enumerate(doc(name).splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            if buffer:
                units.append((start, " ".join(buffer)))
                buffer, start = [], None
            continue
        if fenced:
            units.append((i, line))
            continue
        if line.lstrip().startswith("|") or re.match(r"\s*[-*+]\s+\S", line):
            if buffer:
                units.append((start, " ".join(buffer)))
                buffer, start = [], None
            units.append((i, line))
            continue
        if not line.strip():
            if buffer:
                units.append((start, " ".join(buffer)))
                buffer, start = [], None
            continue
        if start is None:
            start = i
        buffer.append(line)
    if buffer:
        units.append((start, " ".join(buffer)))
    for i, unit in units:
        if unit.lstrip().startswith("|"):
            yield i, unit
        else:
            for sentence in re.split(r"(?<=[.;])\s+", unit):
                if sentence.strip():
                    yield i, sentence


def check(group, name, fn):
    try:
        ok, evidence = fn()
    except Exception as exc:                                   # noqa: BLE001
        ok, evidence = False, "%s: %s" % (type(exc).__name__, exc)
    RESULTS.append({"group": group, "name": name, "pass": bool(ok),
                    "evidence": str(evidence)[:400]})


# =========================================================== structure


def every_required_document_exists():
    missing = [ARCHITECTURE_DOC] if not os.path.exists(os.path.join(REPO, ARCHITECTURE_DOC)) else []
    missing += [d for d in PLANNING_DOCS
                if not os.path.exists(os.path.join(PLANNING, d))]
    return (not missing, str(missing) if missing
            else "%d Phase 15 documents present" % (len(PLANNING_DOCS) + 1))


check("structure", "every required Phase 15 document exists", every_required_document_exists)


def every_document_remains_proposed():
    wrong = [d for d in all_docs() if "Status: `PROPOSED`" not in doc(d)[:600]]
    return (not wrong, str(wrong) if wrong
            else "all %d documents are PROPOSED" % (len(PLANNING_DOCS) + 1))


check("structure", "every Phase 15 document remains PROPOSED", every_document_remains_proposed)


def nothing_claims_approved_or_canonical():
    pattern = re.compile(r"^\s*Status:.*\b(APPROVED|CANONICAL)\b", re.MULTILINE)
    offenders = [d for d in all_docs() if pattern.search(doc(d))]
    return (not offenders, str(offenders) if offenders
            else "no Phase 15 document declares itself APPROVED or CANONICAL")


check("structure", "no Phase 15 document claims APPROVED or CANONICAL status",
      nothing_claims_approved_or_canonical)


def the_package_contains_only_documents():
    unexpected = [f for f in os.listdir(PLANNING) if not f.endswith(".md")]
    return (not unexpected, str(unexpected) if unexpected
            else "the planning package is %d markdown documents and nothing else"
                 % len(PLANNING_DOCS))


check("structure", "the planning package contains only documents",
      the_package_contains_only_documents)


BASELINE = "2c4b90def9a60f8b384feef10f8428c5b437597c"


def merge_base():
    """Where this branch left approved architecture.

    Bounds the containment claim honestly: this shows the branch changed no approved artifact,
    NOT that the branch carries every later approved artifact."""
    result = subprocess.run(["git", "merge-base", "HEAD", BASELINE],
                            cwd=REPO, capture_output=True, text=True)
    return result.stdout.strip() or BASELINE


def changed_paths():
    tracked = subprocess.run(["git", "diff", "--name-only", merge_base(), "--"],
                             cwd=REPO, capture_output=True, text=True).stdout.splitlines()
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"],
                               cwd=REPO, capture_output=True, text=True).stdout.splitlines()
    return sorted({n for n in tracked + untracked if n.strip()})


def no_approved_artifact_is_changed():
    allowed = ("planning/", "prompts/", "validation/phase_15_")
    offenders = [n for n in changed_paths() if not n.startswith(allowed)]
    return (not offenders, str(offenders[:6]) if offenders
            else "only the planning package, its prompt and its own validator are added")


check("containment", "no approved Phase 1-13 artifact is changed", no_approved_artifact_is_changed)


def no_phase_14_file_is_changed():
    offenders = [n for n in changed_paths()
                 if n.startswith("implementation-spec/") or "phase_14" in n]
    return (not offenders, str(offenders[:6]) if offenders
            else "no Phase 14 specification or validator file is touched")


check("containment", "no Phase 14 file is changed", no_phase_14_file_is_changed)


def no_runtime_implementation_is_added():
    forbidden_ext = (".sql", ".yaml", ".yml", ".tf", ".toml", ".ini", ".cfg", ".env",
                     ".pem", ".key", ".lock", ".ts", ".js", ".go", ".rs")
    forbidden_name = ("Dockerfile", "docker-compose.yml", "requirements.txt", "package.json",
                      "pyproject.toml", "Makefile")
    offenders = [n for n in changed_paths()
                 if os.path.basename(n) in forbidden_name
                 or os.path.splitext(n)[1].lower() in forbidden_ext]
    return (not offenders, str(offenders) if offenders
            else "no runtime, infrastructure or dependency artifact is added")


check("containment", "no runtime or infrastructure artifact is added",
      no_runtime_implementation_is_added)


def every_document_disclaims_runtime():
    missing = [d for d in all_docs()
               if "non-runtime statement" not in flat(doc(d))]
    return (not missing, str(missing) if missing
            else "every document carries a non-runtime statement")


check("containment", "every document carries a non-runtime statement",
      every_document_disclaims_runtime)


# =========================================================== identity separation


def approved_ids(pattern, directory):
    found = set()
    root = os.path.join(REPO, directory)
    for base, _dirs, files in os.walk(root):
        for f in files:
            if f.endswith(".md"):
                with open(os.path.join(base, f), encoding="utf-8") as handle:
                    found |= set(re.findall(pattern, handle.read()))
    return found


def cited_ids(pattern):
    found = set()
    for d in all_docs():
        found |= set(re.findall(pattern, doc(d)))
    return found


def every_cited_identifier_resolves():
    """A planner that cited a Role it invented would have invented a Role.

    Every governed identifier the package names is resolved against the approved registries on
    this branch. There is no allowance for a described capability or a synthesised id."""
    problems = []
    for label, pattern, directory in (
            ("role", r"\brole\.[a-z_0-9]+", "roles"),
            ("skill", r"\bskill\.[a-z_0-9]+", "skills"),
            ("review", r"\breview\.[a-z_0-9]+", "reviews"),
            ("decision", r"\bdecision\.[a-z_0-9]+", "decisions"),
            ("workflow", r"\bworkflow\.[a-z_0-9]+", "workflows")):
        approved = approved_ids(pattern, directory)
        for cited in sorted(cited_ids(pattern)):
            if cited in approved:
                continue
            # `workflow.<id>` appears as a metavariable in prose about identity spaces.
            if cited.endswith(".<id>") or "<" in cited:
                continue
            problems.append("%s: %s resolves against no approved registry" % (label, cited))
    return (not problems, str(problems)[:400] if problems
            else "every cited role, skill, review, decision and workflow identifier resolves")


check("identity", "every cited governed identifier resolves against approved architecture",
      every_cited_identifier_resolves)


def the_identity_chain_is_stated_and_extended():
    chain = ("REQUEST", "INTENT", "WORK PLAN", "WORKFLOW", "WORKFLOW RUN", "TASK",
             "WORK ITEM", "ROLE", "MODEL", "ORCHESTRATOR", "HUMAN AUTHORITY")
    body = doc("intent-work-planning-architecture.md")
    problems = []
    # The chain is a blockquote and wraps; joining the quoted lines reads it as the one
    # statement it is. A line-at-a-time scan reported the tail of the chain as missing.
    quoted = [ln for ln in body.splitlines() if ln.lstrip().startswith(">") and "!=" in ln]
    line = [" ".join(quoted)] if quoted else []
    if not line:
        problems.append("the extended identity chain is not stated")
        return False, str(problems)
    stated = " ".join(line)
    position = -1
    for element in chain:
        found = stated.find(element, position + 1)
        if found < 0:
            problems.append("the chain omits %s, or states it out of order" % element)
        else:
            position = found
    return (not problems, str(problems)[:300] if problems
            else "the %d-element chain is stated in order" % len(chain))


check("identity", "the extended identity chain is stated in order",
      the_identity_chain_is_stated_and_extended)


def a_work_plan_never_becomes_a_workflow():
    """The single load-bearing separation of this phase.

    A Work Plan acquiring Workflow identity would let the system create its own governed
    reusable patterns. This checks the rule, its enforcement, and that no statement anywhere
    in the package contradicts it."""
    problems = []
    for phrase, name in (
            ("a work plan never acquires workflow identity",
             "intent-work-planning-architecture.md"),
            ("it is not a workflow, at any point, by any route",
             "workflow-matching-and-composition.md"),
            ("a work plan never becomes a workflow",
             "workflow-candidate-learning-boundary.md"),
            ("the system never writes to a governed registry",
             "workflow-candidate-learning-boundary.md")):
        if says(name, phrase):
            problems.append("%s: missing %r" % (name, phrase[:46]))
    # No statement may make a plan into a workflow, promote it, or register it.
    becomes = re.compile(
        r"(work.?plan|composed plan|plan)[^.]{0,60}?"
        r"(becomes? a workflow|is a workflow|promoted? to (?:a )?workflow|"
        r"registered as (?:a )?workflow|written (?:back )?(?:in)?to the workflow registry|"
        r"self-?registers?)", re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if not becomes.search(sentence):
                continue
            if CORRECTIVE.search(sentence):
                continue
            problems.append("%s:%d lets a Work Plan become a Workflow" % (name, i))
    # The identifier spaces must be declared distinct.
    if "work_plan.<id>" not in doc("work-plan-object-model.md"):
        problems.append("the Work Plan identifier space is not declared")
    return (not problems, str(problems)[:400] if problems
            else "a Work Plan is instance-level, in its own identifier space, by every route")


check("identity", "a Work Plan never acquires Workflow identity",
      a_work_plan_never_becomes_a_workflow)


def a_candidate_suggestion_stays_proposed():
    problems = []
    body = doc("workflow-candidate-learning-boundary.md")
    for token in ("workflow_candidate.<id>", "PROPOSED", "is_approved", "is_matchable"):
        if token not in body:
            problems.append("the suggestion record does not declare %s" % token)
    if "the only permitted value" not in flat(body):
        problems.append("PROPOSED is not declared the only permitted status")
    if says("workflow-candidate-learning-boundary.md",
            "self-approval is impossible by construction, not by policy"):
        problems.append("self-approval is forbidden only by policy, not by construction")
    approve = re.compile(r"(suggestion|candidate)[^.]{0,60}?"
                         r"(is approved|becomes approved|auto-?approv\w*|self-?approv\w*|"
                         r"is registered|becomes a workflow)", re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if approve.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d lets a candidate suggestion be approved" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "a candidate suggestion is PROPOSED, inert and unmatchable")


check("identity", "a repeated-pattern suggestion can never self-register",
      a_candidate_suggestion_stays_proposed)


# =========================================================== authority


def the_planner_never_grants_or_exercises_authority():
    problems = []
    for phrase, name in (
            ("the planner is not a second orchestrator",
             "intent-work-planning-architecture.md"),
            ("resolve first, then fail closed", "governance-preflight.md"),
            ("a missing right blocks. there is no alternative branch",
             "governance-preflight.md"),
            ("business necessity is not an authority", "governance-preflight.md"),
            ("it never exercises a right", "governance-preflight.md"),
            ("it never satisfies a review", "governance-preflight.md")):
        if says(name, phrase):
            problems.append("%s: missing %r" % (name, phrase[:46]))
    grants = re.compile(
        r"(planner|plan|planning|preflight|validation)[^.]{0,70}?"
        r"(grants? (?:a |the )?(?:right|authority)|exercis\w* (?:a |the )?right|"
        r"satisf\w* (?:a |the )?review|approves? the (?:act|work|plan)|"
        r"authoris\w* the (?:act|transmission|send)|creates? a decision record)",
        re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if grants.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d lets the planner grant or exercise authority"
                                % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "the planner resolves Rights, exercises none, and satisfies no review")


check("authority", "the planner never grants, exercises or substitutes for authority",
      the_planner_never_grants_or_exercises_authority)


def a_missing_decision_right_fails_closed():
    problems = []
    preflight = doc("governance-preflight.md")
    if "NO_APPLICABLE_DECISION_RIGHT" not in preflight:
        problems.append("preflight does not name the missing-Right failure")
    failures = doc("failure-and-escalation-model.md")
    row = [ln for ln in failures.splitlines()
           if "NO_APPLICABLE_DECISION_RIGHT" in ln and ln.startswith("|")]
    if not row:
        problems.append("the failure model has no NO_APPLICABLE_DECISION_RIGHT row")
    elif "block" not in flat(row[0]):
        problems.append("the missing-Right failure does not block")
    # The five act postures must exist and include a blocked one.
    for posture in ("PREPARING_ONLY", "REQUESTING_REVIEW", "REQUESTING_DECISION",
                    "EXECUTING_NON_AUTHORITY_ACT", "BLOCKED_FROM_TRANSMISSION"):
        if posture not in preflight:
            problems.append("act posture %s is not defined" % posture)
    if says("governance-preflight.md", "carries its justification"):
        problems.append("a non-authority act may be asserted without justification")
    return (not problems, str(problems)[:400] if problems
            else "a missing applicable Right blocks, with five declared act postures")


check("authority", "a missing applicable Decision Right fails closed",
      a_missing_decision_right_fails_closed)


def the_planner_never_selects_a_model():
    problems = []
    for phrase, name in (
            ("the envelope carries no model profile, provider or routing decision",
             "orchestrator-handoff-contract.md"),
            ("a work item names no model", "orchestrator-handoff-contract.md")):
        if says(name, phrase):
            problems.append("%s: missing %r" % (name, phrase[:46]))
    preflight = doc("governance-preflight.md")
    if "model selection is Phase 9" not in preflight and \
            "model profile" not in flat(preflight):
        problems.append("preflight does not check for model selection")
    selects = re.compile(
        r"(planner|plan|envelope|work item|planning)[^.]{0,70}?"
        r"(selects? (?:a |the )?model|chooses? (?:a |the )?model|"
        r"names? (?:a |the )?model profile|binds? (?:a |the )?provider)", re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if selects.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d lets the planner select a model" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "model selection stays with the Phase 9 Router")


check("authority", "the planner never selects a Model Profile",
      the_planner_never_selects_a_model)


def the_planner_invents_no_governed_primitive():
    problems = []
    for phrase, name in (
            ("the planner invents nothing", "role-skill-requirement-inference.md"),
            ("composition assembles approved primitives only",
             "workflow-matching-and-composition.md"),
            ("fail closed or constrain; never substitute",
             "role-skill-requirement-inference.md")):
        if says(name, phrase):
            problems.append("%s: missing %r" % (name, phrase[:46]))
    invents = re.compile(
        r"(planner|plan|composition|layer)[^.]{0,70}?"
        r"(invents?|creates?|defines?|synthesis\w*|widens?) "
        r"(a |an |the )?(new )?(role|skill|review profile|decision right|workflow)",
        re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if invents.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d lets the planner invent a governed primitive"
                                % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "no Role, Skill, Review Profile, Decision Right or Workflow is invented")


check("authority", "the planner invents no Role, Skill, Review Profile, Right or Workflow",
      the_planner_invents_no_governed_primitive)


# =========================================================== confidence


def confidence_is_never_authority():
    """The asymmetry: low confidence may trigger work; high confidence permits nothing."""
    model = doc("work-plan-object-model.md")
    problems = []
    for kind in ("semantic", "scope", "workflow_fit", "role_fit", "risk_detection",
                 "authority_resolution"):
        if kind not in model:
            problems.append("the confidence model omits %s" % kind)
    if says("work-plan-object-model.md", "there is no overall confidence"):
        problems.append("confidences may be aggregated into one number")
    if says("work-plan-object-model.md",
            "low confidence may trigger work; high confidence never grants permission"):
        problems.append("the confidence asymmetry is not stated")
    grants = re.compile(
        r"(confidence|score|certainty|threshold)[^.]{0,70}?"
        r"(grants?|waives?|satisfies|substitutes? for|permits?|allows?|overrides?|"
        r"approves?|authoris\w*)", re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if grants.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d lets confidence confer permission" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "six separate confidences, never aggregated, never permissive")


check("confidence", "confidence never grants authority, waives review or crosses scope",
      confidence_is_never_authority)


def high_confidence_cannot_waive_material_clarification():
    problems = []
    if says("clarification-policy.md",
            "the class is decided by consequence, not by confidence"):
        problems.append("the clarification class could be decided by confidence")
    if says("context-scope-resolution.md",
            "material scope ambiguity is always clarified, whatever the confidence"):
        problems.append("a confident scope resolution could skip clarification")
    policy = doc("clarification-policy.md")
    for cls in ("C1", "C2", "C3", "C4", "C5"):
        if cls not in policy:
            problems.append("ambiguity class %s is not defined" % cls)
    if "default_if_unanswered" not in policy:
        problems.append("the clarification record has no default field to constrain")
    if says("clarification-policy.md",
            "must be absent for c3, c4 and c5"):
        problems.append("a blocking clarification could carry a default")
    # The record table constraining the field is not the same as the rule forbidding a default
    # on a blocking class. A probe that rewrote the rule and left the table intact was not
    # caught by the table check alone, which is what this pair now closes.
    if says("clarification-policy.md",
            "on a blocking class is a validation failure"):
        problems.append("CL-15 no longer makes a default on a blocking class a failure")
    fallback = re.compile(
        r"(blocking|c4|c5)[^.]{0,70}?"
        r"(falls? back|default|proceeds? (?:on|with)|timeout|assumes?)", re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if not fallback.search(sentence):
                continue
            if CORRECTIVE.search(sentence):
                continue
            problems.append("%s:%d lets a blocking clarification fall back to a default"
                            % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "five classes; C4 and C5 block; no default is permitted on a blocking class")


check("confidence", "high confidence cannot waive clarification on scope or authority",
      high_confidence_cannot_waive_material_clarification)


def scope_is_never_crossed_on_inference():
    problems = []
    for phrase in ("never cross a boundary by guess",
                   "string proximity is not ancestry",
                   "one request, one scope",
                   "where clarification is unavailable, the planner blocks"):
        if says("context-scope-resolution.md", phrase):
            problems.append("missing %r" % phrase[:44])
    resolution = doc("context-scope-resolution.md")
    if "entitlement_status" not in resolution:
        problems.append("the scope record does not carry an entitlement status")
    if says("context-scope-resolution.md",
            "has one permitted value at planning time"):
        problems.append("the planner could record entitlement as granted")
    crosses = re.compile(
        r"(planner|plan|resolver|layer)[^.]{0,70}?"
        r"(crosses?|spans?|merges?|combines?) [^.]{0,30}?(scope|boundary|boundaries)",
        re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if crosses.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d lets the planner cross a scope boundary" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "one scope per request; no boundary crossed by inference or confidence")


check("confidence", "scope is never crossed by inference, similarity or confidence",
      scope_is_never_crossed_on_inference)


# =========================================================== governance consistency


def constraints_outrank_scores_everywhere():
    problems = []
    if says("workflow-matching-and-composition.md",
            "a score never overrides a constraint"):
        problems.append("MC-4 is missing")
    if says("workflow-matching-and-composition.md", "inadmissible is not low-scoring"):
        problems.append("an inadmissible candidate could be ranked rather than removed")
    matching = doc("workflow-matching-and-composition.md")
    for admissibility in ["A-%d" % n for n in range(1, 10)]:
        if admissibility not in matching:
            problems.append("admissibility check %s is not defined" % admissibility)
    if "constraint_overrides_attempted" not in matching:
        problems.append("there is no tripwire for an attempted constraint override")
    overrides = re.compile(
        r"(score|similarity|ranking|fit)[^.]{0,70}?"
        r"(overrides?|outranks?|supersedes?|beats?|takes precedence over)[^.]{0,40}?"
        r"(constraint|precondition|requirement|right|boundary|profile)", re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if overrides.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d lets a score override a constraint" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "nine admissibility checks gate; scores only rank")


check("governance", "a similarity score never overrides a governed constraint",
      constraints_outrank_scores_everywhere)


def a_review_requirement_is_never_satisfied_by_planning():
    problems = []
    if says("governance-preflight.md", "it never satisfies a review"):
        problems.append("preflight does not deny satisfying a review")
    if says("work-plan-object-model.md", "never satisfied here"):
        problems.append("the ReviewRequirement record does not deny satisfaction")
    satisfies = re.compile(
        r"(plan|planner|preflight|validation|requirement)[^.]{0,70}?"
        r"(review is satisfied|satisfies the review|marks? (?:the |a )?review satisfied|"
        r"review requirement is met by)", re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if satisfies.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d lets planning satisfy a review" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "a review requirement is recorded, never satisfied, by planning")


check("governance", "a review requirement is never satisfied by planning",
      a_review_requirement_is_never_satisfied_by_planning)


def inherited_floors_are_never_lowered():
    problems = []
    for phrase, name in (
            ("criticality raises and never lowers",
             "work-classification-and-criticality.md"),
            ("it never downgrades an inherited requirement",
             "work-classification-and-criticality.md"),
            ("composition never lowers a floor",
             "workflow-matching-and-composition.md")):
        if says(name, phrase):
            problems.append("%s: missing %r" % (name, phrase[:44]))
    classification = doc("work-classification-and-criticality.md")
    for trigger in ["T-%d" % n for n in range(1, 17)]:
        if trigger not in classification:
            problems.append("criticality trigger %s is not defined" % trigger)
    if says("work-classification-and-criticality.md",
            "detection failure is not absence"):
        problems.append("an undetected trigger could read as no trigger")
    lowers = re.compile(
        r"(planner|plan|classifier|composition)[^.]{0,70}?"
        r"(lowers?|downgrades?|relaxes?|reduces?|waives?)[^.]{0,40}?"
        r"(criticality|sensitivity|residency|review|requirement|band)", re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if lowers.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d lowers an inherited floor" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "sixteen triggers; criticality and every inherited floor only rise")


check("governance", "no inherited criticality, sensitivity or review floor is lowered",
      inherited_floors_are_never_lowered)


def unknown_routes_conservatively():
    problems = []
    if says("work-classification-and-criticality.md",
            "unknown on a safety field routes conservatively"):
        problems.append("WC-6 is missing")
    if says("work-classification-and-criticality.md",
            "planning conservatively is not asserting the conservative fact"):
        problems.append("the conservative branch could be recorded as an established fact")
    if says("request-intent-model.md",
            "the four safety fields are never inferred permissively"):
        problems.append("RI-4 is missing")
    classification = doc("work-classification-and-criticality.md")
    for field in ("act_direction", "reversibility", "commitment_possible",
                  "transmission_contemplated"):
        if field not in classification:
            problems.append("the conservative branch omits %s" % field)
    return (not problems, str(problems)[:400] if problems
            else "four safety fields; UNKNOWN plans as the consequential value, recorded as UNKNOWN")


check("governance", "an UNKNOWN safety field routes to the conservative branch",
      unknown_routes_conservatively)


# =========================================================== knowledge


def planning_output_stays_correctly_typed():
    problems = []
    model = doc("work-plan-object-model.md")
    for epistemic in ("SOURCE", "EVIDENCE", "FACT_CLAIM", "ASSUMPTION", "CALCULATION",
                      "INFERENCE", "AI_SUGGESTION", "UNKNOWN"):
        if epistemic not in model:
            problems.append("the object model omits the epistemic type %s" % epistemic)
    if says("work-plan-object-model.md", "planner output is ai_suggestion and stays there"):
        problems.append("planner output could be promoted")
    if says("work-plan-object-model.md", "a plan may not resolve its own unknowns"):
        problems.append("the planner could close an UNKNOWN by deciding it")
    if says("request-intent-model.md", "nothing is converted"):
        problems.append("the intent model does not deny epistemic conversion")
    # No active use of the deprecated label, and no conversion.
    mutation = re.compile(
        r"(`?SOURCE`?\s*(?:→|->|to)\s*`?(?:FACT|FACT_CLAIM)|"
        r"(?:AI_SUGGESTION)\s*(?:→|->|to)\s*`?FACT_CLAIM|"
        r"promot\w* (?:the |an )?(?:source|assumption|suggestion)|"
        r"converts? (?:an? )?(?:assumption|suggestion|inference) (?:in)?to (?:a )?fact)",
        re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if mutation.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d describes an epistemic conversion" % (name, i))
    for name in all_docs():
        for i, sentence in statements(name):
            if re.search(r"`FACT`", sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d uses the deprecated `FACT` label actively" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "eight epistemic types; planner output is AI_SUGGESTION and converts to nothing")


check("knowledge", "generated planning knowledge stays correctly typed",
      planning_output_stays_correctly_typed)


# =========================================================== handoff


def the_handoff_requires_a_validated_path():
    problems = []
    handoff = doc("orchestrator-handoff-contract.md")
    if says("orchestrator-handoff-contract.md",
            "the handoff happens only on a passing preflight"):
        problems.append("HO-2 is missing: a plan could hand off unvalidated")
    if says("orchestrator-handoff-contract.md", "the planner hands over a trigger, not a run"):
        problems.append("HO-1 is missing")
    for field in ("execution_basis", "workflow_ref", "work_plan_ref", "scope_ref",
                  "idempotency_key", "criticality_band", "act_posture"):
        if field not in handoff:
            problems.append("the trigger envelope omits %s" % field)
    if says("orchestrator-handoff-contract.md", "fields 2 and 3 are mutually exclusive"):
        problems.append("an envelope could carry both a workflow and a work-plan reference")
    if says("orchestrator-handoff-contract.md", "there is no return path"):
        problems.append("the planner could be re-entered by the run")
    if says("intent-work-planning-architecture.md", "the orchestrator re-checks everything"):
        problems.append("PL-7 is missing: the planner could satisfy an intake check by assertion")
    # The seven approved intake checks must each be served.
    architecture = doc("intent-work-planning-architecture.md")
    intake = architecture.split("## 7.")[1].split("## 8.")[0] if "## 7." in architecture else ""
    served = len([ln for ln in intake.splitlines() if ln.startswith("| ")])
    if served < 8:
        problems.append("the handoff does not map all seven orchestrator intake checks")
    acts = re.compile(
        r"(planner|planning layer)[^.]{0,70}?"
        r"(creates? (?:a |the )?run|activates? (?:a |the )?stage|makes? (?:an |the )?assignment|"
        r"issues? (?:a |the )?routing request|completes? (?:a |the )?run|"
        r"performs? (?:a |the )?retry)", re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if acts.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d lets the planner act as the Orchestrator" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "one envelope, on a passing preflight, with no return path")


check("handoff", "the Orchestrator handoff requires a validated path and no second orchestrator",
      the_handoff_requires_a_validated_path)


def work_items_carry_what_orchestration_needs():
    handoff = doc("orchestrator-handoff-contract.md")
    problems = []
    if says("orchestrator-handoff-contract.md",
            "only from validated plan stages bound to approved definitions"):
        problems.append("HO-6 is missing: work items could be made from an unvalidated plan")
    required = ("work intent reference", "scope reference", "stage and dependency references",
                "role / skill envelope", "expected artifact", "knowledge states",
                "review and gate requirements", "sensitivity", "criticality",
                "completion criteria", "failure and escalation")
    low = flat(handoff)
    for element in required:
        if flat(element) not in low:
            problems.append("a work item does not carry %r" % element)
    if says("orchestrator-handoff-contract.md",
            "a work item is a specification of work, not an assignment"):
        problems.append("HO-7 is missing: the planner could assign")
    return (not problems, str(problems)[:400] if problems
            else "eleven work-item elements; specification, never assignment")


check("handoff", "work items carry deterministic orchestration content and no assignment",
      work_items_carry_what_orchestration_needs)


# =========================================================== user experience


def the_user_is_never_required_to_supply_internal_ids():
    problems = []
    if says("user-experience-contract.md", "none of these is ever required input"):
        problems.append("UX-3 is missing")
    if says("clarification-policy.md", "never ask the user to choose an internal object"):
        problems.append("CL-4 is missing")
    ux = doc("user-experience-contract.md")
    for hidden in ("Workflow ID", "Role ID", "Skill ID", "Review Profile ID",
                   "Decision Right ID", "Model Profile"):
        if hidden not in ux:
            problems.append("the UX contract does not hide %s" % hidden)
    if says("user-experience-contract.md", "a removed or blocked act is stated"):
        problems.append("UX-5 is missing: an act could be dropped silently")
    if says("user-experience-contract.md", "confidence is never displayed as safety"):
        problems.append("UX-7 is missing")
    asks = re.compile(
        r"(user|product)[^.]{0,70}?"
        r"(must (?:choose|select|supply|provide|name)|is asked to (?:choose|select|pick))"
        r"[^.]{0,40}?(workflow|role|skill|review profile|decision right|model)",
        re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            if asks.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d requires the user to supply an internal id" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "internal identifiers are hidden by default and never required")


check("ux", "the user is never required to supply an internal identifier",
      the_user_is_never_required_to_supply_internal_ids)


# =========================================================== failure model


def the_failure_taxonomy_is_complete_and_dispositioned():
    failures = doc("failure-and-escalation-model.md")
    required = ("NO_VALID_SCOPE", "AMBIGUOUS_SCOPE", "NO_MATCHING_WORKFLOW",
                "PLAN_COMPOSITION_REQUIRED", "REQUIRED_ROLE_UNAVAILABLE",
                "REQUIRED_SKILL_UNAVAILABLE", "REVIEW_PROFILE_UNAVAILABLE",
                "NO_APPLICABLE_DECISION_RIGHT", "EVIDENCE_REQUIREMENT_UNSATISFIED",
                "CRITICALITY_UNRESOLVED", "CONFLICTING_REQUIREMENTS", "UNSAFE_INFERENCE",
                "PLAN_VALIDATION_FAILED")
    problems = []
    rows = {}
    for line in failures.splitlines():
        m = re.match(r"^\|\s*F-\d+\s*\|\s*`([A-Z_]+)`\s*\|(.+?)\|", line)
        if m:
            rows[m.group(1)] = flat(m.group(2))
    for mode in required:
        if mode not in rows:
            problems.append("failure mode %s has no row" % mode)
            continue
        if not rows[mode].strip():
            problems.append("failure mode %s has no disposition" % mode)
    if says("failure-and-escalation-model.md", "the strictest disposition wins"):
        problems.append("FE-5 is missing: combined failures could take the weakest disposition")
    if says("failure-and-escalation-model.md", "no disposition is reachable by confidence"):
        problems.append("FE-4 is missing")
    if says("failure-and-escalation-model.md", "a blocked plan is a result, delivered"):
        problems.append("FE-2 is missing: a block could be a silent dead end")
    return (not problems, str(problems)[:400] if problems
            else "%d failure modes, each with exactly one disposition" % len(rows))


check("failure", "the planning failure taxonomy is complete and each mode has a disposition",
      the_failure_taxonomy_is_complete_and_dispositioned)


# =========================================================== self-discipline


def the_preflight_checks_are_complete():
    preflight = doc("governance-preflight.md")
    problems = []
    declared = set(re.findall(r"\*\*(G-\d+)\*\*", preflight))
    for n in range(1, 19):
        if "G-%d" % n not in declared:
            problems.append("preflight check G-%d is not declared" % n)
    if says("governance-preflight.md", "passing preflight is not approval"):
        problems.append("GP-1 is missing: a pass could read as approval")
    if "is_approval" not in preflight:
        problems.append("the validation result does not declare is_approval")
    return (not problems, str(problems)[:400] if problems
            else "%d preflight checks; passing is explicitly not approval" % len(declared))


check("preflight", "every governance preflight check is declared",
      the_preflight_checks_are_complete)


def the_object_model_covers_every_record():
    model = doc("work-plan-object-model.md")
    required = ("Request", "WorkIntent", "ScopeResolution", "WorkRequirementSet",
                "WorkflowMatchAssessment", "WorkPlan", "PlanStage", "RoleRequirement",
                "SkillRequirement", "ReviewRequirement", "DecisionRequirement",
                "EvidenceRequirement", "ClarificationRequirement", "PlanningFinding",
                "PlanValidationResult", "WorkflowCandidateSuggestion")
    problems = []
    rows = {}
    for line in model.splitlines():
        m = re.match(r"^\|\s*\d+\s*\|\s*`(\w+)`\s*\|(.+)\|\s*$", line)
        if m:
            rows[m.group(1)] = [c.strip() for c in m.group(2).split("|")]
    for record in required:
        if record not in rows:
            problems.append("the object model omits %s" % record)
            continue
        if len(rows[record]) < 7:
            problems.append("%s does not answer every column" % record)
    if says("work-plan-object-model.md", "every planning record is non-authoritative"):
        problems.append("OM-1 is missing")
    # Exactly one record may affect execution, and only by withholding.
    # The column answers "affects execution directly". Anything other than a plain "no" is an
    # effect, however it is worded - PlanValidationResult says "Gates the handoff", and a check
    # looking only for "yes" read that as no effect at all.
    # A qualified "No - intake re-checks" is still No; the qualifier explains why. Only a cell
    # that does not open with "no" claims an effect, and exactly one record may.
    affecting = [r for r, cells in rows.items()
                 if cells and not flat(cells[-1]).startswith("no")]
    if affecting != ["PlanValidationResult"]:
        problems.append("records affecting execution directly: %s" % affecting)
    return (not problems, str(problems)[:400] if problems
            else "%d records, all non-authoritative; one gates the handoff" % len(rows))


check("preflight", "the planning object model covers every record and none carries authority",
      the_object_model_covers_every_record)


def the_harness_contains_no_vacuous_check():
    source = read(os.path.join("validation", "phase_15_validation.py"))
    bodies = re.findall(r"\ndef ([a-z0-9_]+)\(\):\n(.*?)(?=\ndef |\ncheck\()", source, re.S)
    vacuous = [n for n, b in bodies
               if "return True" in b and "problems" not in b and "missing" not in b]
    return (not vacuous, str(vacuous) if vacuous
            else "%d checks, none unconditionally passing" % len(RESULTS))


check("preflight", "the harness contains no vacuous or unconditional-pass check",
      the_harness_contains_no_vacuous_check)


def the_validator_disclaims_governance_authority():
    source = read(os.path.join("validation", "phase_15_validation.py"))
    missing = [p for p in ("NEVER GOVERNANCE AUTHORITY", "approves nothing",
                           "does not make the Phase 15 architecture correct")
               if p not in source]
    return (not missing, str(missing) if missing
            else "the harness disclaims authority in its own docstring")


check("preflight", "the validator disclaims governance authority",
      the_validator_disclaims_governance_authority)


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
