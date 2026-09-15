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


#: CORRECTIVE asks only whether a denial appears ANYWHERE in the statement, which a long
#: sentence satisfies by accident - and a mutation planted in a second location inherits that
#: accidental cover. DENIAL/denied_near ask the narrower question the second-location checks
#: need: is the prohibited verb ITSELF negated, within the words immediately before it?
DENIAL = re.compile(
    r"\b(never|not|no|none|nothing|cannot|must not|may not|nor|without|neither|"
    r"forbid\w*|prohibit\w*|refus\w*|excluded|rather than|instead of)\b", re.IGNORECASE)


def row_answer(sentence, match, span=56):
    """The beginning of the NEXT cell after a match, and nothing beyond it.

    A table row answers itself in the following column, so a forward look is right for a row -
    but only as far as that answer. Reading an arbitrary window forwards let a later cell's
    denial of something else ("...no longer needs the conclusion") excuse the claim."""
    rest = sentence[match.end():]
    boundary = rest.find("|")
    if boundary < 0:
        return ""
    return rest[boundary:boundary + span]


def denied_near(sentence, match, window=64, after=0):
    """Is the matched verb negated by something close enough to govern it?

    Backwards only, by default. Looking forwards as well seemed reasonable - a table row answers
    itself in the next column - but it let a following clause that denies something ELSE excuse
    the claim: "Phase 15 creates the runtime Work Item ... and cannot hold one in a pre-runtime
    state" read as denied. So the forward window is enabled only for a table row, where the
    answer genuinely follows the claim, and prose is judged on what precedes the verb."""
    start = max(0, match.start() - window)
    return bool(DENIAL.search(sentence[start:match.end() + after]))


def scan(pattern, message, problems, docs=None, strict=True):
    """Every statement in the package, against one prohibited pattern.

    strict=True uses denied_near: a denial has to govern the matched verb. That is what makes a
    weakening planted in a second active statement visible, where a whole-sentence CORRECTIVE
    test would let the neighbouring qualifiers excuse it."""
    for name in (docs or all_docs()):
        for i, sentence in statements(name):
            m = pattern.search(sentence)
            if not m:
                continue
            row = sentence.lstrip().startswith("|")
            if strict:
                before = sentence[max(0, m.start() - 64):m.end()]
                if DENIAL.search(before):
                    continue
                if row and DENIAL.search(row_answer(sentence, m)):
                    continue
            elif CORRECTIVE.search(sentence):
                continue
            problems.append("%s:%d %s" % (name, i, message))


def statements(name):
    """(line, statement): a table ROW is one statement, a bullet is one, prose splits by sentence.

    A row's columns answer each other - an exemplar row's scenario cell is answered by its
    outcome cell - so splitting a row reads the scenario as a claim. A bullet merged into the
    paragraph around it would acquire every qualifier its neighbours carry."""
    fenced = False
    buffer, bullet, start = [], [], None
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
        if line.lstrip().startswith("|") or re.match(r"\s*([-*+]|\d+\.)\s+\S", line):
            if buffer:
                units.append((start, " ".join(buffer)))
                buffer, start = [], None
            if line.lstrip().startswith("|"):
                units.append((i, line))
            else:
                # A wrapped bullet or numbered item continues on indented lines. Orphaning them made the tail of
                # a bullet a statement of its own, stripped of the denial that governs it - the
                # defect that let "...may be read as saying COMPOSE is runnable today" read as a
                # claim that it is. Joining a bullet to ITS OWN continuation is not the same as
                # merging it into the neighbouring paragraph, which stays forbidden.
                bullet, start = [line], i
                continue
            continue
        if not line.strip():
            if bullet:
                units.append((start, " ".join(bullet)))
                bullet, start = [], None
            if buffer:
                units.append((start, " ".join(buffer)))
                buffer, start = [], None
            continue
        if bullet is not None and bullet and line.startswith((" ", "\t")):
            bullet.append(line.strip())
            continue
        if bullet:
            units.append((start, " ".join(bullet)))
            bullet, start = [], None
        if start is None:
            start = i
        buffer.append(line)
    if bullet:
        units.append((start, " ".join(bullet)))
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
             "PLANNED WORK ITEM SPEC", "WORK ITEM", "ROLE", "MODEL", "ORCHESTRATOR",
             "HUMAN AUTHORITY")
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
            ("a spec names no model", "orchestrator-handoff-contract.md"),
            ("the envelope carries no model profile", "orchestrator-handoff-contract.md")):
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


def planned_work_item_specs_are_never_runtime_work_items():
    """The Phase 11 ownership boundary, checked in both halves.

    `work_item.<id>` is runtime state owned by a run. Phase 15 writes before any run exists, so
    a Phase 15 rule that instantiates one has taken a Phase 11 identity - which is what the
    independent review found in the first version of this package."""
    handoff = doc("orchestrator-handoff-contract.md")
    problems = []
    for phrase, name in (
            ("the planner produces `PlannedWorkItemSpec` records and never instantiates a "
             "runtime work item", "orchestrator-handoff-contract.md"),
            ("a spec carries no runtime anything", "orchestrator-handoff-contract.md"),
            ("no approved contract consumes a `PlannedWorkItemSpec`, and Phase 15 may not claim",
             "orchestrator-handoff-contract.md"),
            ("a spec is not a bridge over PO-4", "orchestrator-handoff-contract.md"),
            ("a spec is a specification of work, not an assignment",
             "orchestrator-handoff-contract.md"),
            ("a spec names no model", "orchestrator-handoff-contract.md"),
            ("`PlannedWorkItemSpec` is a planning record, and `work_item.<id>` is a runtime one",
             "work-plan-object-model.md")):
        if says(name, phrase):
            problems.append("%s: missing %r" % (name, phrase[:52]))
    # The separation must be asserted as an identity, in both owning documents.
    for name in ("orchestrator-handoff-contract.md", "work-plan-object-model.md"):
        if says(name, "PLANNED WORK ITEM SPEC != WORK ITEM"):
            problems.append("%s does not state the spec/Work Item identity separation" % name)
    if says("intent-work-planning-architecture.md",
            "instantiate a phase 11 runtime `work item`"):
        problems.append("N-11 is missing from the prohibitions")
    if "planned_work_item_spec.<id>" not in handoff:
        problems.append("the spec has no identifier space of its own")
    required = ("work intent reference", "scope reference", "stage and dependency references",
                "role / skill envelope", "expected artifact", "knowledge states",
                "review and gate requirements", "sensitivity", "criticality",
                "completion criteria", "failure and escalation")
    low = flat(handoff)
    for element in required:
        if flat(element) not in low:
            problems.append("a planned work item spec does not carry %r" % element)
    # Nothing anywhere may create, own or hold a runtime Work Item, or a run.
    scan(re.compile(
        r"(planner|planning|plan|phase 15|spec|specification|layer)[^.|]{0,80}?"
        r"(instantiat\w*|creates?|mints?|owns?|holds?|opens?|allocates?|pre-?creates?)"
        r"[^.|]{0,30}?(runtime identity|`?work_item\.<id>`?|(?<!planned )work item)",
        re.IGNORECASE),
        "lets Phase 15 instantiate a runtime Work Item", problems)
    scan(re.compile(
        r"(spec|specification|planning record|work plan)[^.|]{0,60}?"
        r"(carries|has|holds|records?)[^.|]{0,30}?"
        r"(runtime state|run ownership|`?run\.<id>`?|assignment status|execution status)",
        re.IGNORECASE),
        "gives a planning record runtime state", problems)
    scan(re.compile(
        r"(spec|specification)[^.|]{0,60}?(becomes?|is promoted to|turns into|"
        r"transitions? (?:in)?to)[^.|]{0,20}?work item", re.IGNORECASE),
        "transitions a spec into a Work Item", problems)
    return (not problems, str(problems)[:400] if problems
            else "eleven spec elements; no runtime Work Item, state, run or assignment")


check("handoff", "planned work item specs are never runtime Work Items",
      planned_work_item_specs_are_never_runtime_work_items)


def the_work_mode_model_is_singular_and_deterministic():
    """One primary mode, a set of secondaries, and no document contradicting the cardinality."""
    intent = doc("request-intent-model.md")
    problems = []
    if "`primary_work_mode`" not in intent:
        problems.append("the intent model has no primary_work_mode field")
    if "`secondary_work_modes`" not in intent:
        problems.append("the intent model has no secondary_work_modes field")
    if says("request-intent-model.md",
            "one primary mode, a set of secondary modes, and no free-form third form"):
        problems.append("RI-12 is missing: the cardinality is not stated deterministically")
    if says("request-intent-model.md", "never contains the primary"):
        problems.append("a mode could appear as both primary and secondary")
    if says("request-intent-model.md",
            "downstream logic that needs a single leading mode reads `primary_work_mode`"):
        problems.append("no rule says how a leading mode is derived downstream")
    # The retired singular field may not survive anywhere, and no document may assign two modes.
    for name in all_docs():
        for i, sentence in statements(name):
            if not re.search(r"`work_mode`", sentence):
                continue
            # A statement that names the field in order to record its retirement is not a use
            # of it. Everything else is.
            if re.search(r"\b(retired|retirement|replaced by|no longer)\b", sentence, re.I):
                continue
            problems.append("%s:%d still uses the retired `work_mode` field" % (name, i))
    scan(re.compile(
        r"`?primary_work_mode`?[^.|]{0,40}?(and|,)[^.|]{0,20}?`?(ACTION|ANALYSIS|ADVICE|"
        r"DRAFTING|MONITORING|DECISION_SUPPORT)`?[^.|]{0,10}?(and|\+)", re.IGNORECASE),
        "gives a Work Intent more than one primary mode", problems)
    return (not problems, str(problems)[:400] if problems
            else "one primary mode, a unique secondary set, stated once and used everywhere")


check("handoff", "the work mode model is singular, deterministic and used consistently",
      the_work_mode_model_is_singular_and_deterministic)


def the_missing_capability_disposition_is_deterministic():
    """F-5 and F-6 must each resolve from a recorded predicate, not from a judgement call."""
    roles = doc("role-skill-requirement-inference.md")
    failures = doc("failure-and-escalation-model.md")
    problems = []
    for token in ("LB-1", "LB-2", "LB-3", "LB-4", "LB-5",
                  "`load_bearing`", "`load_bearing_basis`",
                  "LOAD_BEARING", "NOT_LOAD_BEARING"):
        if token not in roles:
            problems.append("the load-bearing predicate omits %s" % token)
    for letter in ("LB-a", "LB-b", "LB-c", "LB-d", "LB-e"):
        if letter not in roles:
            problems.append("the predicate has no condition %s" % letter)
    if says("role-skill-requirement-inference.md",
            "it never reads a confidence value, an urgency, a deadline or a convenience"):
        problems.append("the predicate could be decided by confidence or convenience")
    if says("role-skill-requirement-inference.md",
            "a reduced deliverable is validated only after `NOT_LOAD_BEARING` is independently"):
        problems.append("LB-2 is missing: a reduction could decide the determination")
    if says("role-skill-requirement-inference.md",
            "the determination is recorded as a first-class field"):
        problems.append("LB-3 is missing: the determination need not be recorded")
    if says("role-skill-requirement-inference.md",
            "the predicate never reaches for a substitute"):
        problems.append("LB-4 is missing: the predicate could substitute a Role")
    # Both failure rows must name the predicate rather than leaving the choice open.
    for mode in ("REQUIRED_ROLE_UNAVAILABLE", "REQUIRED_SKILL_UNAVAILABLE"):
        row = [ln for ln in failures.splitlines() if mode in ln and ln.startswith("|")]
        if not row:
            problems.append("%s has no row" % mode)
            continue
        low = flat(row[0])
        if "load_bearing" not in low:
            problems.append("%s does not resolve from the recorded determination" % mode)
        if "block" not in low or "constrain" not in low:
            problems.append("%s does not name both branches" % mode)
    # And preflight must fail a plan that records the gap without the determination.
    preflight = doc("governance-preflight.md")
    for g in ("**G-5**", "**G-6**"):
        row = [ln for ln in preflight.splitlines() if ln.startswith("| " + g)]
        # The failure column names LOAD_BEARING too, so a bare "load_bearing" test passed even
        # after the *requirement* had been deleted from the check column. The basis field is
        # named only by the requirement, which is what has to survive.
        if not row or "load_bearing_basis" not in flat(row[0]):
            problems.append("%s does not require the load-bearing determination to be recorded"
                            % g)
    scan(re.compile(
        r"(load.?bearing|unavailable (?:role|skill|capability))[^.|]{0,70}?"
        r"(is a judgement|depends on (?:the )?(?:planner|confidence|urgency)|"
        r"at the planner's discretion|decided case by case)", re.IGNORECASE),
        "makes the load-bearing determination discretionary", problems)
    return (not problems, str(problems)[:400] if problems
            else "five conditions, two recorded fields, one disposition per failure mode")


check("failure", "a missing capability resolves to one deterministic disposition",
      the_missing_capability_disposition_is_deterministic)


def evidence_failure_is_plan_level_and_never_partial():
    """F-9, G-11 and HO-2 must say the same thing, and none may run or hold a stage."""
    failures = doc("failure-and-escalation-model.md")
    problems = []
    row = [ln for ln in failures.splitlines()
           if "EVIDENCE_REQUIREMENT_UNSATISFIED" in ln and ln.startswith("|")]
    if not row:
        problems.append("F-9 has no row")
    else:
        low = flat(row[0])
        if "block the plan" not in low:
            problems.append("F-9 does not block the plan")
        if "stage" in low and "no stages to block" not in low:
            problems.append("F-9 still disposes of a stage")
    if says("failure-and-escalation-model.md",
            "phase 15 neither continues nor halts a stage, in any failure mode"):
        problems.append("FE-11 is missing: a failure mode could continue some stages")
    if says("failure-and-escalation-model.md",
            "a `FUTURE_GOVERNANCE_REFERENCE` is not a satisfied requirement"):
        problems.append("FE-12 is missing: a deferred reference could pass as satisfied")
    if "FUTURE_GOVERNANCE_REFERENCE" not in failures:
        problems.append("the deferral branch does not use the approved Phase 11 mechanism")
    if says("governance-preflight.md", "every preflight outcome is plan-level"):
        problems.append("GP-14 is missing: a check could produce a per-stage verdict")
    g11 = [ln for ln in doc("governance-preflight.md").splitlines()
           if ln.startswith("| **G-11**")]
    if not g11 or "block the plan" not in flat(g11[0]):
        problems.append("G-11 does not block at plan level")
    if says("orchestrator-handoff-contract.md",
            "no envelope carrying some stages while others are still unsatisfied"):
        problems.append("HO-2 does not exclude a stage-wise partial handoff")
    scan(re.compile(
        r"(plan|planner|preflight|phase 15)[^.|]{0,80}?"
        r"(may proceed|proceeds?|continues?|may continue|releases?)[^.|]{0,40}?"
        r"(later stages?|other stages?|remaining stages?|unaffected stages?)",
        re.IGNORECASE),
        "lets Phase 15 continue some stages while another is blocked", problems)
    scan(re.compile(
        r"(partial|provisional|reduced|stage-wise|piecemeal)[^.|]{0,30}?"
        r"(handoff|hand-?over|envelope)", re.IGNORECASE),
        "permits a partial handoff", problems)
    scan(re.compile(
        r"(block|blocks|blocking|halts?|holds?)[^.|]{0,20}?"
        r"(the affected stage|that stage|the stage)", re.IGNORECASE),
        "has Phase 15 blocking an individual stage", problems)
    return (not problems, str(problems)[:400] if problems
            else "F-9, G-11 and HO-2 agree: plan-level, whole, with no stage progression")


check("failure", "an unsatisfied evidence requirement is plan-level, never partial",
      evidence_failure_is_plan_level_and_never_partial)


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
                "PLAN_VALIDATION_FAILED", "NO_APPROVED_ROLE_OWNS_CONCLUSION")
    problems = []
    rows = {}
    for line in failures.splitlines():
        m = re.match(r"^\|\s*F-\d+\s*\|\s*`([A-Z_]+)`[^|]*\|(.+?)\|", line)
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
    for n in range(1, 21):
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
                "PlanValidationResult", "PlannedWorkItemSpec",
                "WorkflowCandidateSuggestion")
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
    # The spec's row is the one place a reader meets it in the record inventory. A weakening
    # there ("the runtime Work Item the planner creates") puts the object before the verb, which
    # the prohibited-verb scans cannot match, so the row's own content is checked.
    spec_row = [ln for ln in model.splitlines()
                if ln.startswith("|") and "`PlannedWorkItemSpec`" in ln]
    if not spec_row:
        problems.append("the object model has no PlannedWorkItemSpec row")
    else:
        low = flat(spec_row[0])
        if "never a work_item.<id>" not in low:
            problems.append("the spec's row does not deny runtime Work Item identity")
        if "runtime work item the planner" in low or "the runtime work item" in low.replace(
                "instantiate a runtime work item", ""):
            problems.append("the spec's row describes it AS a runtime Work Item")
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


def task_spec_and_work_item_stay_three_things():
    """Blocker 1. The approved Phase 11 model distinguishes a Task from a Work Item; Phase 15
    adds a third object and may not collapse any pair of the three."""
    problems = []
    for name in ("intent-work-planning-architecture.md", "orchestrator-handoff-contract.md"):
        if says(name, "TASK != PLANNED WORK ITEM SPEC != WORK ITEM"):
            problems.append("%s does not state the three-way separation" % name)
    architecture = doc("intent-work-planning-architecture.md")
    for role, phrase in (("Task", "defined once and unchanged by any run"),
                         ("Work Item", "the run's instance of a task")):
        if flat(phrase) not in flat(architecture):
            problems.append("the identity table does not say what a %s is" % role)
    # No document may pair them as one object, and none may say a Task is made in a run.
    scan(re.compile(r"task\s*/\s*work item|work item\s*/\s*task", re.IGNORECASE),
         "groups Task and Work Item as one object", problems)
    made_in_a_run = re.compile(
        r"(task|activity)[^.|]{0,50}?(is |are )?(created|instantiated|defined|made)"
        r"[^.|]{0,30}?(inside|within|by|during)[^.|]{0,20}?(a |the )?(run|phase 11|orchestrator)",
        re.IGNORECASE)
    for name in all_docs():
        for i, sentence in statements(name):
            m = made_in_a_run.search(sentence)
            if not m or denied_near(sentence, m):
                continue
            # "the run's instance of a Task, created inside a run" is a statement about the Work
            # Item, not about the Task. The Task there is the thing being instanced, not made.
            if re.search(r"instance of (a|that|the)\s*$", sentence[:m.start()],
                         re.IGNORECASE):
                continue
            problems.append("%s:%d has a Task created inside a run" % (name, i))
    scan(re.compile(
        r"(spec|specification)[^.|]{0,40}?(is |are )?(a |an |the )?(task|activity)\b",
        re.IGNORECASE),
        "collapses a spec into a Task", problems)
    return (not problems, str(problems)[:400] if problems
            else "Task, PlannedWorkItemSpec and Work Item are three objects, stated as three")


check("handoff", "Task, planned spec and Work Item stay three separate things",
      task_spec_and_work_item_stay_three_things)


def no_approved_contract_is_claimed_to_consume_a_spec():
    """Blocker 2. `PlannedWorkItemSpec` is a proposed Phase 15 object. No approved Phase 11
    contract names it, so no Phase 15 statement may describe Phase 11 consuming one today."""
    problems = []
    handoff = doc("orchestrator-handoff-contract.md")
    for phrase in ("no approved Phase 11 artifact defines it as an intake object",
                   "may be carried in a **proposed** handoff envelope only where an approved "
                   "execution-basis contract permits it",
                   "require **explicit Phase 11 change control**",
                   "COMPOSE remains non-executable under PO-4",
                   "MATCH** continues to hand off through the approved Workflow-based intake path"):
        if says("orchestrator-handoff-contract.md", phrase):
            problems.append("§3a does not state %r" % phrase[:50])
    if "and none currently does" not in handoff:
        problems.append("§3a does not say that no approved contract currently permits a spec")
    # The crossing table is where a reader learns what actually leaves Phase 15, and a weakening
    # there reads "spec ... which Phase 11 accepts" - subject before verb, which the scans below
    # cannot see. So the row carries its condition, and the condition is checked directly.
    crossing = [ln for ln in handoff.splitlines()
                if ln.startswith("| `PlannedWorkItemSpec` records")]
    if not crossing:
        problems.append("the crossing table does not list the spec")
    elif "only where an approved execution-basis contract permits" not in crossing[0]:
        problems.append("the crossing table lets a spec cross unconditionally")
    consumes = re.compile(
        r"(phase 11|orchestrator|intake|run)[^.|]{0,70}?"
        r"(reads?|consumes?|accepts?|ingests?|re-?validates?|instantiates? .{0,20}from|"
        r"derives? .{0,30}from|translates?)[^.|]{0,40}?"
        r"(`?planned_?work_?item_?spec`?|planned work item spec|planned spec)",
        re.IGNORECASE)
    scan(consumes, "claims an approved contract consumes a PlannedWorkItemSpec", problems)
    scan(re.compile(
        r"(spec|specification)[^.|]{0,60}?"
        r"(lets?|allows?|enables?|bridges?|makes?)[^.|]{0,40}?"
        r"(a |the )?(work.?plan|compose)[^.|]{0,30}?(run|executable|start)", re.IGNORECASE),
        "claims a spec bridges the COMPOSE execution gap", problems)
    return (not problems, str(problems)[:400] if problems
            else "a spec is produced, consumed by nothing approved, and bridges nothing")


check("handoff", "no approved contract is claimed to consume a planned spec",
      no_approved_contract_is_claimed_to_consume_a_spec)


def the_generation_order_is_acyclic():
    """Blocker 3. A spec derives from a VALIDATED stage, so it cannot precede validation."""
    architecture = doc("intent-work-planning-architecture.md")
    problems = []
    if says("intent-work-planning-architecture.md",
            "the sequence is acyclic, and step 12 is downstream of step 11"):
        problems.append("PL-8 is missing: the sequence does not declare its own order")
    if says("intent-work-planning-architecture.md",
            "it cannot exist before validation and it is never an input to the validation"):
        problems.append("a spec could be an input to the validation that must precede it")
    steps = {}
    for line in architecture.splitlines():
        m = re.match(r"^\|\s*(\d+[a-z]?)\s*\|(.+?)\|(.+?)\|(.+?)\|\s*$", line)
        if m:
            steps[m.group(1)] = flat(m.group(2) + " " + m.group(4))
    def step_of(token):
        found = [k for k, v in steps.items() if token in v]
        return found[0] if found else None
    validate, spec = step_of("planvalidationresult"), step_of("plannedworkitemspec")
    envelope = step_of("trigger envelope")
    order = []
    for label, key in (("validation", validate), ("spec", spec), ("handoff", envelope)):
        if key is None:
            problems.append("the planning sequence has no %s step" % label)
        else:
            order.append((label, int(re.match(r"\d+", key).group())))
    if len(order) == 3:
        nums = [n for _, n in order]
        if not nums[0] < nums[1] <= nums[2]:
            problems.append("the sequence runs %s, which is not validate -> spec -> handoff"
                            % order)
    # Nor may any preflight check read a spec: that would close the loop from the other side.
    scan(re.compile(
        r"(preflight|validation|`?G-\d+`?|check)[^.|]{0,60}?"
        r"(reads?|takes?|uses?|requires?|inspects?)[^.|]{0,30}?"
        r"(`?planned_?work_?item_?spec`?|planned work item spec)", re.IGNORECASE),
        "makes a spec an input to the validation that must precede it", problems)
    return (not problems, str(problems)[:400] if problems
            else "validate at step %s, spec at step %s, handoff at step %s"
                 % (validate, spec, envelope))


check("handoff", "a planned spec is generated after validation, never before",
      the_generation_order_is_acyclic)


def the_primary_mode_is_derived_upstream_only():
    """Blocker 4 and escaped class 4. WorkIntent precedes PlanStage, so the primary mode may
    not be read back from one."""
    intent = doc("request-intent-model.md")
    problems = []
    if says("request-intent-model.md",
            "the primary mode is derived upstream, or it is `UNKNOWN`"):
        problems.append("RI-13 is missing: the derivation is not confined to upstream material")
    if says("request-intent-model.md", "the derivation reads the Request and nothing else"):
        problems.append("the derivation does not declare its own inputs")
    if says("request-intent-model.md", "it is never invented to avoid an `UNKNOWN`"):
        problems.append("an arbitrary primary could be picked to avoid UNKNOWN")
    if says("request-intent-model.md", "complete, not a remainder after an arbitrary pick"):
        problems.append("an UNKNOWN primary does not require the complete secondary set")
    for token in ("`primary_work_mode`", "`secondary_work_modes`"):
        if token not in intent:
            problems.append("the intent model omits %s" % token)
    scan(re.compile(
        r"`?primary_work_mode`?[^.|]{0,80}?"
        r"(from|by|reads?|derived|determined|decided)[^.|]{0,50}?"
        r"(planstage|plan stage|stage dependency|dependency order|later stages|"
        r"workflow candidate|plan stages)", re.IGNORECASE),
        "derives the primary mode from a downstream planning object", problems)
    scan(re.compile(
        r"`?secondary_work_modes`?[^.|]{0,60}?(contains?|includes?|carries)"
        r"[^.|]{0,30}?(the )?primary", re.IGNORECASE),
        "lets the secondary set duplicate the primary", problems)
    scan(re.compile(
        r"(work intent|workintent)[^.|]{0,60}?(has no|omits|without)[^.|]{0,30}?"
        r"primary_?work_?mode", re.IGNORECASE),
        "lets a Work Intent omit the primary mode", problems, strict=False)
    return (not problems, str(problems)[:400] if problems
            else "five ordered upstream tests, UNKNOWN where none resolves, no downstream read")


check("handoff", "the primary work mode is derived from upstream material only",
      the_primary_mode_is_derived_upstream_only)


def the_load_bearing_test_precedes_any_reduction():
    """Blocker 5 and escaped class 2. The predicate is evaluated against the deliverable the
    user asked for, and a reduction is its consequence rather than its evidence."""
    roles = doc("role-skill-requirement-inference.md")
    problems = []
    for phrase in ("every test is evaluated against the deliverable the user originally requested",
                   "before any constraint-induced reduction",
                   "a reduced deliverable is never evidence about the removed capability",
                   "the no-owner case is never routed through F-5",
                   "a conclusion the user asked for cannot be narrowed away"):
        if says("role-skill-requirement-inference.md", phrase):
            problems.append("missing %r" % phrase[:52])
    for token in ("LB-0", "LB-6", "RS-12", "RS-13", "NO_APPROVED_ROLE_OWNS_CONCLUSION"):
        if token not in roles:
            problems.append("the corrected predicate omits %s" % token)
    # F-14 must exist, block, and be distinguished from F-5 and F-6.
    failures = doc("failure-and-escalation-model.md")
    row = [ln for ln in failures.splitlines()
           if "NO_APPROVED_ROLE_OWNS_CONCLUSION" in ln and ln.startswith("|")]
    if not row:
        problems.append("F-14 has no row")
    else:
        low = flat(row[0])
        if "block" not in low:
            problems.append("F-14 does not block")
        if "f-5" not in low:
            problems.append("F-14 is not distinguished from F-5")
    for mode in ("REQUIRED_ROLE_UNAVAILABLE", "REQUIRED_SKILL_UNAVAILABLE"):
        r = [ln for ln in failures.splitlines() if mode in ln and ln.startswith("|")]
        if r and "approved" not in flat(r[0]):
            problems.append("%s does not confine itself to an approved owner" % mode)
    if says("governance-preflight.md",
            "No conclusion the originally requested deliverable needs is left without an "
            "approved owner"):
        problems.append("G-20 is missing: an unowned conclusion could pass preflight")
    scan(re.compile(
        r"(load.?bearing|not_load_bearing)[^.|]{0,80}?"
        r"(because|since|as)[^.|]{0,50}?(reduced|narrowed|constrained) deliverable",
        re.IGNORECASE),
        "uses a reduced deliverable as evidence about the removed capability", problems)
    scan(re.compile(
        r"(load.?bearing|disposition|constrain)[^.|]{0,70}?"
        r"(because of|on|from|given)[^.|]{0,30}?"
        r"(urgency|the deadline|convenience|how confident|confidence|seniority)",
        re.IGNORECASE),
        "decides the load-bearing result from urgency, confidence or convenience", problems)
    return (not problems, str(problems)[:400] if problems
            else "the predicate reads the original deliverable; reduction follows, never decides")


check("failure", "load-bearing is decided on the original deliverable, before any reduction",
      the_load_bearing_test_precedes_any_reduction)


def prerequisite_references_are_a_strict_tri_state():
    """Blocker 6. RESOLVED, FUTURE_GOVERNANCE_REFERENCE, or blocking. Never a passable UNKNOWN."""
    handoff = doc("orchestrator-handoff-contract.md")
    problems = []
    if says("orchestrator-handoff-contract.md",
            "a plain `UNKNOWN` prerequisite blocks, and is never rewritten as a declared future"):
        problems.append("HO-15 is missing: UNKNOWN could pass as a deferred reference")
    if says("failure-and-escalation-model.md",
            "a prerequisite reference is `RESOLVED`, `FUTURE_GOVERNANCE_REFERENCE`, or"):
        problems.append("FE-13 is missing")
    for state in ("`RESOLVED`", "`FUTURE_GOVERNANCE_REFERENCE`", "`UNKNOWN`"):
        if state not in handoff:
            problems.append("the prerequisite states omit %s" % state)
    g19 = [ln for ln in doc("governance-preflight.md").splitlines()
           if ln.startswith("| **G-19**")]
    if not g19:
        problems.append("preflight has no prerequisite-state check")
    elif "future_governance_reference" not in flat(g19[0]):
        problems.append("G-19 does not name the deferred state")
    # The retired formulation must not survive in any active location.
    scan(re.compile(
        r"(prerequisite|reference|refs?)[^.|]{0,60}?"
        r"(resolved or (?:explicitly )?`?unknown`?|`?unknown`? or resolved)", re.IGNORECASE),
        "still permits a prerequisite to be 'resolved or explicitly UNKNOWN'", problems,
        strict=False)
    scan(re.compile(
        r"`?unknown`?[^.|]{0,50}?(is|counts as|is treated as|equals?|amounts to)"
        r"[^.|]{0,30}?`?future_governance_reference`?", re.IGNORECASE),
        "equates UNKNOWN with a declared future reference", problems)
    return (not problems, str(problems)[:400] if problems
            else "three prerequisite states; a plain UNKNOWN blocks and is never relabelled")


check("handoff", "a prerequisite reference is resolved, declared future, or blocking",
      prerequisite_references_are_a_strict_tri_state)


def the_self_check_inventory_matches_the_package():
    """Counts stated in prose must be derived from the package, not remembered from a draft."""
    problems = []
    self_check = doc("phase-15-self-check.md")
    open_items = doc("open-items.md")
    declared = sorted({int(n) for n in re.findall(r"\*\*PO-(\d+)\*\*", open_items)})
    if not declared:
        problems.append("open-items.md declares no PO- items")
    elif declared != list(range(1, len(declared) + 1)):
        problems.append("the open-item inventory is not PO-1..PO-%d: %s"
                        % (len(declared), declared))
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
             8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
             14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen",
             18: "eighteen", 19: "nineteen", 20: "twenty"}
    n = len(declared)
    low = flat(self_check)
    # The stated count must be the derived one, and no other count may be claimed.
    if "%s open items" % words.get(n, n) not in low and "%d open items" % n not in low:
        problems.append("the self-check does not state the derived count of %d open items" % n)
    for other, word in words.items():
        if other == n:
            continue
        if "%s open items" % word in low or re.search(r"\b%d open items\b" % other, low):
            problems.append("the self-check states %d open items; the inventory has %d"
                            % (other, n))
    # The same discipline for the two other counted inventories.
    records = len(re.findall(r"(?m)^\|\s*\d+\s*\|\s*`\w+`\s*\|",
                             doc("work-plan-object-model.md")))
    if "%s records" % words.get(records, records) not in flat(doc("work-plan-object-model.md")):
        problems.append("the object model does not state its own record count of %d" % records)
    modes = len(re.findall(r"(?m)^\|\s*F-\d+\s*\|", doc("failure-and-escalation-model.md")))
    if "%s planning failure modes" % words.get(modes, modes) not in \
            flat(doc("failure-and-escalation-model.md")):
        problems.append("the failure model does not state its own count of %d modes" % modes)
    return (not problems, str(problems)[:400] if problems
            else "%d open items, %d records, %d failure modes - each counted from the package"
                 % (n, records, modes))


check("structure", "every stated inventory count is the package's own count",
      the_self_check_inventory_matches_the_package)


def po_4_stays_an_explicit_blocked_implementation_dependency():
    """PO-4 is approvable only while it stays explicit and fail-closed. It may never be waved."""
    items = doc("open-items.md")
    problems = []
    if says("open-items.md", "APPROVABLE WITH EXPLICIT BLOCKED IMPLEMENTATION DEPENDENCY"):
        problems.append("PO-4's classification is not preserved")
    for phrase in ("MATCH is **executable in principle**",
                   "cannot currently start a Phase 11 run",
                   "requires **explicit Phase 11 change control**"):
        if says("open-items.md", phrase):
            problems.append("PO-4 does not state %r" % phrase[:44])
    if "Reading C" not in items or says("open-items.md", "reading c is excluded here"):
        problems.append("the self-registration reading is not excluded")
    # The architecture's own intake-check-1 row is where a reader first meets the question, and
    # it is the row a weakening would edit. A scan could not reach it: `work_plan.<id>` carries a
    # dot, which the cell-bounded patterns stop at. So the row is checked structurally.
    architecture = doc("intent-work-planning-architecture.md")
    row = [ln for ln in architecture.splitlines()
           if ln.startswith("| 1. Workflow definition resolves")]
    if not row:
        problems.append("the architecture does not map intake check 1")
    else:
        low = flat(row[0])
        if "not a workflow definition" not in low:
            problems.append("intake check 1 no longer says a Work Plan is not a Workflow "
                            "definition")
        if "po-4" not in low:
            problems.append("intake check 1 does not carry the PO-4 dependency")
    scan(re.compile(
        r"(compose|composed plan|work.?plan)[^.|]{0,70}?"
        r"(satisfies|passes|meets|clears)[^.|]{0,30}?intake check 1", re.IGNORECASE),
        "claims COMPOSE satisfies intake check 1", problems)
    scan(re.compile(
        r"(compose|composed plan|work.?plan)[^.|]{0,60}?"
        r"(is executable|is runnable|can start a run|starts a run|may start a run)",
        re.IGNORECASE),
        "claims a Work Plan can start a run today", problems)
    return (not problems, str(problems)[:400] if problems
            else "PO-4 stays explicit, fail-closed, and excludes self-registration")


check("preflight", "PO-4 remains an explicit blocked implementation dependency",
      po_4_stays_an_explicit_blocked_implementation_dependency)


# =========================================================== second-location scans
#
# The independent review planted 16 weakenings in SECOND locations - an active statement that
# carries a rule without being the rule's canonical owner - and 12 of them were not observed.
# Each check below owns one of those classes and scans every statement in the package with the
# stricter denied_near test, so that a rule surviving in its own table is not mistaken for a
# rule surviving everywhere.


def no_capability_is_substituted_by_a_similar_one():
    problems = []
    if says("role-skill-requirement-inference.md", "co-activation, never blending"):
        problems.append("RS-4 is missing")
    if says("role-skill-requirement-inference.md", "business necessity is not a role"):
        problems.append("RS-11 is missing")
    scan(re.compile(
        r"(role|skill|review profile|capability|owner)[^.|]{0,70}?"
        r"(is )?(substitut\w*|replac\w*|stands? in|steps? in|covers? for|is covered by|"
        r"nearest|closest|most similar|next best)[^.|]{0,40}?"
        r"(role|skill|review profile|capability|conclusion)", re.IGNORECASE),
        "substitutes one capability for another", problems)
    scan(re.compile(
        r"(unavailable|missing|absent)[^.|]{0,40}?(role|skill)[^.|]{0,50}?"
        r"(reassigned?|assigned? to|handled by|taken (?:on )?by)", re.IGNORECASE),
        "reassigns an unavailable capability's conclusion", problems)
    return (not problems, str(problems)[:400] if problems
            else "an unavailable capability is never covered by a similar one")


check("second-location", "an unavailable Role or Skill is never replaced by a similar one",
      no_capability_is_substituted_by_a_similar_one)


def a_candidate_capability_is_never_treated_as_approved():
    problems = []
    if says("role-skill-requirement-inference.md", "a candidate Skill is not a Skill"):
        problems.append("RS-8 is missing")
    if says("role-skill-requirement-inference.md",
            "a candidate capability is unavailable for the predicate too"):
        problems.append("LB-5 is missing: a candidate could count as present")
    scan(re.compile(
        r"(candidate|proposed|future|forthcoming|pending)[^.|]{0,50}?"
        r"(role|skill|capability|review profile|specialist)[^.|]{0,60}?"
        r"(is |counts? as |treated as |may be )(approved|available|activat\w*|used|relied)",
        re.IGNORECASE),
        "treats a candidate capability as approved", problems)
    scan(re.compile(
        r"(difficult conversations?|communication strategy)[^.|]{0,70}?"
        r"(is approved|is available|may be used|can be activated|owns)", re.IGNORECASE),
        "treats the unapproved communication capability as available", problems)
    return (not problems, str(problems)[:400] if problems
            else "a candidate capability is absent, for planning and for the predicate alike")


check("second-location", "a candidate capability is never treated as approved",
      a_candidate_capability_is_never_treated_as_approved)


def a_requirement_is_never_its_own_satisfaction():
    """ReviewRequirement != a satisfied review; DecisionRequirement != an exercised Right."""
    problems = []
    if says("governance-preflight.md", "it never satisfies a review"):
        problems.append("GP-8 is missing")
    if says("governance-preflight.md", "it never exercises a right"):
        problems.append("GP-9 is missing")
    model = doc("work-plan-object-model.md")
    for token, label in (("**Never satisfied here**", "ReviewRequirement"),
                         ("**Never exercised here**", "DecisionRequirement")):
        if token not in model:
            problems.append("%s does not declare that it is never discharged here" % label)
    scan(re.compile(
        r"(review\s?requirement|reviewrequirement|planned review|required review)[^.|]{0,60}?"
        r"(is satisfied|satisfies|counts as|stands (?:in )?for|discharges|marked satisfied|"
        r"is the review|serves as (?:the |a )?review)", re.IGNORECASE),
        "treats a ReviewRequirement as a satisfied review", problems)
    scan(re.compile(
        r"(decision\s?requirement|decisionrequirement|resolved right|named right)[^.|]{0,60}?"
        r"(is exercised|exercises|counts as|discharges|is the decision|"
        r"serves as (?:the |a )?(?:decision|approval)|constitutes approval)", re.IGNORECASE),
        "treats a DecisionRequirement as an exercised Right", problems)
    return (not problems, str(problems)[:400] if problems
            else "requirements are recorded, never discharged, inside planning")


check("second-location", "a recorded requirement is never its own satisfaction",
      a_requirement_is_never_its_own_satisfaction)


def a_planning_record_is_never_governance_evidence():
    problems = []
    if says("work-plan-object-model.md",
            "planning records persist, and persistence is not authority"):
        problems.append("OM-7 is missing")
    if says("work-plan-object-model.md",
            "a planning record is never evidence for the work it planned"):
        problems.append("OM-8 is missing")
    if says("orchestrator-handoff-contract.md",
            "`planning_provenance` is operational, not evidence"):
        problems.append("HO-5 is missing")
    scan(re.compile(
        r"(planning record|persisted record|plan|provenance|planning provenance|"
        r"planning finding)[^.|]{0,70}?"
        r"(is evidence|counts as evidence|serves as evidence|is governance evidence|"
        r"may be cited as|satisfies (?:a |the )?(?:gate|requirement)|"
        r"establishes (?:the |a )?(?:fact|claim|entitlement))", re.IGNORECASE),
        "treats a persisted planning record as governance evidence", problems)
    return (not problems, str(problems)[:400] if problems
            else "planning records persist and remain non-authoritative, non-evidential")


check("second-location", "a persisted planning record is never governance evidence",
      a_planning_record_is_never_governance_evidence)


def scope_ancestry_is_never_decided_by_similarity():
    problems = []
    if says("context-scope-resolution.md", "string proximity is not ancestry"):
        problems.append("CS-5 is missing")
    scan(re.compile(
        r"(similar\w*|name|naming|string|prefix|substring|lexical|fuzzy|closest|nearest)"
        r"[^.|]{0,60}?"
        r"(determines?|decides?|resolves?|establishes?|implies|indicates?|selects?)"
        r"[^.|]{0,40}?(scope|ancestry|parent|sibling|hierarchy)", re.IGNORECASE),
        "resolves scope or ancestry by string similarity", problems)
    scan(re.compile(
        r"(sibling|neighbouring|adjacent|related)\s+(scope|project|programme)[^.|]{0,60}?"
        r"(may be (?:used|selected|chosen)|is selected|is chosen|is assumed)", re.IGNORECASE),
        "selects a sibling scope without resolution", problems)
    return (not problems, str(problems)[:400] if problems
            else "ancestry comes from the approved graph, never from a name")


check("second-location", "scope ancestry is never decided by string similarity",
      scope_ancestry_is_never_decided_by_similarity)


def phase_15_never_performs_an_intake_check():
    problems = []
    if says("intent-work-planning-architecture.md", "the orchestrator re-checks everything"):
        problems.append("PL-7 is missing")
    if says("intent-work-planning-architecture.md",
            "phase 15's obligation is to make each of them answerable, not to perform them"):
        problems.append("the architecture does not separate answerable from performed")
    scan(re.compile(
        r"(planner|planning layer|phase 15|preflight|plan)[^.|]{0,80}?"
        r"(performs?|carries out|completes?|discharges?|satisfies|passes|clears|"
        r"stands in for|replaces)[^.|]{0,40}?(intake check|intake validation|"
        r"orchestrator intake)", re.IGNORECASE),
        "has Phase 15 performing a Phase 11 intake check", problems)
    scan(re.compile(
        r"(intake|orchestrator)[^.|]{0,60}?"
        r"(need not|does not need to|may skip|is relieved of|can rely on the planner)",
        re.IGNORECASE),
        "relieves Phase 11 intake of re-checking", problems, strict=False)
    return (not problems, str(problems)[:400] if problems
            else "Phase 15 makes the seven intake checks answerable and performs none")


check("second-location", "Phase 15 makes intake checks answerable and never performs one",
      phase_15_never_performs_an_intake_check)


def no_plan_is_registered_or_auto_approved_anywhere():
    """Escape class 1, scanned outside the learning-boundary document's own tables."""
    problems = []
    if says("workflow-candidate-learning-boundary.md",
            "self-approval is impossible by construction, not by policy"):
        problems.append("WL-4 is missing")
    scan(re.compile(
        r"(repeated|recurring|similar|observed|common)[^.|]{0,40}?"
        r"(plans?|patterns?)[^.|]{0,60}?"
        r"(auto-?register\w*|registers?|are registered|becomes? (?:an? )?(?:approved )?workflow|"
        r"are promoted|is promoted|enter the (?:workflow )?registry)", re.IGNORECASE),
        "auto-registers a repeated pattern as a Workflow", problems)
    scan(re.compile(
        r"(candidate|suggestion|pattern)[^.|]{0,60}?"
        r"(status|is)[^.|]{0,20}?`?APPROVED`?", re.IGNORECASE),
        "gives a candidate suggestion APPROVED status", problems)
    scan(re.compile(
        r"(planner|system|phase 15|layer)[^.|]{0,60}?"
        r"(writes?|registers?|commits?|persists?)[^.|]{0,40}?"
        r"(workflow registry|governed registry|role registry|skill registry)", re.IGNORECASE),
        "writes to a governed registry", problems)
    return (not problems, str(problems)[:400] if problems
            else "no repeated pattern reaches the registry by any route")


check("second-location", "a repeated pattern is never auto-registered or auto-approved",
      no_plan_is_registered_or_auto_approved_anywhere)


def confidence_never_bypasses_a_blocking_clarification():
    """Escape class 2: C4 and C5 block regardless of how sure the planner is."""
    problems = []
    if says("clarification-policy.md",
            "the class is decided by consequence, not by confidence"):
        problems.append("the class could be decided by confidence")
    scan(re.compile(
        r"(confidence|certainty|score|sure|confident)[^.|]{0,70}?"
        r"(skips?|bypass\w*|waives?|removes?|avoids?|obviates?|closes?|answers?|"
        r"makes? unnecessary)[^.|]{0,40}?"
        r"(clarification|question|c4|c5|blocking class)", re.IGNORECASE),
        "lets confidence bypass a blocking clarification", problems)
    scan(re.compile(
        r"(c4|c5|blocking clarification)[^.|]{0,60}?"
        r"(is skipped|may be skipped|is waived|may be waived|need not be asked|"
        r"is answered by the planner)", re.IGNORECASE),
        "lets a blocking clarification go unasked", problems)
    return (not problems, str(problems)[:400] if problems
            else "C4 and C5 are decided by consequence and asked regardless of confidence")


check("second-location", "high confidence never bypasses a C4 or C5 clarification",
      confidence_never_bypasses_a_blocking_clarification)


def no_epistemic_promotion_in_any_second_location():
    """Escape class 9, scanned as a verb rather than only as an arrow."""
    problems = []
    scan(re.compile(
        r"(ai_?suggestion|suggestion|inference|assumption|planner output|planning output)"
        r"[^.|]{0,70}?"
        r"(becomes?|is promoted|promotes?|is upgraded|upgrades?|is converted|converts?|"
        r"is recorded as|is treated as|counts as|matures into)[^.|]{0,40}?"
        r"(fact_?claim|fact|evidence|approved knowledge|canonical)", re.IGNORECASE),
        "promotes AI output into a stronger knowledge state", problems)
    scan(re.compile(
        r"(once|after|where)[^.|]{0,50}?(confirmed|accepted|validated|reviewed)[^.|]{0,40}?"
        r"(ai_?suggestion|suggestion|intent)[^.|]{0,40}?"
        r"(fact_?claim|approved|canonical)", re.IGNORECASE),
        "converts a confirmed reading into an approved knowledge state", problems)
    return (not problems, str(problems)[:400] if problems
            else "no verb anywhere promotes AI_SUGGESTION into a stronger state")


check("second-location", "AI_SUGGESTION is never promoted to FACT_CLAIM anywhere",
      no_epistemic_promotion_in_any_second_location)


def no_planning_object_selects_a_model():
    """Escape class 10: the planning-stage spec is a second location for N-10."""
    problems = []
    scan(re.compile(
        r"(spec|specification|work item|plan stage|stage|plan|envelope)[^.|]{0,60}?"
        r"(selects?|chooses?|names?|binds?|specifies?|carries)[^.|]{0,30}?"
        r"(a |the )?(model|model profile|provider|routing decision)", re.IGNORECASE),
        "lets a planning object select a model", problems)
    return (not problems, str(problems)[:400] if problems
            else "no planning object, spec included, reaches a model")


check("second-location", "no planning object selects a model, spec included",
      no_planning_object_selects_a_model)


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
